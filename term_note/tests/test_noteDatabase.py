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
    note_db.create_tables(conn)
    assert (conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            .fetchall() == [("note", ), ("tag", ), ("tagmap", )])


def test_add_note_with_tags(conn, note_db):
    note_id = note_db.add_note(conn, "stuff", "things", ["tags", "moreTags"])
    assert (conn.execute("SELECT note_id FROM note WHERE note_id= ?;", (note_id, ))
            .fetchone() == (note_id, ))
    assert (conn.execute("SELECT name FROM tag").fetchall() == [
        ("tags", ), ("moreTags", )
    ])

    tag_ids = map(lambda x: x[0],
                  conn.execute("SELECT tag_id FROM tag").fetchall())
    tagmap = list(map(lambda x: (note_id, x), tag_ids))
    assert (conn.execute(
        "SELECT note_id, tag_id FROM tagmap WHERE note_id = ?",
        (note_id, )).fetchall() == tagmap)


def test_add_note_with_existing_tags(conn, note_db):
    note_id = note_db.add_note(conn, "stuff2", "things", ["tags", "moreTags"])

    print(conn.execute("SELECT note_id FROM note NATURAL join (tagmap NATURAL join tag) WHERE note_id = ?", (note_id,)))

    assert (conn.execute("""SELECT note_id FROM note WHERE note_id = ?;""", (note_id, ))
            .fetchone() == (note_id, ))
    assert (conn.execute("""SELECT name FROM tag""").fetchall() == [
        ("tags", ), ("moreTags", )
    ])

    tag_ids = map(lambda x: x[0],
                  conn.execute("""SELECT tag_id FROM tag""").fetchall())
    tagmap = list(map(lambda x: (note_id, x), tag_ids))
    assert (conn.execute(
        """SELECT note_id, tag_id FROM tagmap WHERE note_id = ?""",
        (note_id, )).fetchall() == tagmap)


def test_delete_note(conn, note_db):
    note_db.delete_note(conn, 2)
    assert (conn.execute("SELECT note_id FROM note WHERE note_id = ?",
                         (2, )).fetchone() is None)
    assert (conn.execute("SELECT note_id FROM tagmap WHERE note_id = ?",
                         (2, )).fetchall() == [])


def test_update_note(conn, note_db):
    note_id = 1
    note_db.update_note(conn, note_id, "not stuff", "not things",
                        ["tags", "lessTags"])
    # note = conn.execute(
    #     "SELECT title, text, date_modified FROM note WHERE id = ?",
    #     (note_id, )).fetchone()
    # tagmap = conn.execute("SELECT title, text, date_modified, name")
