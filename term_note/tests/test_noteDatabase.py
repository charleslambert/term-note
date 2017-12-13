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


def test_create_tables(note_db_no_tables, engine):
    note_db_no_tables.create_tables()
    assert(engine.table_names() == ["note", "tag", "tagmap"])


def test_add_note_without_tags(note_db, engine):
    note_id = note_db.add("stuff", "things")
    with engine.begin() as conn:
        s = select([note_db.note.c.id, note_db.note.c.title, note_db.note.c.text]).where(note_db.note.c.id == note_id)
        result = conn.execute(s).fetchone()
    assert((1, "stuff", "things") == result)

# def test_add_note_with_tags(conn, note_db):
#     note_id = note_db.add_note("stuff", "things", ["tags", "moreTags"])

#     assert (conn.execute("""SELECT note.note_id, tag.name FROM note
#         JOIN (tagmap JOIN tag ON tagmap.tag_id = tag.tag_id)
#         ON note.note_id = tagmap.note_id
#         WHERE note.note_id = ?""",
#                          (note_id, )).fetchall() == [(note_id, "tags"),
#                                                      (note_id, "moreTags")])


# def test_add_note_with_existing_tags(conn, note_db):
#     note_id = note_db.add_note("stuff2", "things", ["tags", "moreTags"])

#     assert (conn.execute("""SELECT note.note_id, tag.name FROM note
#         JOIN (tagmap JOIN tag ON tagmap.tag_id = tag.tag_id)
#         ON note.note_id = tagmap.note_id
#         WHERE note.note_id = ?""",
#                          (note_id, )).fetchall() == [(note_id, "tags"),
#                                                      (note_id, "moreTags")])


# def test_delete_note(conn, note_db):
#     note_db.delete_note(2)
#     assert (conn.execute("SELECT note_id FROM note WHERE note_id = ?",
#                          (2, )).fetchone() is None)
#     assert (conn.execute("SELECT note_id FROM tagmap WHERE note_id = ?",
#                          (2, )).fetchall() == [])


# # def test_update_note(conn, note_db):
# #     note_id = 1
# #     note_db.update_note(note_id, "not stuff", "not things",
# #                         ["tags", "lessTags"])
# #     assert (conn.execute(
# #         """SELECT note.note_id, title, text, tag.name FROM note
# #         JOIN (tagmap JOIN tag ON tagmap.tag_id = tag.tag_id)
# #         ON note.note_id = tagmap.note_id
# #         WHERE note.note_id = ?""",
# #         (note_id, )).fetchall() == [(note_id, "not stuff", "not things",
# #                                      "tags"), (note_id, "not stuff",
# #                                                "not things", "lessTags")])
