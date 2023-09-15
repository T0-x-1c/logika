from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QRadioButton

app = QApplication([])
window = QWidget()

text = QLabel('2+2*2')

btn1 = QRadioButton('8')
btn2 = QRadioButton('6')
btn3 = QRadioButton('3')
btn4 = QRadioButton('10')

vline = QVBoxLayout()
hline1 = QVBoxLayout()
hline2 = QVBoxLayout()
hline3 = QVBoxLayout()

hline1.addWidget(text)

hline2.addWidget(btn1)
hline2.addWidget(btn2)

hline3.addWidget(btn3)
hline3.addWidget(btn4)

vline.addLayout(hline1)
vline.addLayout(hline2)
vline.addLayout(hline3)

window.setLayout(vline)

window.show()
app.exec_()