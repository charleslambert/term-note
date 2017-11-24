import datetime


class NoteDatabase:
    def __init__(self, conn):
        self.db_con = conn

    def create_tables(self):
        with self.db_con as con:
            con.execute("""
            CREATE TABLE IF NOT EXISTS note
            (note_id INTEGER PRIMARY KEY,
            title TEXT,
            text TEXT,
            date_created TEXT,
            date_modified TEXT)""")

            con.execute("""
            CREATE TABLE IF NOT EXISTS tag
            (tag_id INTEGER PRIMARY KEY,
            name TEXT)""")

            con.execute("""
            CREATE TABLE IF NOT EXISTS tagmap
            (tagmap_id INTEGER PRIMARY KEY,
            note_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY(note_id) REFERENCES note(id),
            FOREIGN KEY(tag_id) REFERENCES tag(id))""")

    def add_tags(self, note_id, tags):
        for tag in tags:
            tag_id = self.db_con.execute(
                "SELECT tag_id FROM tag WHERE name = ?", (tag, )).fetchone()
            if (not tag_id):
                with self.db_con as con:
                    tag_id = con.execute("INSERT INTO tag (name) VALUES(?)",
                                         (tag, )).lastrowid
            else:
                tag_id = tag_id[0]

            with self.db_con as con:
                con.execute("INSERT INTO tagmap (note_id, tag_id) VALUES(?,?)",
                            (note_id, tag_id))

    def add_note(self, title, text, tags=[]):
        date = datetime.datetime.now()
        with self.db_con as con:
            note_id = con.execute(
                "INSERT INTO note (title, text, date_created, date_modified) VALUES(?,?,?,?)",
                (title, text, date, date)).lastrowid

            self.add_tags(note_id, tags)

        return note_id

    def delete_note(self, id):
        with self.db_con as con:
            con.execute("DELETE FROM note WHERE note_id = ? ", (id, ))
            con.execute("DELETE FROM tagmap WHERE note_id = ?", (id, ))

    def update_note(self, id, title, text, tags):
        pass
