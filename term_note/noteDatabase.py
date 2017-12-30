from datetime import datetime
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy import select
from collections import namedtuple


note_record = namedtuple(
    'note_record', ['id', 'title', 'text', 'created', 'modified'])


class NoteDatabase:
    def __init__(self, engine=create_engine('sqlite:///note.db')):
        self.engine = engine
        self.create_tables()

    def create_tables(self):
        """Generate tables"""

        metadata = MetaData()
        self.note = Table('note',
                          metadata,
                          Column('id', Integer, primary_key=True),
                          Column('title', String),
                          Column('text', String),
                          Column('created', DateTime),
                          Column('modified', DateTime))
        self.tag = Table('tag',
                         metadata,
                         Column('id', Integer, primary_key=True),
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
            ins = self.note.insert()
            result = conn.execute(ins, title=title, text=text,
                                  created=datetime.now(),
                                  modified=datetime.now())
            id = result.inserted_primary_key[0]

        tag_ids = self.add_tags(tags)
        self.add_tagmaps(id, tag_ids)

        return id

    def add_tags(self, tags):
        """Add tags to db

        Take tags given and add them to the db

        Arguments:
            tags {list(string)} -- The tag names to be added

        Returns:
            list(int) -- The ids of all inserted tags
        """
        with self.engine.begin() as conn:
            ins = self.tag.insert()
            tag_ids = []
            for tag in tags:
                tag_ids.append(conn.execute(
                    ins, name=tag).inserted_primary_key[0])
        return tag_ids

    def add_tagmaps(self, id, tag_ids):
        """Add tagmaps to db

        Add the link between note and tags

        Arguments:
            id {int} -- The id of the note to be linked
            tag_ids {list(int)} -- The ids of tags to be linked
        """
        tagmaps = map(lambda tag_id: {"note_id": id, "tag_id": tag_id},
                      tag_ids)

        with self.engine.begin() as conn:
            ins = self.tagmap.insert()
            conn.execute(ins, list(tagmaps))

    def delete(self, id):
        """Delete a note

        Delete a note and any tagmaps related

        Arguments:
            id {int} -- The id of the note
        """
        with self.engine.begin() as conn:
            d = self.tagmap.delete().where(self.tagmap.c.note_id == id)
            conn.execute(d)

        with self.engine.begin() as conn:
            d = self.note.delete().where(self.note.c.id == id)
            conn.execute(d)

    def update(self, id, **kwargs):
        """Update a note

        [description]

        Arguments:
            id {int} -- The id of the note to update
            **kwargs -- The fields to be updated
        """
        with self.engine.begin() as conn:
            u = self.note.update().where(self.note.c.id == id)
            conn.execute(u, kwargs)

    def notes(self):
        s = select([self.note])
        with self.engine.begin() as conn:
            return list(map(lambda x: note_record(*x), conn.execute(s).fetchall()))
