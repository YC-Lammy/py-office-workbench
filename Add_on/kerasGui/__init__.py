from PySide2.QtWidgets import *
from PySide2.QtCore import QCoreApplication
from PySide2.QtGui import *
from PySide2 import QtGui, QtCore
from PySide2.QtTest import QTest

def kerasGui(screen_width, screen_height):
    import gc
    #keras would be imported after user finish configuration

    nodeNum = 0
    def keyHandler(event):# handle key events in nodeView widget
        key = event.key()
        print(key)
        if key ==16777223:
            for i in nodeScene.selectedItems():
                nodeScene.removeItem(i.parentItem())
        elif key == 71:
            nodeScene.selectedItems()
    def addNode(target):
        if target == "inputLayer":
            main = QWidget()
            main.setLayout()
           # main.mousePressEvent =

    def showMainContextMenu(pos):
        menu = QMenu('contextMenu')
        addMenu = menu.addMenu("add")
        addMenu.addAction("Input Layer").triggered.connect(lambda : addNode("inputLayer"))
        menu.addAction("&Duplicate")
        menu.exec_(pos)

    def resizeGrid(event, grid):
        global  gridItem
        nodeScene.removeItem(grid)
        gridItem = nodeScene.addPixmap(QPixmap("pic/background/gridLine.png")\
            .scaled(nodeView.width(), nodeView.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        gridItem.setZValue(-1)

    def zoomScene(event):
        print(event.position())
        print(event.angleDelta().y())

    def updateMouseReleasePos(event):
        refObject.setObjectName(str(event.x())+','+str(event.y()))

    def dragLine(event):

        lastReleasePos = refObject.objectName()
        start = nodeView.mapFromGlobal(event.globalPos())
        print(nodeScene.itemAt(start,QTransform()))
        line = nodeScene.addLine(start.x(),start.y(),100,100)
        line.setPen(QPen(Qt.white))


    mainLayout = QGridLayout()
    refObject = QLabel()

    nodeScene = QGraphicsScene()
    nodeView = QGraphicsView()
    nodeView.setBackgroundBrush(QColor(40,40,40)) #set background colour
    nodeView.setScene(nodeScene)
    nodeView.setContextMenuPolicy(Qt.CustomContextMenu) #there is no default menu
    nodeView.customContextMenuRequested.connect(showMainContextMenu) #show context menu

    gridItem = nodeScene.addPixmap(QPixmap("pic/background/gridLine.png")\
        .scaled(nodeView.width(),nodeView.height(),Qt.IgnoreAspectRatio, Qt.SmoothTransformation)) # add grid lines

    nodeView.resizeEvent = lambda x: resizeGrid(x,gridItem) # assign the resize event for the grid lines
    nodeView.keyPressEvent = keyHandler
    nodeView.wheelEvent = zoomScene
    #.mouseReleaseEvent = updateMouseReleasePos

    paintPath = QtGui.QPainterPath()
    paintPath.addRoundRect(QtCore.QRectF(0,0,screen_width/10,screen_height/5), 20,20)
    gradient = QLinearGradient(0,0,0,screen_height/5)
    gradient.setColorAt(0,Qt.darkRed)
    gradient.setColorAt(0.2,QColor(80,80,80))
    rect = nodeScene.addPath(paintPath,QPen(Qt.NoPen), QBrush(gradient))
    rect.setFlags(QGraphicsItem.ItemIsMovable)
    c = nodeScene.addRect(0,30,screen_width/10,screen_height/5-30)
    c.setPen(QPen(Qt.NoPen))
    c.setParentItem(rect)
    c.setFlags(QGraphicsItem.ItemIsSelectable)
    roundBt = QPushButton()
    roundBt.setFixedSize(12, 12)
    a = QtCore.QRect(QtCore.QPoint(), roundBt.size())
    roundBt.setMask(QRegion(a, QRegion.Ellipse))
    roundBt.mousePressEvent = dragLine
    roundBt.mouseReleaseEvent = updateMouseReleasePos
    roundBt.move(-(roundBt.width() / 2), 30)
    b = nodeScene.addWidget(roundBt)
    b.setParentItem(rect)
    mainLayout.addWidget(nodeView)
    gc.collect()
    return  mainLayout