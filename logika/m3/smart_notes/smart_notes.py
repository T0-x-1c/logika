from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QLabel,
    QListWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QInputDialog,
    QTableWidget,  QListWidgetItem, QFormLayout,
    QGroupBox, QButtonGroup, QRadioButton, QSpinBox, QMessageBox)


def save_all():
    with open('notes.json', 'w', encoding='utf-8') as file:
        json.dump(notes, file, ensure_ascii=False, sort_keys=True, indent=4)



app = QApplication([])
window = QWidget()
window.setWindowTitle("Розумні нотатки")
window.setWindowIcon(QIcon('pict/icon.png'))
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
btn_tags_del = QPushButton('Відкріпити тег')
btn_tags_search = QPushButton('Шукати за тегом')
btn_setting = QPushButton('⚙️')
btn_setting.setMinimumSize(30,30)
btn_txt_save = QPushButton('Зберегти в .txt')
btn_hide = QPushButton('>')
btn_hide.setMinimumSize(15,15)
btn_hide.setSizePolicy(1,1)

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
    else:
        show_window.setVisible(True)


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

Black = (80,80,80)

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


# def hide_col2():
#     hide_window.setVisible(False)
#
# def show_col2():
#

def save_txt():
    pass


def transparency_window(transparency_func):
    window.setWindowOpacity(transparency_func/10)
    setting_window.setWindowOpacity(transparency_func/10)

def window_theme_dark():
    window.setStyleSheet(f'''
                        background-color: rgb(80,80,80);
                        ''')

def window_theme_white():
    window.setStyleSheet(None)

def save_txt():
    key = lst_note.currentItem().text()

    name_txt = key
    text_txt = notes[key]['текст']

    with open(f'{name_txt}.txt', 'x', encoding='utf-8') as txt_file:
        txt_file.write(f"      Name:\n    ***{name_txt}***")
        txt_file.write(text_txt)


setting_window = QWidget()
setting_window.setWindowIcon(QIcon('pict/Settings_icon'))

def setting_open():
    setting_window.setFixedSize(490, 170)
    setting_window.setWindowTitle("Налаштування")

    setting_osn_layout = QHBoxLayout()

    setting_row1 = QVBoxLayout()
    setting_row2 = QVBoxLayout()
    setting_row3 = QVBoxLayout()

    setting_col1 = QVBoxLayout()
    setting_col2 = QVBoxLayout()
    setting_col3 = QVBoxLayout()
    setting_col4 = QVBoxLayout()

    setting_transparency_lb = QLabel('прозорість вікна')
    setting_transparency_spin = QSpinBox(value = 10)

    setting_transparency_spin.setMinimum(0)
    setting_transparency_spin.setMaximum(10)

    setting_dark_theme = QRadioButton('Ввімкнути темну тему')
    setting_bright_theme = QRadioButton('Ввімкнути світлу тему')
    setting_bright_theme.setChecked(True)

    setting_soon_to_be_1 = QRadioButton('Скоро...')
    setting_soon_to_be_2 = QRadioButton('Скоро...')

    setting_save_path = QLineEdit()
    setting_save_path.setPlaceholderText('Введіть шлях для збереження')

    setting_btn_save_path = QPushButton('Зберегти шлях')

    setting_btn_save_transparency = QPushButton('Зберегти непрозорість')
    setting_btn_save = QPushButton('Зберегти налаштування')


    setting_col1.addWidget(setting_transparency_lb)
    setting_col1.addWidget(setting_transparency_spin)

    setting_col2.addWidget(setting_btn_save_transparency)

    setting_row2.addWidget(setting_dark_theme)
    setting_row2.addWidget(setting_bright_theme)
    setting_row2.addWidget(setting_soon_to_be_1)
    setting_row2.addWidget(setting_soon_to_be_2)

    setting_col3.addWidget(setting_save_path)
    setting_col3.addWidget(setting_btn_save_path)

    setting_col4.addWidget(setting_btn_save)


    setting_osn_layout.addLayout(setting_row1)
    setting_osn_layout.addLayout(setting_row2)
    setting_osn_layout.addLayout(setting_row3)

    setting_row1.addLayout(setting_col1)
    setting_row1.addLayout(setting_col2)

    setting_row3.addLayout(setting_col3)
    setting_row3.addLayout(setting_col4)



    setting_btn_save_transparency.clicked.connect(lambda: transparency_window(setting_transparency_spin.value()))

    setting_dark_theme.clicked.connect(window_theme_dark)
    setting_bright_theme.clicked.connect(window_theme_white)

    # setting_btn_save.clicked.connect(save_setting)

    setting_window.setLayout(setting_osn_layout)
    setting_window.show()


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

with open('notes.json', 'r', encoding='utf-8') as file:
    notes = json.load(file)

lst_note.addItems(notes)

window.setLayout(osn_layout)

window.show()

sys.exit(app.exec_())
