from PySide2.QtWidgets import *
from PySide2.QtCore import QCoreApplication
from PySide2.QtGui import *
def scientific_calculator(screen_width, screen_height):
    from Add_on.scientific_calculator import constants
    import decimal
    import math
    decimal
    PI = constants.PI

    class compute_pi:
        def __init__(self, ditgits=1000):
            self.digit = ditgits
            self.constant = PI

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
            pi = Decimal(4 * (4 * arccot(5, decimals + 3) - arccot(239, decimals + 3))).quantize(
                Decimal(10) ** (-decimals))
            o = open('pi.txt','w')
            o.write(str(pi))
            o.close()
            print('pi saved in pi.txt')

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

            if not compiled:
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
                p = subprocess.Popen(['./gmp-chudnovsky', str(digits), '1'], stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE, cwd=path)
            elif sys_name == 'Windows':
                p = subprocess.Popen(['gmp-chudnovsky.exe', str(digits), '1'], stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE, cwd=path)

            out, err = p.communicate()
            print(out.decode())
    def key_handler(key):
        if key =='del':
            pass
        else:
            line.setText(line.text()+' '+key)

    def execute():
        def print(text):
            edit.append(str(text)+'\n')

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
        radians = math.radians
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
    edit.setMaximumHeight(screen_height/4)
    edit.setAlignment(Qt.AlignRight)
    edit.setFont(QFont("Sans Bold", 15))
    line = QLineEdit()
    line.setFont(QFont("Sans Bold", 15))
    line.setMinimumHeight(screen_height/12)
    line.returnPressed.connect(execute)
    tab = QTabWidget()
    layout.addWidget(edit)
    layout.addWidget(line)
    layout.addWidget(tab)

    ########################## main keyboard layout ##############################
    main_keyboard_widget = QWidget()
    main_keyboard_layout = QGridLayout()
    main_keyboard_widget.setLayout(main_keyboard_layout)
    mainKeyboardLayout = [['C','del','ans','undo','^',],['7','8','9'],['4','5','6'],['2','3','4']]
    def setupkeyboard():
        row = 0
        column = 0
        for i in mainKeyboardLayout:
            for x in i :
                but = QPushButton(x)
                but.setMinimumHeight(40)
                #but.setFixedSize(100,100)
                but.clicked.connect(lambda :key_handler(x))
                main_keyboard_layout.addWidget(but,row,column)
                column+=1
            row +=1
            column=0
    setupkeyboard()
    tab.addTab(main_keyboard_widget,'calculator')



    return layout