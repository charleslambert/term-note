from urwid import Text, SimpleFocusListWalker, ListBox, WidgetWrap, AttrMap, LineBox


class listItem(Text):
    def __init__(self, note):
        self.note = note
        text = "{}\n{}\n{}".format(note.title, note.text[:20] + '...'
                                   if len(note.text) > 20 else note.text,
                                   note.created.date())
        Text.__init__(self, text)

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

        initial_list= self._w.body
        if len(initial_list) > 0:
            self._emit('item focused', initial_list[0].note )

    def create_widget_list(self):
        wlist = map(lambda x: listItem(x), self.notes)
        wlist = map(lambda x: AttrMap(x, '', 'reveal focus'), wlist)
        wlist = map(lambda x: LineBox(x), wlist)

        return list(wlist)

    def update(self):
        self.notes = self.db.notes()
        updated_list = self.create_widget_list()
        self._w.body[:] = updated_list

    def keypress(self, size, key):
        if key == 'j':
            try:
                self._w.focus_position += 1
                self._emit('item focused', self._w.focus.base_widget.note)
            except IndexError:
                pass

        elif key == 'k':
            try:
                self._w.focus_position -= 1
                self._emit('item focused', self._w.focus.base_widget.note)
            except IndexError:
                pass

        elif key in ('enter', 'l'):
            self._emit('selected', self._w.focus.base_widget.note)

        elif key == 'right':
            return None

        elif key == 'o':
            self._emit('create')

        elif key == 'd':
            if len(self.list.body) > 0:
                self._emit('delete',
                           self._w.focus.base_widget.note.id)

        super(NoteList, self).keypress(size, key)
        return key
