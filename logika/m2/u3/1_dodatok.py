from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from random import randint

app = QApplication([])
window = QWidget()
window.resize(450,200)

text = QLabel('натисни на кнопку, щоб згенерувати число')

winer_text = QLabel('?')

button_random = QPushButton('Згенерувати')

line = QVBoxLayout()
line.addWidget(text, alignment=Qt.AlignCenter)
line.addWidget(winer_text, alignment=Qt.AlignCenter)
line.addWidget(button_random, alignment=Qt.AlignCenter)

def random_num():
    rand = randint(1, 100)
    winer_text.setText(str(rand))

button_random.clicked.connect(random_num)

window.setLayout(line)

window.show()
app.exec_()