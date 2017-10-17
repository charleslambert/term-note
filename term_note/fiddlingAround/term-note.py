#!/usr/bin/env python
import subprocess
import tempfile
import click
import sqlite3
from npyscreen import *

@click.command()
@click.option('--editor', default="nvim")
def main(editor):
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        try:
            subprocess.call([editor, tf.name])
        except FileNotFoundError:
            print("ERROR: Editor Command Not Found")
            quit()

        con = sqlite3.connect("term_note.db")
        con.execute(
            "create table if not exists note (id integer primary key, text  varchar)"
        )

        with con:
            con.execute("insert into note(text) values (?)", (tf.read(), ))

        with con:
            f = con.execute("select * from note")
            print(list(map(lambda x: x[1].decode("utf-8"), f.fetchall())))
    MyForm = Form()


    usrn_box = MyForm.add_widget(TitleText, name="Your name:")
    internet = MyForm.add_widget(TitleText, name="Your favourite internet page:")

    MyForm.edit()
if __name__ == '__main__':
    main()
