import sqlite3
import datetime


class noteDatabase:
    def __init__(self, filename="term_note.db"):
        self.db = sqlite3.connect(filename)
        with self.db as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS note
            (id INTEGER PRIMARY KEY,
            title TEXT,
            text TEXT,
            date_created TEXT,
            date_modified TEXT)""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS tag
            (id INTEGER PRIMARY KEY,
            name TEXT)""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS tagmap
            (id INTEGER PRIMARY KEY,
            note_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY(note_id) REFERENCES note(id),
            FOREIGN KEY(tag_id) REFERENCES tag(id))""")

    def add_note(self, title, text, tags=[]):
        date = datetime.datetime.now()
        with self.db as cursor:
            cursor.execute(
                "INSERT INTO note (title, text, date_created, date_modified) VALUES(?,?,?,?)",
                (title, text, date, date)) 


db = noteDatabase()
db.add_note("Test", "Something")
