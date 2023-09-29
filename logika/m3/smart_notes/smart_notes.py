from PyQt5.QtCore import Qt
import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QLabel,
    QListWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QInputDialog,
    QTableWidget,  QListWidgetItem, QFormLayout,
    QGroupBox, QButtonGroup, QRadioButton, QSpinBox, )


def save_all():
    with open('notes.json', 'w', encoding='utf-8') as file:
        json.dump(notes, file, ensure_ascii=False, sort_keys=True, indent=4)

app = QApplication([])
window = QWidget()
window.resize(800,600)


field_text = QTextEdit()

lb_notes = QLabel('Список заміток')

lst_note = QListWidget()

btn_note_create = QPushButton('Створити замітку')
btn_note_save = QPushButton('Зберегти замітку')
btn_note_del = QPushButton('Видалити замітку')

lb_tags = QLabel('Список тегів')

lst_tags = QListWidget()

btn_tags_add = QPushButton('Додати тег')
btn_tags_unfasten = QPushButton('Відкріпити тег')
btn_tags_search = QPushButton('Шукати за тегом')

fild_tags = QLineEdit()
fild_tags.setPlaceholderText('Введіть тег')

osn_layout = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
row1 = QHBoxLayout()
row2 = QHBoxLayout()


osn_layout.addLayout(col1, stretch=2)
osn_layout.addLayout(col2, stretch=1)

col1.addWidget(field_text)


row1.addWidget(btn_note_create)
row1.addWidget(btn_note_del)

row2.addWidget(btn_tags_add)
row2.addWidget(btn_tags_unfasten)


col2.addWidget(lb_notes)
col2.addWidget(lst_note)
col2.addLayout(row1)
col2.addWidget(btn_note_save)


col2.addWidget(lb_tags)
col2.addWidget(lst_tags)
col2.addWidget(fild_tags)
col2.addLayout(row2)
col2.addWidget(btn_tags_search)



def show_notes():
    key = lst_note.currentItem().text()
    field_text.setText(notes[key]['текст'])

    lst_tags.clear()
    lst_tags.addItems(notes[key]['теги'])


def create_notes():
    note_name, ok = QInputDialog.getText(window, "додати замітку", "назва замітки")
    if note_name and ok:
        lst_note.addItem(note_name)
        notes[note_name] = {"текст" : "", "теги" : []}

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
    key = lst_note.currentItem().text()
    notes[key]['текст'] = field_text.toPlainText()
    
    save_all()


lst_note.itemClicked.connect(show_notes)

btn_note_create.clicked.connect(create_notes)
btn_note_save.clicked.connect(save_notes)
btn_note_del.clicked.connect(del_note)
#
# btn_tags_add.clicked.connect(create_tags)
# btn_tags_unfasten.clicked.connect(unfasten_tags)
# btn_tags_search.clicked.connect(search_notes)

with open('notes.json', 'r', encoding='utf-8') as file:
    notes = json.load(file)


lst_note.addItems(notes)

window.setLayout(osn_layout)

window.show()
sys.exit(app.exec_())
