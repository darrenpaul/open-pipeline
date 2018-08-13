#!/usr/bin/env python2.7

import os
import re
import sys
import glob
from pprint import pprint
try:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *

from gui_pieces import application_widget

# ROOTDIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(ROOTDIR.replace("{sep}GuiEnvironment".format(sep=os.sep), ""))


class GuiEnvironment(QMainWindow):
    def __init__(self, parent=None):
        super(GuiEnvironment, self).__init__(parent)
        self.__build_ui()
        self.__style_interface()
        self.windowPostion = self.pos()

        widgets = application_widget.ApplicationButton(applications=["maya", "houdini"])
        self.setCentralWidget(widgets)

    def __build_ui(self):
        self.__build_windows()

    def __build_windows(self):
        self.setWindowTitle("GuiEnvironment")
        self.setFixedSize(300, 600)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        QApplication.setGraphicsSystem('native')
        QApplication.setStyle(QStyleFactory.create("plastique"))

    def __build_widgets(self):
        self.widgets = Widgets()
        self.setCentralWidget(self.widgets)

    def __style_interface(self):
        QApplication.setStyle(QStyleFactory.create('plastique'))
        self.setStyleSheet("background-color:#263238; color:#ececec;")

    def mousePressEvent(self, event):
        self.windowPostion = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.windowPostion)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.windowPostion = event.globalPos()


def show_gui():
    app = QApplication([])
    window = GuiEnvironment()
    window.show()
    sys.exit(app.exec_())
