#!/usr/bin/env python2.7

def __import_gui_widget():
    from modules import gui
    gui.show_gui()


if __name__ == "__main__":
    print "running"
    __import_gui_widget()