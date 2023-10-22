from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QLabel,
    QListWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QInputDialog,
    QTableWidget, QListWidgetItem, QFormLayout,
    QGroupBox, QButtonGroup, QRadioButton, QSpinBox, QMessageBox, QColorDialog)


def save_all():
    with open('notes.json', 'w', encoding='utf-8') as file:
        json.dump(notes, file, ensure_ascii=False, sort_keys=True, indent=4)


with open('settings.json', 'r', encoding='utf-8') as set_file:
    settings = json.load(set_file)

app = QApplication([])
window = QWidget()

from setting_function import *

window.resize(800, 600)
window.setWindowIcon(QIcon('pict/icon.png'))
window.setWindowTitle("Розумні нотатки")

field_text = QTextEdit()
lb_notes = QLabel('Список заміток')
lst_note = QListWidget()

lb_tags = QLabel('Список тегів')

lst_tags = QListWidget()

field_tags = QLineEdit()
field_tags.setPlaceholderText('Введіть тег')

osn_layout = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col3 = QVBoxLayout()
row1 = QHBoxLayout()
row2 = QHBoxLayout()
row3 = QHBoxLayout()

hide_window = QWidget()
show_window = QWidget()

show_window.setLayout(col2)


def show_col2():
    if show_window.isVisible():
        show_window.setVisible(False)
        btn_hide.setText('<')
    else:
        show_window.setVisible(True)
        btn_hide.setText('>')


osn_layout.addLayout(col1, stretch=100)
osn_layout.addLayout(col3, stretch=1)
osn_layout.addWidget(show_window, stretch=50)

col1.addWidget(field_text)

row1.addWidget(btn_note_create)
row1.addWidget(btn_note_del)

row2.addWidget(btn_tags_add)
row2.addWidget(btn_tags_del)

row3.addWidget(lb_notes, stretch=9)
row3.addWidget(btn_setting, stretch=1)

col2.addLayout(row3)
col2.addWidget(lst_note)
col2.addLayout(row1)
col2.addWidget(btn_note_save)

col2.addWidget(lb_tags)
col2.addWidget(lst_tags)
col2.addWidget(field_tags)
col2.addLayout(row2)
col2.addWidget(btn_tags_search)
col2.addWidget(btn_txt_save)

col3.addWidget(btn_hide)

'''colors'''

Black = (80, 80, 80)


def show_notes():
    key = lst_note.currentItem().text()
    field_text.setText(notes[key]['текст'])

    lst_tags.clear()
    lst_tags.addItems(notes[key]['теги'])


def create_notes():
    note_name, ok = QInputDialog.getText(window, "додати замітку", "назва замітки")
    if note_name and ok:
        lst_note.addItem(note_name)
        notes[note_name] = {"текст": "", "теги": []}

        save_all()


def del_note():
    if lst_note.currentItem():
        key = lst_note.currentItem().text()
        del notes[key]

        field_text.clear()
        lst_tags.clear()
        lst_note.clear()

        lst_note.addItems(notes)

        save_all()


def save_notes():
    if lst_note.currentItem():
        key = lst_note.currentItem().text()
        notes[key]['текст'] = field_text.toPlainText()

        save_all()


def create_tags():
    if lst_note.currentItem() and field_tags.text() != '':
        key = lst_note.currentItem().text()
        tags_lst_func = []
        tags_lst_func.append(field_tags.text())

        notes[key]['теги'] += tags_lst_func

        lst_tags.clear()
        field_tags.clear()
        lst_tags.addItems(notes[key]['теги'])

        save_all()


def del_tags():
    if lst_tags.currentItem():
        key = lst_note.currentItem().text()
        select_tag = lst_tags.currentItem().text()

        notes[key]['теги'].remove(select_tag)

        lst_tags.clear()
        lst_tags.addItems(notes[key]['теги'])
        save_all()


def search_note_by_tag():
    if btn_tags_search.text() == 'Скинути пошук':
        lst_note.clear()
        lst_note.addItems(notes)
        field_tags.clear()

        btn_tags_search.setText('Шукати за тегом')


    else:
        if field_tags.text() != '':
            field_text.clear()
            lst_tags.clear()

            search_teg = field_tags.text()
            found_notes = []

            for notes_with_tag, all_notes in notes.items():
                if search_teg in all_notes['теги']:
                    found_notes.append(notes_with_tag)

            lst_note.clear()
            lst_note.addItems(found_notes)

            btn_tags_search.setText('Скинути пошук')


def setting_open():
    setting_window.show()


def save_txt():
    if lst_note.currentItem():
        key = lst_note.currentItem().text()

        name_txt = key
        text_txt = notes[key]['текст']

        with open(f'{settings["save_path"]}/{name_txt}.txt', 'x', encoding='utf-8') as txt_file:
            txt_file.write(f"        Name:\n    >>>{name_txt}<<<\n\n        Text:\n")
            txt_file.write(text_txt)


lst_note.itemClicked.connect(show_notes)

btn_note_create.clicked.connect(create_notes)
btn_note_save.clicked.connect(save_notes)
btn_note_del.clicked.connect(del_note)

btn_tags_add.clicked.connect(create_tags)
btn_tags_del.clicked.connect(del_tags)
btn_tags_search.clicked.connect(search_note_by_tag)

btn_setting.clicked.connect(setting_open)
btn_txt_save.clicked.connect(save_txt)
btn_hide.clicked.connect(show_col2)

all_button = [btn_hide, btn_setting, btn_tags_search, btn_tags_del, btn_tags_add, btn_txt_save, btn_note_create,
              btn_note_del, btn_note_save,
              setting_btn_palette, setting_btn_save_path, setting_btn_save_transparency]

with open('notes.json', 'r', encoding='utf-8') as file:
    notes = json.load(file)

lst_note.addItems(notes)

'''загрузка файлів налаштувань'''
if settings["window_theme_dark"]:
    setting_dark_theme.setChecked(True)
    window_theme_dark()

if settings["window_theme_white"]:
    setting_white_theme.setChecked(True)
    window_theme_white()

if settings["window_theme_rbg"]:
    setting_rgb_theme.setChecked(True)
    last_rgb_color()

if settings["window_theme_hex"]:
    setting_hex_theme.setChecked(True)
    last_hex_color()

if settings["color_palette"]:
    settingrb_palette.setChecked(True)
    last_palette_color()

transparency_window(setting_spin_transparency.value())

window.setLayout(osn_layout)

window.show()
sys.exit(app.exec_())
