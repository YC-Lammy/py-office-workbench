from PySide2.QtWidgets import *
from PySide2.QtCore import QCoreApplication
from PySide2.QtGui import *
def scientific_calculator(screen_width, screen_height):
    from Add_on.scientific_calculator import constants
    import decimal
    import math

    resultPI = {'pi':''}

    class compute_pi:
        def __init__(self, ditgits=1000):
            if len(piTabdigits.text())>=1:
                try:
                    self.digit = int(piTabdigits.text())
                except:
                    self.digit = ditgits
            else:
                self.digit = ditgits


        def compute(self,algorithm = 'Chudnovsky'):
            if algorithm =='Chudnovsky':
                self.chudnovsky()
            elif algorithm == 'Machin':
                self.machin()


        def machin(self,digits = 0):
            from decimal import Decimal, getcontext
            # arccot function using power formula arccot = 1/x - 1/(3x^3) + 1/(5x^5) ...
            if digits==0:
                digits = self.digit

            def arccot(x, digits):
                # set precision and starting values
                getcontext().prec = digits
                total = 0
                n = 1
                # loop while new term is large enough to actually change the total
                while Decimal((2 * n - 1) * x ** (2 * n - 1)) < Decimal(10 ** digits):
                    # find value of new term
                    term = ((-1) ** (n - 1)) * 1 / Decimal((2 * n - 1) * x ** (2 * n - 1))
                    total += term  # add the new term to the total
                    n += 1  # next n
                return total
            decimals = digits
            # find pi using Machin's Formula pi = 4 * (4 * arccot(5) - arccot(239))
            pi = str(Decimal(4 * (4 * arccot(5, decimals + 3) - arccot(239, decimals + 3))).quantize(
                Decimal(10) ** (-decimals)))
            edit.append(pi)
            resultPI['pi'] = pi

        def chudnovsky(self,digits=0):
            import subprocess
            import pathlib
            from platform import system
            from os import listdir

            sys_name = system()

            compiled = False
            if sys_name != 'Windows':
                for i in listdir():
                    if 'gmp-chudnovsky' in i and i != 'gmp-chudnovsky.c':
                        compiled = True
                        break
            compiled = True # remove it if not using linux

            if compiled==False:
                try:
                    p = subprocess.Popen(['gcc', '-s', '-Wall', '-o', 'gmp-chudnovsky', 'gmp-chudnovsky.c', '-lgmp', '-lm'],
                                     stdout=subprocess.PIPE,stdin=subprocess.PIPE)
                    out , err = p.communicate()
                    print(out)
                    print(err)
                except Exception as e:
                    QMessageBox(text=e).exec_()

            if digits==0:
                digits = self.digit
            path = pathlib.Path().absolute()
            if sys_name == 'Linux' or sys_name == 'Darwin':
                p = subprocess.Popen(['Add_on/scientific_calculator/gmp-chudnovsky', str(digits), '1'], stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE, cwd=path)
            elif sys_name == 'Windows':
                p = subprocess.Popen(['gmp-chudnovsky.exe', str(digits), '1'], stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE, cwd=path)

            out, err = p.communicate()
            pi = out.decode()
            if self.digit>10000:
                edit.append('result too large\nyou can choose to save into file\n')
            else:
                edit.append(pi+'\n')
            resultPI['pi'] = pi

        def savePI(self):
            dir,filter = QFileDialog().getSaveFileName()
            with open(dir, 'w') as o:
                o.write(resultPI['pi'])
                o.close()

    def key_handler(key):
        funcs = ['sin','cos','tan','sinh','cosh','tanh','Deg','Rad','Grad']
        back = False
        if key =='del': key=''
        elif key == '÷': key = '/'
        elif any(x in key for x in funcs):
            key +='()'
            back = True
        line.insert(key)
        if back:
            line.cursorBackward(False,1)

    def execute():
        def print(text):
            edit.append(str(text)+'\n')

        def gradFromRad(rad):
            return 200 * rad / math.pi

        def radFromGrad(grad):
            return math.pi * grad / 200

        text = line.text()
        text = text.replace('x','*')\
            .replace('^','**')\
            .replace('^','**')\
            .replace('ans',str(ans['ans']))
        cos = math.cos
        sin = math.sin
        tan = math.tan
        log = math.log
        floor = math.floor
        e = math.e
        pi = math.pi
        Rad = math.radians
        Deg = math.degrees
        #decimal.getcontext().prec = 1000
        try:
            ans['ans'] = eval(text)
            if len(str(ans['ans']))>15:
                ans['ans'] = '%e'%decimal.Decimal(ans['ans'])
            print(ans['ans'])
        except Exception as e:
            print(str(e))
            print(text)

    ans = {'ans':''}
    layout = QVBoxLayout()
    layout.setMargin(0)
    edit = QTextEdit()
    edit.setMaximumHeight(screen_height/3)
    edit.setAlignment(Qt.AlignRight)
    edit.setFont(QFont("Sans Bold", 15))
    line = QLineEdit()
    line.setFont(QFont("Sans Bold", 15))
    line.setMinimumHeight(screen_height/16)
    line.returnPressed.connect(execute)
    tab = QTabWidget()
    layout.addWidget(edit)
    layout.addWidget(line)
    layout.addWidget(tab)

    ########################## main keyboard layout ##############################
    main_keyboard_widget = QWidget()
    main_keyboard_layout = QGridLayout()
    main_keyboard_widget.setLayout(main_keyboard_layout)
    mainKeyboardLayout = [
        ['C','%','del','ans','undo','^','sin','cos','tan']
        ,['7','8','9','÷','(',')','sinh','cosh','tanh']
        ,['4','5','6','x','^2','sqr','Deg','Rad','Grad']
        ,['2','3','4','+']
        ,['0','.','i','-','=']]
    def setupkeyboard():
        def add_but(x): # make sure variable x does not over write by passing it as arg
            but = QPushButton(x)
            but.setMinimumHeight(40)
            but.clicked.connect(lambda: key_handler(x))
            main_keyboard_layout.addWidget(but, row, column) # follow the grid layout
        row = 0
        column = 0
        for i in mainKeyboardLayout:
            for x in i :
                add_but(x) # pass in x every loop
                column+=1
            row +=1
            column=0
    setupkeyboard() # variables stores in local and collected

    ######################## plot tab ##########################

    import pyqtgraph as pg
    from pyqtgraph import QtGui as graphGui
    pg.setConfigOptions(antialias=True)

    graphWidget = pg.PlotWidget()
    graphWidget.setRenderHints(graphGui.QPainter.Antialiasing)
    graphWidget.showGrid(x=True,y=True)
    graphWidget.setAntialiasing(True)
    plotLine1 = QLineEdit()
    plotLine1.setMaximumWidth(screen_width/4)
    plotLine2 = QLineEdit()
    plotLine2.setMaximumWidth(screen_width / 4)
    plotLine3 = QLineEdit()
    plotLine3.setMaximumWidth(screen_width / 4)

    plotLayout = QGridLayout()
    plotLayout.addWidget(plotLine1,0,0,1,1)
    plotLayout.addWidget(plotLine2, 1, 0,1,1)
    plotLayout.addWidget(plotLine3, 3, 0,1,1)
    plotLayout.addWidget(graphWidget,0,1,4,4)
    plotWidget = QWidget()
    plotWidget.setStyleSheet('background-color:white;')
    plotWidget.setLayout(plotLayout)

    ######################## pi calculate ###################
    piTabWidget = QWidget()

    piTabLayout = QFormLayout()
    piTabWidget.setLayout(piTabLayout)
    piTabCb = QComboBox()
    piTabCb.addItems(['Chudnovsky','Machin'])
    piTabLayout.addRow(QLabel('Algorithm :'),piTabCb)
    piTabdigits = QLineEdit()
    piTabdigits.setPlaceholderText('Default digits : 1000')
    piTabLayout.addRow(QLabel('Decimals :'),piTabdigits)
    piTabSavePi = QPushButton('Save result')
    piTabSavePi.clicked.connect(lambda :compute_pi().savePI())
    piTabLayout.addWidget(piTabSavePi)
    piTabButton = QPushButton('Run algorithm')
    piTabButton.clicked.connect(lambda :compute_pi().compute(piTabCb.currentText()))
    piTabLayout.addWidget(piTabButton)

    tab.addTab(main_keyboard_widget,'calculator')
    tab.addTab(plotWidget, 'plot graph')
    tab.addTab(piTabWidget, 'calculate PI')

    runBT= QPushButton('Run')
    runBT.clicked.connect(execute)
    tab.setCornerWidget(runBT)


    return layout