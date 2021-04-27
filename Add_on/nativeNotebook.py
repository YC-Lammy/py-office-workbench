import traceback

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

def nativeNotebook(screen_width,screen_height):

    blocks = [] # dict in array
    def newBlock():
        num = len(blocks)

        edit = QTextEdit()
        edit.verticalScrollBar().hide()
        edit.keyReleaseEvent = lambda x: resizeText(num)
        edit.document().setUndoRedoEnabled(True)
        edit.insertPlainText('')
        edit.setFixedHeight(edit.document().size().height())
        label = QTextEdit()
        label.setReadOnly(True)
        label.setFrameStyle(QFrame.NoFrame)
        label.insertPlainText('')
        label.verticalScrollBar().hide()
        label.setFixedHeight(edit.document().size().height())

        blockLayout = QFormLayout()
        button = QPushButton()
        button.setFlat(True)
        button.setFixedSize(30, 30)
        button.setIcon(QIcon('pic/icon/execute.png'))
        button.clicked.connect(lambda: runBlock(num))
        addCodeButton = QPushButton('+ Code')
        addCodeButton.clicked.connect(newBlock)
        addCodeButton.setFixedHeight(30)
        addCodeButton.setStyleSheet('background-color : white')
        closeButton = QPushButton('X')
        closeButton.setFixedSize(30, 30)
        closeButton.clicked.connect(lambda :removeBlock(num))
        blockLayout.addRow(button, edit)
        blockLayout.addWidget(label)
        blockLayout.addRow(closeButton, addCodeButton)

        blockWidget = QWidget()
        blockWidget.resize(blockWidget.width(), screen_height / 10)
        blockWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        blockWidget.setStyleSheet("background-color: rgb(250,250,250);")
        blockWidget.setLayout(blockLayout)

        blocks.append({'var': {}, 'text': edit, 'label': label, 'layout': blockLayout, 'widget': blockWidget})
        label.changeEvent = lambda x: resizeText(num, 1000)

        subLayout.addWidget(blockWidget)

    def removeBlock(num):
        subLayout.removeWidget(blocks[num]['widget'])
        blocks[num].pop('var')
        for x,y in blocks[num].items():
            y.deleteLater()


    def runBlock(blocknum):
        try:
            def print(text):
                text = str(text)
                label = blocks[blocknum]['label']
                label.setReadOnly(False)
                label.append(text + '\n')
                label.setReadOnly(True)
                width = blocks[blocknum]['widget'].width() - 60
                size = label.document().size()
                blocks[blocknum]['label'].setFixedSize(width, size.height())
                blocks[blocknum]['widget'].resize(blocks[blocknum]['widget'].width(),
                                             size.height() + blocks[blocknum]['label'].height() + 60)

            blocks[blocknum]['label'].clear()
            print('')

            text = blocks[blocknum]['text'].toPlainText()
            if blocknum == 0:
                loc = {}
                blocks[blocknum]['var']={}
            else:
                loc = blocks[blocknum - 1]['var']

            if 'os.system'in text:
                raise Exception('os.system restricted')

            code = compile( 'locals().update(loc)\n'+text,'code','exec')
            exec(code, locals(), blocks[blocknum]['var'])
        except Exception as e:
            blocks[blocknum]['label'].setTextColor(Qt.red)
            print(str(e))
            print(traceback.format_exc())
            blocks[blocknum]['label'].setTextColor(Qt.black)
        resizeText(blocknum)

    def savePy():
        text = ''
        for i in blocks:
            text+='\n################################\n\n'
            text+=i['text'].toPlainText()
        path, filter = QFileDialog.getSaveFileName(dir='c://')
        with open(path,'w')as f:
            f.write(text)
            f.close()

    def resizeText(num,width=False):
        if not width:
            width = blocks[num]['widget'].width()-60
        size = blocks[num]['text'].document().size()
        blocks[num]['text'].setFixedSize(width,size.height())
        blocks[num]['widget'].resize(blocks[num]['widget'].width(),size.height()+blocks[num]['label'].height()+60)

    mainLayout = QHBoxLayout()


    mainWidget = QWidget()
    mainWidget.setMaximumWidth(int(screen_width/1.1))
    mainWidget.setStyleSheet("background-color: white;")
    subLayout  = QVBoxLayout(mainWidget)
    subLayout.setAlignment(Qt.AlignTop)

##################### first block ####################################
    edit = QTextEdit()
    edit.verticalScrollBar().hide()
    edit.keyReleaseEvent = lambda x: resizeText(0)
    edit.document().setUndoRedoEnabled(True)
    edit.insertPlainText('')
    edit.setFixedHeight(edit.document().size().height())
    label = QTextEdit()
    label.setReadOnly(True)
    label.setFrameStyle(QFrame.NoFrame)
    label.insertPlainText('')
    label.verticalScrollBar().hide()
    label.setFixedHeight(edit.document().size().height())

    blockLayout = QFormLayout()
    button = QPushButton()
    button.setFlat(True)
    button.setFixedSize(30,30)
    button.setIcon(QIcon('pic/icon/execute.png'))
    button.clicked.connect(lambda :runBlock(0))
    addCodeButton = QPushButton('+ Code')
    addCodeButton.clicked.connect(newBlock)
    addCodeButton.setFixedHeight(30)
    addCodeButton.setStyleSheet('background-color : white')
    blockLayout.addRow(button,edit)
    blockLayout.addWidget(label)
    blockLayout.addWidget(addCodeButton)

    blockWidget = QWidget()
    blockWidget.resize(blockWidget.width(),screen_height/10)
    blockWidget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Maximum)
    blockWidget.setStyleSheet("background-color: rgb(250,250,250);")
    blockWidget.setLayout(blockLayout)

    blocks.append({'var': {}, 'text': edit, 'label': label, 'layout': blockLayout,'widget':blockWidget})
    label.changeEvent = lambda x: resizeText(0, 1000)

    subLayout.addWidget(blockWidget)

##################### menu ###############################################
    menu = QMenuBar()
    menu.setMaximumWidth(int(screen_height/1.1))
    file = menu.addMenu('File')
    file.addAction('Save').triggered.connect(savePy)
    edit = menu.addMenu('Edit')
    run = menu.addMenu('Run')
    run.addAction('Rerun All')


########################################################################
    toolWidget = QWidget()
    toolLayout =QFormLayout()
    toolWidget.setLayout(toolLayout)
    menuButton = QPushButton('Menu')
    menuButton.setFlat(True)
    syncButton = QPushButton()
    syncButton.setIcon(QIcon('pic/icon/link_sync.png'))
    syncButton.setFlat(True)
    syncButton.setIconSize(QSize(30,30))

    toolLayout.addRow(QLabel('|'),menuButton)
    toolLayout.addRow(QLabel('|'),syncButton)

    scroll = QScrollArea()
    scroll.setWidget(mainWidget)
    scroll.setWidgetResizable(True)

    mainLayout.addWidget(toolWidget,alignment=Qt.AlignLeft)
    mainLayout.addWidget(scroll)

    subLayout.setMenuBar(menu)
    return mainLayout
