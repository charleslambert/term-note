from urwid import Frame, Text, Pile, LineBox, WidgetWrap, Edit, Filler, Columns, SimpleFocusListWalker, AttrMap, ListBox, connect_signal, Divider, BigText, BoxAdapter, SolidFill
from itertools import chain, zip_longest
from noteDatabase import NoteDatabase
import urwid


from noteDatabase import note_record
from datetime import datetime

class NoteEdit(WidgetWrap):
    signals = ['added']

    def __init__(self, db):
        self.new_note = False
        self.db = db

        self.title_header = Text('Title' + '\n{}'.format('=' * len('title')))
        self.title = Edit(multiline=True)

        self.text_header = Text('Text' + '\n{}'.format('=' * len('title')))
        self.text = Edit(multiline=True)

        self.tags_header = Text('Tags' + '\n{}'.format('=' * len('title')))
        self.tags = Edit(multiline=True)

        pile = Pile([
            self.title_header,
            self.title,
            self.text_header,
            self.text,
            self.tags_header,
            self.tags])
        pile = Filler(pile, valign='top')
        WidgetWrap.__init__(self, pile)

    def set_item(self, title='', body='', tag=''):
        self.title.set_edit_text(title)
        self.text.set_edit_text(body)
        self.tags.set_edit_text(tag)

    def keypress(self, size, key):
        if key == 'left':
            return None
        elif key == 'enter':
            if self.new_note:
                self.db.add(self.title.get_edit_text(),
                            self.text.get_edit_text(),
                            self.tags.get_edit_text())
            else:
                # self.db.update(self._w.base_widget[self._w.base_widget.focus_position].note.id,
                #                title=self.title.get_edit_text(),
                #                text=self.text.get_edit_text(),
                #                modified=datetime.now(),
                #                tags=self.tags.get_edit_text())
                pass

            self._emit('added')

        super(NoteEdit, self).keypress(size, key)
        return key


class listItem(Text):
    signals = ['activate']

    def __init__(self, note):
        self.note = note
        text = "{}\n{}\n{}".format(
            note.title, note.text[:20] + '...' if len(note.text) > 20 else note.text, note.created.date())
        Text.__init__(self, text)

    def keypress(self, size, key):
        return key

    def selectable(self):
        self._emit('activate', self.note)
        return True


class NoteList(WidgetWrap):
    signals = ['activate', 'create', 'delete']

    def __init__(self, db):
        self.db = db
        self.notes = self.db.notes()

        body = self.create_widget_list()
        body = SimpleFocusListWalker(body)
        body = ListBox(body)
        self.list = body
        WidgetWrap.__init__(self, self.list)

    def create_widget_list(self):
        wlist = map(lambda x: listItem(x), self.notes)
        wlist = map(lambda x: AttrMap(x, '', 'reveal focus'), wlist)
        wlist = map(lambda x: LineBox(x), wlist)
        wlist = list(wlist)
        for i in wlist:
            connect_signal(i.base_widget, 'activate', self.pass_activate)

        return list(wlist)

    def pass_activate(self, widget, note):
        self._emit('activate', note)

    def update(self):
        self.notes = self.db.notes()
        updated_list = self.create_widget_list()

        self._w.body[:] = updated_list

    def keypress(self, size, key):
        if key == 'j':
            try:
                self._w.focus_position += 1
            except IndexError:
                pass

        elif key == 'k':
            try:
                self._w.focus_position -= 1
            except IndexError:
                pass

        if key == 'right':
            return None
        if key == 'o':
            self._emit('create')

        if key == 'd':
            if len(self.list.body) > 0:
                self._emit('delete',
                           self._w.body[self._w.body.focus].base_widget.note.id)

        super(NoteList, self).keypress(size, key)
        return key


class NoteView(WidgetWrap):
    def __init__(self):
        self.db = NoteDatabase()
        self.edit = NoteEdit(self.db)
        self.list = NoteList(self.db)
        connect_signal(self.edit, 'added', self.update_handler)
        connect_signal(self.list, 'activate', self.selection_handler)
        connect_signal(self.list, 'create', self.creation_handler)
        connect_signal(self.list, 'delete', self.deletion_handler)
        colm = Columns([LineBox(self.list),  LineBox(self.edit)])

        # Adjust column size
        colm.contents[0] = (colm.contents[0][0], ('weight', 0.38, False))
        colm.options()
        self.colm = colm
        frame = Frame(LineBox(self.colm), footer=Text(['Enter to save (',
                                                       ('attr1', 'o'),
                                                       ') to create (',
                                                       ('attr1', 'd'),
                                                       ') to delete']))
        WidgetWrap.__init__(self, frame)

    def update_handler(self, widget):
        self.list.update()

    def selection_handler(self, widget, note):
        self.edit.set_item(note.title,  note.text)

    def creation_handler(self, widget):
        self.colm.focus_position = 1
        self.colm[1].new_note = True
        self.edit.set_item()

    def deletion_handler(self, widget, id):
        self.db.delete(id)
        self.list.update()

    def keypress(self, size, key):
        super(NoteView, self).keypress(size, key)
        if key == 'enter':
            if self.colm.focus_position == 0:
                self.colm.focus_position = 1
            else:
                try:
                    self.colm.focus_position = 0
                    self.colm[0].focus_position = 0
                except IndexError:
                    pass

                self.colm[1].new_note = False

        if key == 'ctrl x':
            raise urwid.ExitMainLoop()

        if key == 'l':
            try:
                self.colm.focus_position += 1
            except IndexError:
                pass

        return key


palette = [
    ('reveal focus', 'dark cyan', '', 'standout'),
    ('attr1', 'dark red', ''),
]


loop = urwid.MainLoop(NoteView(), palette=palette)
loop.run()
