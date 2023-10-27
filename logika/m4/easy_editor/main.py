# потрібна константа Qt.KeepAspectRatio для зміни розмірів із збереженням пропорцій
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap  # оптимізована для показу на екрані картинка
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFileDialog, QLabel,
    QPushButton, QListWidget, QHBoxLayout, QVBoxLayout
)

from PIL import Image, ImageFilter
# from PIL.ImageQt import ImageQt  # Для перенесення графіки з Pillow до QT
# from PIL.ImageFilter import SHARPEN

app = QApplication([])
window = QWidget()

window.resize(700,500)
window.setStyleSheet('''
    background-color: rgb(227,243,243)
    ''')

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
    QPushButton {
        background-color: rgb(214,255,255);
        border: 3px solid rgb(153,255,255);
        border-radius:4px;
        }
    
    QPushButton:hover {
            color: yellow;
        }
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

def filter(files):
    result = []
    ext = ['jpg', 'jpeg', 'bmp', 'gif', 'jfif', 'svg', 'png']

    for file in files:
        if file.split('.')[-1] in ext:
            result.append(file)

    return result

def show_file():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
    #c:\sistr
    file_and_folders = os.listdir(workdir)
    #["gomer1.jpg", "gomer2.jpg"]
    filtered_img = (filter(file_and_folders))

    lst_folder.clear()
    lst_folder.addItems(filtered_img)

class ImageProcesor():
    def __init__(self):
        self.filename = None
        self.original = None
        self.save_dir = 'Modifiet/'

    def loadimage(self, fielname):
        self.filename = fielname

        full_path = os.path.join(workdir, fielname)
        self.original = Image.open(full_path)

    def show_image(self, path):
        lb_pict.hide()
        pixmapeimage = QPixmap(path)

        w,h = lb_pict.width(), lb_pict.height()

        pixmapeimage = pixmapeimage.scaled(w,h, Qt.KeepAspectRatio)

        lb_pict.setPixmap(pixmapeimage)
        lb_pict.show()

def showChosenImage():
    file_name = lst_folder.currentItem().text()
    work_img.loadimage(file_name)
    full_path = os.path.join(workdir, file_name)
    work_img.show_image(full_path)

work_img = ImageProcesor()

btn_folder.clicked.connect(show_file)
lst_folder.itemClicked.connect(showChosenImage)

window.setLayout(osn_layout)
window.show()
app.exec_()