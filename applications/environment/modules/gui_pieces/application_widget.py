#!/usr/bin/env python2.7

try:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *


class ApplicationButton(QWidget):
    def __init__(self, applications=[]):
        super(ApplicationButton, self).__init__()
        self.grid = QGridLayout()
        self.grid.addWidget(self.__build_button())
        self.setLayout(self.grid)

    def __build_button(self):
        _path = r"C:/Users/Darren/development/open-pipeline/data/icons/maya.png"
        img = QImage(r"C:/Users/Darren/development/open-pipeline/data/icons/maya.png")
        # pixmap = QPixmap(img.scaledToWidth(100))
        pixmap = QPixmap(_path).scaled(100, 100, transformMode=Qt.SmoothTransformation)
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        return lbl






# def makeClickable(widget):
#     def SendClickSignal(widget, evnt):
#         widget.emit(SIGNAL('clicked()'))
#     widget.mousePressEvent = lambda evnt: SendClickSignal(widget, evnt)