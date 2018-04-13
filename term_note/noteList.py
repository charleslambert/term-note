from urwid import Text, SimpleFocusListWalker, ListBox, WidgetWrap, AttrMap, LineBox


class listItem(Text):
    def __init__(self, note):
        self.note = note
        Text.__init__(self, self.format_note(self.note))

    def truncate(self, string, length):
        if len(string) > length:
            return string[:20] + '...'
        else:
            return string

    def format_note(self, note):
        return "{}\n{}\n{}".format(self.truncate(note.title, 20),
                                   self.truncate(note.text, 20),
                                   note.created.date())

    def keypress(self, size, key):
        return key

    def selectable(self):
        return True


class NoteList(WidgetWrap):
    signals = ['item focused', 'create', 'delete', 'selected']

    def __init__(self, db):
        self.db = db
        self.notes = self.db.notes()

        body = self.create_widget_list()
        body = SimpleFocusListWalker(body)
        body = ListBox(body)
        self.list = body

        WidgetWrap.__init__(self, self.list)

        initial_list = self._w.body
        if len(initial_list) > 0:
            self._emit('item focused', initial_list[0].base_widget.note)

    def create_widget_list(self):
        wlist = map(lambda x: listItem(x), self.notes)
        wlist = map(lambda x: AttrMap(x, '', 'reveal focus'), wlist)
        wlist = map(lambda x: LineBox(x), wlist)

        return list(wlist)

    def update(self):
        self.notes = self.db.notes()
        updated_list = self.create_widget_list()
        self._w.body[:] = updated_list

    def focused(self):
        self._emit('item focused', self._w.focus.base_widget.note)

    def attempt_move(self, n, direction):
        try:
            if direction == "pos":
                self._w.focus_position += 1
            else:
                self._w.focus_position -= 1

            self.focused()
        except IndexError:
            pass

    def keypress(self, size, key):
        if key == 'j':
            self.attempt_move(1, "pos")

        elif key == 'k':
            self.attempt_move(1, "neg")

        elif key in ('enter', 'l'):
            focused_widget = self._w.focus
            if focused_widget:
                self._emit('selected', focused_widget.base_widget.note)

        elif key == 'right':
            return None

        elif key == 'o':
            self._emit('create')

        elif key == 'd':
            if len(self.list.body) > 0:
                self._emit('delete', self._w.focus.base_widget.note.id)

        super(NoteList, self).keypress(size, key)
        return key
