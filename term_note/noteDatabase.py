import sqlite3
import datetime


class noteDatabase:
    def __init__(self, filename="term_note.db"):
        self.db = sqlite3.connect(filename)
        self.create_tables(self.db)

    def create_tables(self, db):
        with db as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS note
            (id INTEGER PRIMARY KEY,
            title TEXT,
            text TEXT,
            date_created TEXT,
            date_modified TEXT)""")

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tag
            (id INTEGER PRIMARY KEY,
            name TEXT)""")

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tagmap
            (id INTEGER PRIMARY KEY,
            note_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY(note_id) REFERENCES note(id),
            FOREIGN KEY(tag_id) REFERENCES tag(id))""")

    def add_note(self, title, text, tags=[]):
        date = datetime.datetime.now()
        tag_ids = []
        with self.db as c:
            c.execute(
                "INSERT INTO note (title, text, date_created, date_modified) VALUES(?,?,?,?)",
                (title, text, date, date))

            for tag in tags:
                cur = c.execute("SELECT id FROM tag WHERE name = ?", (tag,))
                # print( cur, tag)
                if(not cur.fetchone()):
                    c.execute("INSERT INTO tag (name) VALUES(?)", (tag,))


    def pull(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tag")
        a = cursor.fetchall()
        return a


db = noteDatabase()
db.add_note("Test", "Something", ['stuff', 'things', 'trifal'])
