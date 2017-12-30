import pytest
import os
from term_note.noteDatabase import NoteDatabase
from sqlalchemy import create_engine, select, delete
from datetime import datetime


@pytest.fixture(scope="module")
def engine():
    db_file = "test.db"
    engine = create_engine("sqlite:///test.db")
    yield engine
    os.remove(db_file)


@pytest.fixture()
def note_db_no_tables(engine):
    return NoteDatabase(engine)


@pytest.fixture()
def note_db(engine):
    db = NoteDatabase(engine)
    db.create_tables()
    yield db
    with engine.begin() as conn:
        conn.execute(db.note.delete())
        conn.execute(db.tag.delete())
        conn.execute(db.tagmap.delete())


def get_all_data(engine, note_db):
    """Get all db data

    Convnience function for getting all
    testable db data
    """
    with engine.begin() as conn:
        note = select([note_db.note.c.id,
                       note_db.note.c.title,
                       note_db.note.c.text])
        tags = select([note_db.tag])
        tagmaps = select([note_db.tagmap])
        note_result = conn.execute(note).fetchall()
        tags_result = conn.execute(tags).fetchall()
        tagmaps_result = conn.execute(tagmaps).fetchall()
    return note_result, tags_result, tagmaps_result


def test_create_tables(note_db_no_tables, engine):
    note_db_no_tables.create_tables()
    assert(engine.table_names() == ["note", "tag", "tagmap"])


def test_add_note_without_tags(note_db, engine):
    note_id = note_db.add("stuff", "things")
    with engine.begin() as conn:
        s = select([note_db.note.c.id,
                    note_db.note.c.title,
                    note_db.note.c.text]).where(note_db.note.c.id == note_id)
        result = conn.execute(s).fetchone()
    assert((1, "stuff", "things") == result)


def test_add_note_with_tags(note_db, engine):
    note_db.add("stuff1", "things1", ["tag1", "tag2"])
    note_db.add("stuff2", "things2", ["tag3"])
    note_result, tags_result, tagmaps_result = get_all_data(engine, note_db)

    assert([(1, "stuff1", "things1"),
            (2, "stuff2", "things2")] == note_result)

    assert([(1, "tag1"),
            (2, "tag2"),
            (3, "tag3")] == tags_result)

    assert([(1, 1),
            (1, 2),
            (2, 3)] == tagmaps_result)


def test_delete_note(note_db, engine):
    note = note_db.note.insert()
    tag = note_db.tag.insert()
    tagmap = note_db.tagmap.insert()

    with engine.begin() as conn:
        conn.execute(note, id=1, title="hello",
                     text="world",
                     created=datetime(1, 1, 1),
                     modified=datetime(1, 1, 1))
        conn.execute(tag, [{"id": 1, "name": "tag1"},
                           {"id": 2, "name": "tag2"}])
        conn.execute(tagmap, [{"note_id": 1, "tag_id": 1},
                              {"note_id": 1, "tag_id": 2}])
    note_db.delete(1)
    notes, tags, tagmaps = get_all_data(engine, note_db)
    assert([] == notes)
    assert([(1, "tag1"),
            (2, "tag2")] == tags)
    assert([] == tagmaps)


def test_update_note(note_db, engine):
    note = note_db.note.insert()
    tag = note_db.tag.insert()
    tagmap = note_db.tagmap.insert()

    with engine.begin() as conn:
        conn.execute(note, id=1, title="hello",
                     text="world",
                     created=datetime(1, 1, 1),
                     modified=datetime(1, 1, 1))
        conn.execute(tag, [{"id": 1, "name": "tag1"},
                           {"id": 2, "name": "tag2"}])
        conn.execute(tagmap, [{"note_id": 1, "tag_id": 1},
                              {"note_id": 1, "tag_id": 2}])

    note_db.update(1, title="Not", text="Today")
    notes, tags, tagmaps = get_all_data(engine, note_db)
    assert([(1, "Not", "Today")] == notes)
    assert([(1, "tag1"),
            (2, "tag2")] == tags)
    assert([(1, 1), (1, 2)] == tagmaps)


def test_notes(note_db, engine):
    note = note_db.note.insert()

    with engine.begin() as conn:
        conn.execute(note, id=1, title="hello",
                     text="world",
                     created=datetime(1, 1, 1),
                     modified=datetime(1, 1, 1))

    assert([(1, 'hello', 'world', datetime(1, 1, 1),
             datetime(1, 1, 1))] == note_db.notes())
