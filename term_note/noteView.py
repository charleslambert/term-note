from urwid import Frame, Text, Pile, LineBox, WidgetWrap, Edit, Filler, Columns, SimpleFocusListWalker, AttrMap, ListBox, connect_signal
from noteDatabase import NoteDatabase
from urwid import MainLoop, ExitMainLoop
from noteEdit import NoteEdit
from noteList import NoteList

# from datetime import datetime


class NoteView(WidgetWrap):
    def __init__(self):
        self.db = NoteDatabase()
        self.edit = NoteEdit(self.db)
        self.list = NoteList(self.db)

        connect_signal(self.edit, 'added', self.update_handler)
        connect_signal(self.list, 'item focused', self.selection_handler)
        connect_signal(self.list, 'create', self.creation_handler)
        connect_signal(self.list, 'delete', self.deletion_handler)
        connect_signal(self.list, 'selected', self.switch_handler)

        colm = Columns([LineBox(self.list), LineBox(self.edit)])

        # Adjust column size
        colm.contents[0] = (colm.contents[0][0], ('weight', 0.38, False))
        colm.options()

        self.colm = colm
        frame = Frame(
            LineBox(self.colm),
            footer=Text([
                'Enter to save (', ('attr1', 'o'), ') to create (',
                ('attr1', 'd'), ') to delete'
            ]))
        WidgetWrap.__init__(self, frame)

    def update_handler(self, widget):
        self.list.update()
        self.switch_handler(widget, None)

    def selection_handler(self, widget, note):
        self.edit.set_item(note.title, note.text)
        self.edit.current_id = note.id

    def creation_handler(self, widget):
        self.colm.focus_position = 1
        self.colm[1].new_note = True
        self.edit.set_item()

    def deletion_handler(self, widget, id):
        self.db.delete(id)
        self.list.update()

    def switch_handler(self, widget, note):
        if widget is self.list:
            self.colm.focus_position = 1
            self.edit.current_id = note.id
        else:
            self.colm.focus_position = 0

    def keypress(self, size, key):
        super(NoteView, self).keypress(size, key)

        if key == 'ctrl x':
            raise ExitMainLoop()

        return key


palette = [
    ('reveal focus', 'dark cyan', '', 'standout'),
    ('attr1', 'dark red', ''),
]

loop = MainLoop(NoteView(), palette=palette)
loop.run()
