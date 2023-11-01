from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys
import json
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QInputDialog,
    QRadioButton, QSpinBox, QColorDialog)


'''btn'''
btn_pict_left = QPushButton('Ліво')
btn_pict_right = QPushButton('Право')
btn_mirror = QPushButton('Дзеркало')
btn_sharpness = QPushButton('Різкість')
btn_bw = QPushButton('Ч/Б')
btn_setting = QPushButton('⚙️')

'''Функції налаштувань'''

setting_window = QWidget()
window = QWidget()

with open('settings.json', 'r', encoding='utf-8') as set_file:
    settings = json.load(set_file)

def save_setting():
    with open('settings.json', 'w', encoding='utf-8') as set_file:
        json.dump(settings, set_file, ensure_ascii=False, sort_keys=True, indent=4)

def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i + 2], 16)
        rgb.append(decimal)

    return rgb

def transparency_window(transparency_func):
    settings["value"] = transparency_func
    window.setWindowOpacity(transparency_func/10)
    setting_window.setWindowOpacity(transparency_func/10)

    save_setting()

def window_theme_dark():
    window.setStyleSheet(f'''
                        background-color: rgb(111,111,111);
                        ''')
    setting_window.setStyleSheet(f'''
                        background-color: rgb(111,111,111);
                        ''')


    settings["window_theme_dark"] = True
    settings["window_theme_white"] = False
    settings["window_theme_rbg"] = False
    settings["window_theme_hex"] = False
    settings["color_palette"] = False
    save_setting()

def window_theme_white():
    window.setStyleSheet(None)
    setting_window.setStyleSheet(None)

    settings["window_theme_dark"] = False
    settings["window_theme_white"] = True
    settings["window_theme_rbg"] = False
    settings["window_theme_hex"] = False
    settings["color_palette"] = False


    save_setting()

def window_theme_rbg():
    rgb_color, ok = QInputDialog.getText(setting_window, 'Введіть RGB коляр', 'Введіть RGB коляр \n(xxx,xxx,xxx)')
    if ok:
        settings["last_rgb_color"] = rgb_color
        window.setStyleSheet(f'''
                                background-color: rgb({rgb_color});
                                ''')
        setting_window.setStyleSheet(f'''
                                background-color: rgb({rgb_color});
                                ''')

        rgb = rgb_color.split(',')
        rgb = [int(rgb[0]),int(rgb[1]),int(rgb[2])]

        settings["window_theme_dark"] = False
        settings["window_theme_white"] = False
        settings["window_theme_rbg"] = True
        settings["window_theme_hex"] = False
        settings["color_palette"] = False

        save_setting()

def last_rgb_color():
    window.setStyleSheet(f'''
                            background-color: rgb({settings["last_rgb_color"]});
                            ''')
    setting_window.setStyleSheet(f'''
                                    background-color: rgb({settings["last_rgb_color"]});
                                    ''')


def window_theme_standart():
    all_btn = [btn_pict_left, btn_pict_right, btn_mirror, btn_sharpness, btn_bw, btn_setting]

    for btn in all_btn:
        btn.setStyleSheet('''
        QPushButton {
            background-color: rgb(204,255,255);
            border: 3px solid rgb(153,255,255);
            border-radius:4px;
            }

        QPushButton:hover {
            background-color: rgb(224,255,255);
            border: 3px solid rgb(183,255,255);
            border-radius:4px;
            }

                            ''')

    window.setStyleSheet('''
        background-color: rgb(234,255,255)
        ''')

    setting_window.setStyleSheet(f'''
        background-color: rgb(234,255,255);
        ''')

    settings["window_theme_dark"] = False
    settings["window_theme_white"] = False
    settings["window_theme_rbg"] = False
    settings["window_theme_standart"] = True
    settings["color_palette"] = False

    save_setting()


def save_path():
    func_save_path = setting_save_path.text()
    print(func_save_path)
    settings["save_path"] = func_save_path

    save_setting()

'''Палітра кольорів'''

