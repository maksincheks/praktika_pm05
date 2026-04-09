import random
import os
from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon


class CaptchaPuzzle(QWidget):
    def __init__(self):
        super().__init__()
        self.order = [0, 1, 2, 3]
        self.correct = [0, 1, 2, 3]
        self.selected = -1
        self.pixmaps = []
        self.buttons = []
        self.init_ui()

    def init_ui(self):
        for i in range(1, 5):
            filename = os.path.join("images", f"{i}.png")
            pixmap = QPixmap(filename)
            self.pixmaps.append(pixmap)

        btn1 = QPushButton(self)
        btn1.setGeometry(130, 0, 100, 100)
        btn1.setStyleSheet("border: none; padding: 0; margin: 0;")
        btn1.clicked.connect(lambda: self.on_click(0))

        btn2 = QPushButton(self)
        btn2.setGeometry(235, 0, 100, 100)
        btn2.setStyleSheet("border: none; padding: 0; margin: 0;")
        btn2.clicked.connect(lambda: self.on_click(1))

        btn3 = QPushButton(self)
        btn3.setGeometry(130, 100, 100, 100)
        btn3.setStyleSheet("border: none; padding: 0; margin: 0;")
        btn3.clicked.connect(lambda: self.on_click(2))

        btn4 = QPushButton(self)
        btn4.setGeometry(235, 100, 100, 100)
        btn4.setStyleSheet("border: none; padding: 0; margin: 0;")
        btn4.clicked.connect(lambda: self.on_click(3))

        self.buttons = [btn1, btn2, btn3, btn4]

        self.setFixedSize(450, 250)
        self.shuffle()

    def update_display(self):
        for i, btn in enumerate(self.buttons):
            idx = self.order[i]
            btn.setIcon(QIcon(self.pixmaps[idx]))
            btn.setIconSize(btn.size())
            if self.selected == i:
                btn.setStyleSheet("border: 3px solid green; padding: 0; margin: 0;")
            else:
                btn.setStyleSheet("border: none; padding: 0; margin: 0;")

    def on_click(self, idx):
        if self.selected == -1:
            self.selected = idx
            self.update_display()
        else:
            if self.selected != idx:
                self.order[self.selected], self.order[idx] = self.order[idx], self.order[self.selected]
            self.selected = -1
            self.update_display()

    def shuffle(self):
        random.shuffle(self.order)
        self.selected = -1
        self.update_display()

    def is_solved(self):
        return self.order == self.correct

    def reset(self):
        self.shuffle()
