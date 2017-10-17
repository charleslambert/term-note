#!/usr/bin/python3
import urwid

class noteList(urwid.SimpleFocusListWalker):


list = []
for i in range(20):

    line = urwid.SelectableIcon(u"Hello World {}".format(i), cursor_position=0)
    line = urwid.AttrMap(line, "white")
    line = urwid.LineBox(line, title="Title")
    line = urwid.AttrMap(line, "white", focus_map="light red ochre")
    list.append(line)
walker = urwid.SimpleFocusListWalker(list)
list_box = urwid.ListBox(walker)
list_box = urwid.AttrMap(list_box, "gunmetal")
header = urwid.Text(u"Header")
footer = urwid.Text(u"Rx")
frame1 = urwid.Frame(list_box, header, footer)
placeh = urwid.WidgetPlaceholder(frame1)


def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    elif key in ('r', 'R'):
        placeh.original_widget = urwid.Filler(
            urwid.Text(u"It is alive!!!"), 'top')
    elif key in ('w', 'W'):
        placeh.original_widget = frame1


loop = urwid.MainLoop(
    placeh,
    palette=[('light red ochre', '', '', '', 'h209',
              'h236'), ('white', 'white', '', '', '',
                        'h236'), ('black coral', '', '', '', 'h60', 'h236'),
             ('silver', '', '', '', 'h7', 'h236'), ('gunmetal', '', '', '',
                                                    'h236', 'h236')],
    unhandled_input=exit_on_q)
loop.screen.set_terminal_properties(colors=256)
loop.run()