def open_color_palette():
    color = QColorDialog.getColor()
    if color.isValid():
        red = color.red()
        green = color.green()
        blue = color.blue()

        global last_palette_color

        last_palette_color = (f'{red},{green},{blue}')
        settings["last_palette_color"] = last_palette_color

        window.setStyleSheet(f'''
                                background-color: rgb({last_palette_color});
                                ''')
        setting_window.setStyleSheet(f'''
                                        background-color: rgb({last_palette_color});
                                        ''')
        rgb = [red,green,blue]

        settingrb_palette.setChecked(True)
        settingrb_palette.setText(last_palette_color)

        settings["window_theme_dark"] = False
        settings["window_theme_white"] = False
        settings["window_theme_rbg"] = False
        settings["window_theme_hex"] = False
        settings["color_palette"] = True
        settings["last_rgb_btn_color"] = rgb

        save_setting()


def last_palette_color():
    if last_palette_color != None:
        window.setStyleSheet(f'''
                                        background-color: rgb({settings["last_palette_color"]});
                                        ''')
        setting_window.setStyleSheet(f'''
                                        background-color: rgb({settings["last_palette_color"]});
                                        ''')

    rgb = settings["last_palette_color"]
    rgb = rgb.split(',')
    rgb = [int(rgb[0]), int(rgb[1]), int(rgb[2])]

    settings["window_theme_dark"] = False
    settings["window_theme_white"] = False
    settings["window_theme_rbg"] = False
    settings["window_theme_hex"] = False
    settings["color_palette"] = True
    settings["last_rgb_btn_color"] = rgb

    save_setting()



'''Налаштування'''

setting_window = QWidget()
setting_window.setWindowIcon(QIcon('pict/Settings_icon'))

setting_window.setFixedSize(590, 190)
setting_window.setWindowTitle("Налаштування")

setting_osn_layout = QHBoxLayout()

setting_row1 = QVBoxLayout()
setting_row2 = QVBoxLayout()
setting_row3 = QVBoxLayout()

setting_col1 = QVBoxLayout()
setting_col2 = QVBoxLayout()
setting_col3 = QVBoxLayout()
setting_col4 = QHBoxLayout()

setting_lb_transparency = QLabel('прозорість вікна')
setting_spin_transparency = QSpinBox(value = settings["value"])

setting_spin_transparency.setMinimum(0)
setting_spin_transparency.setMaximum(10)

setting_dark_theme = QRadioButton('Ввімкнути темну тему')
setting_white_theme = QRadioButton('Ввімкнути світлу тему')

setting_standart_theme = QRadioButton('Встановити все по замовчуваням')
setting_rgb_theme = QRadioButton('Змінити колір фону RGB')

settingrb_palette = QRadioButton()
setting_btn_palette = QPushButton('Відкрити палітру')

setting_save_path_lb = QLabel('Введіть шлях \nдля збереження зображень')

setting_save_path = QLineEdit()
setting_save_path.setPlaceholderText('Введіть шлях для збереження')
setting_save_path.setText(f'{settings["save_path"]}')

setting_btn_save_transparency = QPushButton('Зберегти непрозорість')
setting_btn_save_path = QPushButton('Зберегти шлях збереження')

setting_col1.addWidget(setting_lb_transparency)
setting_col1.addWidget(setting_spin_transparency)

setting_col2.addWidget(setting_btn_save_transparency)

setting_row2.addWidget(setting_dark_theme)
setting_row2.addWidget(setting_white_theme)
setting_row2.addWidget(setting_rgb_theme)
setting_row2.addWidget(setting_standart_theme)

setting_col4.addWidget(settingrb_palette)
setting_col4.addWidget(setting_btn_palette)
setting_row2.addLayout(setting_col4)


setting_col3.addWidget(setting_save_path_lb)
setting_col3.addWidget(setting_save_path)

setting_col3.addWidget(setting_btn_save_path)

setting_osn_layout.addLayout(setting_row1)
setting_osn_layout.addLayout(setting_row2)
setting_osn_layout.addLayout(setting_row3)

setting_row1.addLayout(setting_col1)
setting_row1.addLayout(setting_col2)

setting_row3.addLayout(setting_col3)


setting_btn_save_transparency.clicked.connect(lambda: transparency_window(setting_spin_transparency.value()))

setting_dark_theme.clicked.connect(window_theme_dark)
setting_white_theme.clicked.connect(window_theme_white)
setting_rgb_theme.clicked.connect(window_theme_rbg)
setting_standart_theme.clicked.connect(window_theme_standart)

settingrb_palette.clicked.connect(last_palette_color)
setting_btn_palette.clicked.connect(open_color_palette)

setting_btn_save_path.clicked.connect(save_path)

setting_window.setLayout(setting_osn_layout)