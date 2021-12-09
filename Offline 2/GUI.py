from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QGridLayout, QWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QPoint, QSize
import sys

class DrawCircle(QWidget):
    def __init__(self, color, parent=None):
        QWidget.__init__(self, parent)
        self.color = color

    def setColor(self,color):
        self.color = color
        self.update()

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        # painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.setBrush(QBrush(Qt.green, Qt.DiagCrossPattern))

        painter.drawRect(100, 0, 500,200)
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        
        painter.drawEllipse((100, 100), 10, 10)

        # painter = QPainter(self)
        # painter.setRenderHint(QPainter.Antialiasing)
        # radx = 5
        # rady = radx
        # if self.color in ('red', 'green'):
        #     col = QColor(self.color)
        #     painter.setPen(col)
        #     painter.setBrush(col)
        # k = int(radx * 1.5)
        # center = QPoint(k,k)
        # painter.drawEllipse(center,radx,rady)

    def sizeHint(self):
        return QSize(15, 15)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Mancalaaaaaaaaa"
        self.top = 200
        self.left = 200
        self.width = 720
        self.height = 480

        label1 = QLabel("Player 1")
        label1.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        label1.setFont(QFont('Arial', 16))
        self.layout = QGridLayout()
        self.layout.addWidget(label1, 0, 0, 1, 1) # fromRow, fromColumn, rowSpan, colSpan
        board = DrawCircle('green')
        self.layout.addWidget(board, 1, 0, 2, 1)
        label1 = QLabel("Player 2")
        label1.setFont(QFont('Arial', 16))
        label1.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.layout.addWidget(label1, 2, 0, 1, 1)
        self.InitWindow()


    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setLayout(self.layout)
        self.show()


    def get_painter(self):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        # painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.setBrush(QBrush(Qt.green, Qt.DiagCrossPattern))

        painter.drawRect(100, 15, 400,200)
        return painter





    
if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())