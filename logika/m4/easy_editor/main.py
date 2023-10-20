# потрібна константа Qt.KeepAspectRatio для зміни розмірів із збереженням пропорцій
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap  # оптимізована для показу на екрані картинка
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFileDialog, QLabel,
    QPushButton, QListWidget, QHBoxLayout, QVBoxLayout
)

# from PIL import Image, ImageFilter
# from PIL.ImageQt import ImageQt  # Для перенесення графіки з Pillow до QT
# from PIL.ImageFilter import SHARPEN

app = QApplication([])
window = QWidget()

window.resize(700,500)

col1 = QVBoxLayout()
col2 = QHBoxLayout()
col3 = QVBoxLayout()
osn_layout = QHBoxLayout()

btn_folder = QPushButton('Папка')
btn_folder.setStyleSheet('''
    background-color: rgb(242,224,224);
    border: 3px solid rgb(255,102,102);
    border-radius:4px;
                            ''')
lst_folder = QListWidget()

lb_pict = QLabel('Картинка')

btn_pict_left = QPushButton('Ліво')
btn_pict_right = QPushButton('Право')
btn_mirror = QPushButton('Дзеркало')
btn_sharpness = QPushButton('Різкість')
btn_bw = QPushButton('Ч/Б')

all_btn = [btn_pict_left, btn_pict_right, btn_mirror, btn_sharpness, btn_bw]

for btn in all_btn:
    btn.setStyleSheet('''
    background-color: rgb(214,255,255);
    border: 3px solid rgb(153,255,255);
    border-radius:4px;
                        ''')

col1.addWidget(btn_folder)
col1.addWidget(lst_folder)

col2.addWidget(btn_pict_left)
col2.addWidget(btn_pict_right)
col2.addWidget(btn_mirror)
col2.addWidget(btn_sharpness)
col2.addWidget(btn_bw)

col3.addWidget(lb_pict)
col3.addLayout(col2)

osn_layout.addLayout(col1, stretch=2)
osn_layout.addLayout(col3, stretch=6)


workdir = QFileDialog.getExistingDirectory()
file_and_folders = os.listdir(workdir)
print(file_and_folders)

def filter(files):
    result = []
    ext = ['jpg', 'jpeg', 'bmp', 'gif', 'jfif', 'svg', 'png']

    for file in files:
        if file.split('.')[-1] in ext:
            result.append(file)

    return result

lst_folder.addItems(filter(file_and_folders))


window.setLayout(osn_layout)
window.show()
app.exec_()