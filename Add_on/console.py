""" Console
Interactive console widget.  Use to add an interactive python interpreter
in a GUI application.
"""

import sys
import code
import re
from typing import Dict, Callable
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
import PySide2.QtGui as QtGui
from contextlib import redirect_stdout, redirect_stderr


def console(screen_width, screen_height):
    def execute(line):
        pass

    scroll = QScrollArea()

    mainwidget = QWidget()
    scroll.setWidget(mainwidget)
    mainwidget.setStyleSheet('background-color:black;')
    layout = QVBoxLayout()
    layout.addWidget(scroll)
    scroll.setWidgetResizable(True)

    formlayout = QFormLayout(mainwidget)
    #mainwidget.setLayout(formlayout)
    console = QLineEdit()
    console.setFrame(False)
    line = 1
    console.returnPressed.connect(lambda :execute(0))
    #console.grabMouse()
    #console.setCursorWidth(10)
    console.setStyleSheet('background-color:black; color:white;')
    console.setFont(QtGui.QFont('Lucida Sans Typewriter', 10))
    label = QLabel('>>')
    label.setStyleSheet('color:white;')
    formlayout.addRow(label,console)
    return layout