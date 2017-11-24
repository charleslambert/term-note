import pytest
import sqlite3 as sql
import os
from term_note.noteDatabase import NoteDatabase


@pytest.fixture(scope="module")
def conn():
    db_file = "test.db"
    conn = sql.Connection(db_file)
    yield conn
    conn.close()
    os.remove(db_file)


@pytest.fixture
def note_db(conn):
    return NoteDatabase(conn)


def test_create_tables(conn, note_db):
    note_db.create_tables()
    assert (conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            .fetchall() == [("note", ), ("tag", ), ("tagmap", )])


def test_add_note_with_tags(conn, note_db):
    note_id = note_db.add_note("stuff", "things", ["tags", "moreTags"])

    assert (conn.execute("""SELECT note.note_id, tag.name FROM note
        JOIN (tagmap JOIN tag ON tagmap.tag_id = tag.tag_id)
        ON note.note_id = tagmap.note_id
        WHERE note.note_id = ?""",
                         (note_id, )).fetchall() == [(note_id, "tags"),
                                                     (note_id, "moreTags")])


def test_add_note_with_existing_tags(conn, note_db):
    note_id = note_db.add_note("stuff2", "things", ["tags", "moreTags"])

    assert (conn.execute("""SELECT note.note_id, tag.name FROM note
        JOIN (tagmap JOIN tag ON tagmap.tag_id = tag.tag_id)
        ON note.note_id = tagmap.note_id
        WHERE note.note_id = ?""",
                         (note_id, )).fetchall() == [(note_id, "tags"),
                                                     (note_id, "moreTags")])


def test_delete_note(conn, note_db):
    note_db.delete_note(2)
    assert (conn.execute("SELECT note_id FROM note WHERE note_id = ?",
                         (2, )).fetchone() is None)
    assert (conn.execute("SELECT note_id FROM tagmap WHERE note_id = ?",
                         (2, )).fetchall() == [])


# def test_update_note(conn, note_db):
#     note_id = 1
#     note_db.update_note(note_id, "not stuff", "not things",
#                         ["tags", "lessTags"])
#     assert (conn.execute(
#         """SELECT note.note_id, title, text, tag.name FROM note
#         JOIN (tagmap JOIN tag ON tagmap.tag_id = tag.tag_id)
#         ON note.note_id = tagmap.note_id
#         WHERE note.note_id = ?""",
#         (note_id, )).fetchall() == [(note_id, "not stuff", "not things",
#                                      "tags"), (note_id, "not stuff",
#                                                "not things", "lessTags")])
