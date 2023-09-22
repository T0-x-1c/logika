from PyQt5.QtCore import Qt
import  json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QLabel,
    QListWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QInputDialog,
    QTableWidget,  QListWidgetItem, QFormLayout,
    QGroupBox, QButtonGroup, QRadioButton, QSpinBox)


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

col2.addLayout(row1)

col2.addWidget(lb_tags)
col2.addWidget(lst_tags)
col2.addLayout(row2)
col2.addWidget(btn_tags_search)

col2.addLayout(row2)

def show_notes():
    key = lst_note.selectedItems()[0].text()
    field_text.setText(notes[key]['текст'])


lst_note.itemClicked.connect(show_notes)


with open('notes.json', 'r', encoding='utf-8') as file:
    notes = json.load(file)


lst_note.addItems(notes)


window.setLayout(osn_layout)

window.show()
app.exec_()
