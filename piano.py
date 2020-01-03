from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QVBoxLayout, QAbstractButton, QLabel
import sys
from PyQt5.QtGui import QPainter, QColor, QKeySequence, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, QRectF
import pygame.mixer as mx


mx.init(44100, 16, 6)
notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
keys = [eval(f'Qt.Key_{i}') for i in '1Q2WE4R5T6YU8I9OP']
keys = [Qt.Key_Tab] + keys + [Qt.Key_Minus, Qt.Key_BracketLeft, Qt.Key_Equal, Qt.Key_BracketRight, Qt.Key_Backspace, Qt.Key_Backslash]
keys = list(map(lambda x: x.as_integer_ratio()[0], keys))
keys[0] = 96
keys_str = list('~1Q2WE4R5T6YU8I9OP-[=]\\')
keys_str.insert(-1, 'BS')


class Tile(QAbstractButton):
    def __init__(self, path, text):
        super().__init__()
        self.pnt = QPainter()
        self.pressed_ = False
        self.note = mx.Sound(path)
        self.name = path.rsplit('\\', maxsplit=1)[-1].rsplit('.', maxsplit=1)[0]
        self.black = 'b' in self.name
        self.label = QLabel(text)
        if self.black:
            p = self.label.palette()
            p.setBrush(QPalette.Active, QPalette.ButtonText, QBrush(QColor('white')))
            self.label.setPalette(p)
        vlo = QVBoxLayout(self)
        vlo.addSpacing(self.sizeHint().height() // 8 * 7)
        vlo.addWidget(self.label)
        self.pressed.connect(self.note.play)
        self.released.connect(self.note.stop)

    def paintEvent(self, event):
        self.pnt.begin(self)
        x, y = self.size().width(), self.size().height()
        if self.isDown() or self.pressed_:
            color = QColor('darkGray' if self.black else 'lightGray')
        else:
            color = QColor('black' if self.black else 'white')
        self.pnt.fillRect(0, 0, x, y, color)
        if not self.black:
            self.pnt.setBrush(QColor('black'))
            self.pnt.drawLine(0, 0, 0, y - 1)
            self.pnt.drawLine(0, y - 1, x - 1, y - 1)
            self.pnt.drawLine(x - 1, y - 1, x - 1, 0)
        self.pnt.end()
    
    def sizeHint(self):
        if self.black:
            return QSize(40, 200)
        return QSize(60, 300)

    def play(self):
        self.note.play()
        self.update()
    
    def stop(self):
        self.note.stop()
        self.update()

class Piano(QWidget):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Piano")
        self.setFixedSize(2 * 7 * 60 + 20, 310)
        self.setFocusPolicy(Qt.ClickFocus)
        x = 10
        i = 0
        for oct_ in range(3, 5):
            for name in notes:
                b = Tile(f'mf\\{name + str(oct_)}.wav', keys_str[i])
                i += 1
                b.setParent(self)
                b.move(x, 0)
                self.buttons.append(b)
                if b.black:
                    b.move(x - 20, 0)
                else:
                    b.lower()
                    x += 60
    
    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        try:
            b = self.buttons[keys.index(event.key())]
            b.pressed_ = True
            b.play()
        except:
            return

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
        try:
            b = self.buttons[keys.index(event.key())]
            b.pressed_ = False
            b.stop()
        except:
            return

app = QApplication(sys.argv)
ex = Piano()
ex.show()
sys.exit(app.exec_())