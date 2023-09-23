from PyQt5.QtCore import Qt
import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QLabel,
    QListWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QInputDialog,
    QTableWidget,  QListWidgetItem, QFormLayout,
    QGroupBox, QButtonGroup, QRadioButton, QSpinBox, )


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
    key = lst_note.selectedItems()[0].text()
    field_text.setText(notes[key]['текст'])


def create_notes():
    notes_name, true = QInputDialog.getText(window, 'нотаток', 'Введіть назву нотатку:')
    if true:
        notes[notes_name] = {'текст': '', 'теги': []}
        lst_note.clear()
        lst_note.addItems(notes)

def save_notes():
    if lst_note.selectedItems():
        key = lst_note.currentItem().text()
        notes[key]['текст'] = field_text.toPlainText()

        with open('notes.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, ensure_ascii=False, indent=4)

def delete_note():
    if lst_note.selectedItems():
        selected_note = lst_note.currentItem().text()
        if selected_note in notes:
            del notes[selected_note]
            lst_note.takeItem(lst_note.currentRow())
            field_text.clear()
            lst_tags.clear()


        with open('notes.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, ensure_ascii=False, indent=4)

def show_tags():
    selected_items = lst_note.selectedItems()
    if selected_items:
        key = selected_items[0].text()
        tags = notes[key]['теги']
        lst_tags.clear()
        lst_tags.addItems(tags)


def create_tags():
    selected_items = lst_note.selectedItems()
    if selected_items:
        tags_text = fild_tags.text()
        key = lst_note.currentItem().text()
        if tags_text:
            tags_list = tags_text.split(',')
            tags_list = []
            tags_list.append(tags_text)
            if tags_list:
                notes[key]['теги'] = tags_list
                lst_tags.clear()  # Очищаємо список тегів
                lst_tags.addItems(tags_list)  # Додаємо нові теги
                fild_tags.clear()

    save_notes()

def unfasten_tags():
    select_tegs = lst_tags.selectedItems()
    select_note = lst_note.currentItem()
    key = select_note.text()
    if select_tegs:
        for tag in select_tegs:
            teg_text = tag.text()
            notes[key]['теги'].remove(teg_text)
            lst_tags.takeItem(lst_tags.row(tag))

    save_notes()

def search_notes():
    tags_text = fild_tags.text().strip()
    selected_tags = tags_text.split()

    found_notes = []

    for note_name, note_data in notes.items():
        note_tags = note_data.get('теги', [])
        if all(tag in note_tags for tag in selected_tags):
            found_notes.append(note_name)

    lst_note.clear()
    lst_note.addItems(found_notes)


lst_note.itemClicked.connect(show_notes)
lst_note.itemClicked.connect(show_tags)


btn_note_create.clicked.connect(create_notes)
btn_note_save.clicked.connect(save_notes)
btn_note_del.clicked.connect(delete_note)

btn_tags_add.clicked.connect(create_tags)
btn_tags_unfasten.clicked.connect(unfasten_tags)
btn_tags_search.clicked.connect(search_notes)

with open('notes.json', 'r', encoding='utf-8') as file:
    notes = json.load(file)


lst_note.addItems(notes)

window.setLayout(osn_layout)

window.show()
sys.exit(app.exec_())
