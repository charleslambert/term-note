from urwid import Text, Edit, Pile, Filler, WidgetWrap
from datetime import datetime
from operator import iadd, isub

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
            self.title_header, self.title, self.text_header, self.text,
            self.tags_header, self.tags
        ])
        pile = Filler(pile, valign='top')
        WidgetWrap.__init__(self, pile)

    def set_item(self, title='', body='', tag=''):
        self.title.set_edit_text(title)
        self.text.set_edit_text(body)
        self.tags.set_edit_text(tag)

    def keypress(self, size, key):
        if key == 'left':
            return None

        elif key == 'ctrl w':
            if self.new_note:
                self.db.add(self.title.get_edit_text(),
                            self.text.get_edit_text(),
                            self.tags.get_edit_text())
            else:
                self.db.update(
                    self.current_id,
                    title=self.title.get_edit_text(),
                    text=self.text.get_edit_text(),
                    modified=datetime.now(),
                    tags=self.tags.get_edit_text())
            self.new_note = False
            self._emit('added')

        elif key == 'ctrl n':
            try:
                self._w.base_widget.focus_position += 1
            except IndexError:
                pass

        elif key == 'ctrl p':
            try:
                self._w.base_widget.focus_position -= 1
            except IndexError:
                pass

        super(NoteEdit, self).keypress(size, key)
        return key


