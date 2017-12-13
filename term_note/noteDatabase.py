from datetime import datetime
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime, select, func


class NoteDatabase:
    def __init__(self, engine=create_engine('sqlite:///note.db:', echo=True)):
        self.engine = engine

    def create_tables(self):
        """Generate tables"""

        metadata = MetaData()
        self.note = Table('note',
                          metadata,
                          Column('id', Integer, primary_key=True),
                          Column('title', String(30)),
                          Column('text', String(200)),
                          Column('date_created', DateTime),
                          Column('date_modified', DateTime))
        self.tag = Table('tag',
                         metadata,
                         Column('id', Integer, primary_key=True, autoincrement=False),
                         Column('name', String))
        self.tagmap = Table('tagmap',
                            metadata,
                            Column('note_id', ForeignKey('note.id')),
                            Column('tag_id', ForeignKey('tag.id')))
        metadata.create_all(self.engine)

    def add(self, title, text, tags=None):
        if tags is None:
            tags = []

        with self.engine.begin() as conn:
            result = conn.execute(self.note.insert(), title=title, text=text,
                              date_created=datetime.now(), date_modified=datetime.now())

            return result.inserted_primary_key[0]


    # def add_tags(self, note_id, tags):
    #     for tag in tags:
    #         tag_id = self.db_con.execute(
    #             "SELECT tag_id FROM tag WHERE name = ?", (tag, )).fetchone()
    #         if (not tag_id):
    #             with self.db_con as con:
    #                 tag_id = con.execute("INSERT INTO tag (name) VALUES(?)",
    #                                      (tag, )).lastrowid
    #         else:
    #             tag_id = tag_id[0]

    #         with self.db_con as con:
    #             con.execute("INSERT INTO tagmap (note_id, tag_id) VALUES(?,?)",
    #                         (note_id, tag_id))

    # def add_note(self, title, text, tags=[]):
    #     date = datetime.datetime.now()
    #     with self.db_con as con:
    #         note_id = con.execute(
    #             "INSERT INTO note (title, text, date_created, date_modified) VALUES(?,?,?,?)",
    #             (title, text, date, date)).lastrowid

    #         self.add_tags(note_id, tags)

    #     return note_id

    # def delete_note(self, id):
    #     with self.db_con as con:
    #         con.execute("DELETE FROM note WHERE note_id = ? ", (id, ))
    #         con.execute("DELETE FROM tagmap WHERE note_id = ?", (id, ))

    # def update_note(self, id, title, text, tags):
    #     pass
