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


def test_createTables(conn, note_db):
    note_db.createTables(conn)
    assert (conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            .fetchall() == [("note", ), ("tag", ), ("tagmap", )])


def test_add_note_no_tags(conn, note_db):
    note_db.add_note(conn, "stuff", "things")
    assert (conn.execute("""SELECT title FROM note WHERE title= "stuff";""")
            .fetchone() == ("stuff", ))


def test_add_note_with_tags(conn, note_db):
    note_db.add_note(conn, "stuff2", "things", ["tags", "moreTags"])
    assert (conn.execute("""SELECT title FROM note WHERE title= "stuff2";""")
            .fetchone() == ("stuff2", ))
    assert (conn.execute("""SELECT name FROM tag""").fetchall() == [
        ("tags", ), ("moreTags", )
    ])

    note_id = conn.execute(
        """SELECT id FROM note WHERE title = 'stuff2'""").fetchone()
    tag_ids = list(
        map(lambda x: x[0], conn.execute("""SELECT id FROM tag""").fetchall()))
    tagmap = [(note_id[0], tag_ids[0]), (note_id[0], tag_ids[1])]
    assert (conn.execute("""SELECT note_id, tag_id FROM tagmap WHERE note_id = ?""", note_id).fetchall()
            == tagmap)


def test_add_note_with_existing_tags(conn, note_db):
    note_db.add_note(conn, "stuff3", "things", ["tags", "moreTags"])
    assert (conn.execute("""SELECT title FROM note WHERE title= "stuff3";""")
            .fetchone() == ("stuff3", ))
    assert (conn.execute("""SELECT name FROM tag""").fetchall() == [
        ("tags", ), ("moreTags", )
    ])

    note_id = conn.execute(
        """SELECT id FROM note WHERE title = 'stuff3'""").fetchone()
    tag_ids = list(
        map(lambda x: x[0], conn.execute("""SELECT id FROM tag""").fetchall()))
    tagmap = [(note_id[0], tag_ids[0]), (note_id[0], tag_ids[1])]
    assert (conn.execute("""SELECT note_id, tag_id FROM tagmap WHERE note_id = ?""", note_id).fetchall()
            == tagmap)
