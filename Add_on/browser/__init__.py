import sys, ctypes,psutil
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PySide2.QtCore import *
from PySide2.QtGui import *

def browser(screen_width,screen_height):
    saveBrowseHistory = True
    #class SignalCommunicate(QObject):
        #request_graph_update = Signal(list)
        #request_graph_cleared = Signal()
    historyFile = open('Add_on/browser/History.cfg', 'r')
    historyList = (historyFile.read()).splitlines()
    historyList = list(dict.fromkeys(historyList))
    historyList = [i.replace('https://www.google.com/search?q=','') for i in historyList]
    searchCompleter = QCompleter(
        historyList)
    searchCompleter.setCaseSensitivity(Qt.CaseInsensitive)
    searchCompleter.setMaxVisibleItems(8)
    searchCompleter.setFilterMode(Qt.MatchContains)
    def saveHistory():
        searchBar.setText(browser.url().toString())
        searchBar.clearFocus()
        if saveBrowseHistory:
            a = open('Add_on/browser/History.cfg', 'a')
            a.write(f'{browser.url().toString()}\r')
            a.close()

    def clearHistory():
        for i in 100:
            a = open('Add_on/browser/History.cfg', 'w')
            a.write('')
            a.close()

    def load_url():
        url = searchBar.text()
        if '.' not in url:
            browser.load(f'https://www.google.com/search?q={url}')
        elif 'http'not in url and '://' not in url:
            browser.load(f'http://{url}')
        else:
            browser.load(url)
        webBack.setDisabled(False)
        webForward.setDisabled(True)
        webReload.setDisabled(False)

    def backward():
        browser.back()
        webForward.setDisabled(False)

    def viewPageSource():
        browser.page().runJavaScript("document.getElementsByTagName('html')[0]", print)

    web_browser_box = QGridLayout()
    browser = QWebEngineView()
    browserSettings = browser.settings()
    browserSettings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
    browserSettings.setAttribute(browserSettings.FullScreenSupportEnabled, True)
    browserSettings.setAttribute(browserSettings.PluginsEnabled, True)
    #browser.loadStarted.connect(progressBar)
    browser.loadFinished.connect(saveHistory)
    searchBar = QLineEdit()
    searchBar.setPlaceholderText("Search or enter URL")
    searchBar.setCompleter(searchCompleter)
    searchBar.setMinimumHeight(screen_height/25)
    searchBar.setFont(QFont("Calibri", 15))
    searchBar.setStyleSheet("color:grey")
    searchBar.returnPressed.connect(load_url)
    webBack = QPushButton('<-')
    webBack.clicked.connect(backward)
    webBack.setFlat(True)
    webBack.setDisabled(True)
    webForward = QPushButton('->')
    webForward.clicked.connect(browser.forward)
    webForward.setFlat(True)
    webForward.setDisabled(True)
    webReload = QPushButton()
    webReload.setIcon(QIcon('pic/icon/Refresh_icon.png'))
    webReload.clicked.connect(browser.reload)
    webReload.setFlat(True)
    webReload.setDisabled(True)
    zoomIn = QPushButton("+")
    zoomIn.setFlat(True)
    zoomIn.clicked.connect(lambda : browser.setZoomFactor(browser.zoomFactor()+0.2))
    zoomOut = QPushButton("-")
    zoomOut.setFlat(True)
    zoomOut.clicked.connect(lambda: browser.setZoomFactor(browser.zoomFactor()- 0.2))
    web_browser_box.addWidget(webBack,0,0,1,1)
    web_browser_box.addWidget(webForward,0,1,1,1)
    web_browser_box.addWidget(QLabel(''),0,2,1,1)
    web_browser_box.addWidget(webReload,0,5,1,1)
    web_browser_box.addWidget(searchBar,0,6,1,14)
    web_browser_box.addWidget(zoomOut,0,22,1,1)
    web_browser_box.addWidget(zoomIn, 0, 23, 1, 1)
    web_browser_box.addWidget(browser,1,0,1,28)
    browser.setZoomFactor(1.2)
    return web_browser_box