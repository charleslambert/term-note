import sqlite3
import datetime


class NoteDatabase:
    def __init__(self, conn):
        self.db = conn

    def create_tables(self, db):
        with db:
            db.execute("""
            CREATE TABLE IF NOT EXISTS note
            (note_id INTEGER PRIMARY KEY,
            title TEXT,
            text TEXT,
            date_created TEXT,
            date_modified TEXT)""")

            db.execute("""
            CREATE TABLE IF NOT EXISTS tag
            (tag_id INTEGER PRIMARY KEY,
            name TEXT)""")

            db.execute("""
            CREATE TABLE IF NOT EXISTS tagmap
            (tagmap_id INTEGER PRIMARY KEY,
            note_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY(note_id) REFERENCES note(id),
            FOREIGN KEY(tag_id) REFERENCES tag(id))""")

    def add_note(self, conn, title, text, tags=[]):
        date = datetime.datetime.now()
        with conn:
            note_id = conn.execute(
                "INSERT INTO note (title, text, date_created, date_modified) VALUES(?,?,?,?)",
                (title, text, date, date)).lastrowid

            for tag in tags:
                tag_id = conn.execute("SELECT tag_id FROM tag WHERE name = ?",
                                      (tag, )).fetchone()
                if (not tag_id):
                    with conn:
                        tag_id = conn.execute(
                            "INSERT INTO tag (name) VALUES(?)",
                            (tag, )).lastrowid
                else:
                    tag_id = tag_id[0]

                with conn:
                    conn.execute(
                        "INSERT INTO tagmap (note_id, tag_id) VALUES(?,?)",
                        (note_id, tag_id))
        return note_id

    def delete_note(self, conn, id):
        with conn:
            conn.execute("DELETE FROM note WHERE note_id = ? ", (id, ))
            conn.execute("DELETE FROM tagmap WHERE note_id = ?", (id, ))

    def update_note(self, conn, id, title, text, tags):
        pass
