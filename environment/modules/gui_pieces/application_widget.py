#!/usr/bin/env python2.7
import os

try:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *


ROOT_DIR = os.path.abspath(os.path.join(__file__ , "../../../")).replace(os.sep, "/")
print ROOT_DIR


class ApplicationButton(QWidget):
    def __init__(self, applications=[]):
        super(ApplicationButton, self).__init__()
        self.grid = QGridLayout()
        for app in applications:
            self.grid.addWidget(self.__build_button(application_name=app))
        self.setLayout(self.grid)

    def __build_button(self, application_name):
        _path = os.path.join(ROOT_DIR, "source/icons/{appname}.png".format(appname=application_name))
        img = QImage(_path)
        pixmap = QPixmap(_path).scaled(128, 128, transformMode=Qt.SmoothTransformation)
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        return lbl






# def makeClickable(widget):
#     def SendClickSignal(widget, evnt):
#         widget.emit(SIGNAL('clicked()'))
#     widget.mousePressEvent = lambda evnt: SendClickSignal(widget, evnt)