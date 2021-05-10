import sys,os, gc
from PySide2.QtWidgets import *
from PySide2.QtCore import QCoreApplication
from PySide2.QtGui import *
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon


def main():
	global tabs
	QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
	app = QApplication(sys.argv)
	cfg = open('config.cfg','r')
	modules = [i.replace("\n",'') for i in cfg.read().split(',')]
	cfg.close()
	##################### Menu bar Actions ########################
	def pick_sys_file(filter="All files (*)"):
		from mimetypes import guess_type
		if filter == False:
			filter = "All files (*)"
		file_name, filter = QFileDialog.getOpenFileName(window, 'Open File', 'c://', filter=filter)
		print(guess_type(file_name))
		return file_name

	def get_background_task(pid):
		import threading, psutil
		threading_box = QWidget()
		threading_box.setWindowTitle('resources usage')
		threading_box.setWindowIcon(QIcon('pic/icon/main.png'))
		pyUse = psutil.Process(pid)
		label = QLabel()

		def setValues():
			gc.collect()
			cpu = psutil.cpu_count()
			vms = psutil.virtual_memory()[0]/1024**2
			platform = sys.platform
			swap = psutil.swap_memory()[0]/1024**2
			while True:
				threading_box.show()
				label.setText(f'platform: {platform}\n'
							f'Cores: {cpu}\n'
							f'Total Virtual memory: {vms}\n'
							f'Total swap memory: {swap}\n \n'
							f'Threads: {pyUse.num_threads()}\n'
							f'single core percentage: {pyUse.cpu_percent(interval=0.2)}\n'
							f'Memory use: {(pyUse.memory_full_info().uss/1024**2)} MB')
				gc.collect()
				if threading_box.isHidden():
					label.deleteLater()
					threading_box.deleteLater()
					layout.deleteLater()
					gc.collect()
					break

		layout = QVBoxLayout()
		layout.addWidget(label)
		threading_box.setLayout(layout)
		a = threading.Thread(target=setValues)
		a.daemon = True
		a.start()
		gc.collect()

	def addOnDialog():
		def addModule():
			global modules
			from shutil import copy2
			file = QFileDialog.getOpenFileName()
			print(file.split('/')[-1])
			copy2(file, '/Add_on')
			o = open('config.cfg','a')
			o.write(','+file.split('/')[-1])
			o.close()
			cfg = open('config.cfg', 'r')
			modules = [i.replace("\n", '') for i in cfg.read().split(',')]
			cfg.close()

		box = QDialog(window)
		content = QWidget()
		layout = QFormLayout(content)
		for i in modules:
			layout.addRow(QLabel(i),QPushButton('remove'))

		button = QPushButton('Add Module')
		button.clicked.connect(addModule)

		scroll =QScrollArea()
		scroll.setWidget(content)
		scroll.setMaximumHeight(screen_height/3)
		scroll.setMinimumWidth(content.width()+scroll.verticalScrollBar().width())
		scroll.setWidgetResizable(True)

		l = QVBoxLayout()
		l.addWidget(scroll)
		l.addWidget(button)
		box.setLayout(l)
		box.exec_()


	def link_options():
		link_box = QMessageBox()
		link_box.setWindowTitle('Link between tabs')
		link_box.exec()

	def console():
		from Add_on import console
		layout = console.console(screen_width,screen_height)
		window =QDialog()
		window.setMinimumSize(screen_width/2,screen_height/2)
		window.setLayout(layout)
		window.setWindowTitle('python console')
		window.exec_()

	def save_preference():
		o = open('preference.cfg', 'w')
		a = [[str(mainTabWidget.indexOf(i)), k
				 , i.objectName()] for k, i in tabs.items()]  # get index from object name
		o.write(str(a))
		o.close()
		del o

	def load_factory_preference():
		pass

	#################### Main Application ####################################
	app.setWindowIcon(QIcon('pic/icon/main.png'))
	app.setApplicationDisplayName('workbench')
	app.setApplicationName('workbench')
	app.setStyleSheet("QToolTip {color: #ffffff; background-color: #000000; border: 5px solid #00000000;}")
	size = app.primaryScreen().size() # get primary screen size
	screen_height = size.height()
	screen_width = size.width()
	print('metrics(0): '+str(screen_width)+' metrics(1): '+str(screen_height))
	app.setStyle('Fusion')
	window = QWidget()
	window.setGeometry(0, 0, screen_width, screen_height)
	window.setWindowTitle('workbench')

	################### Tab widget ######################
	print('Setting up main Widget...')
	mainTabWidget = QTabWidget()
	mainTabWidget.setTabsClosable(True)
	mainTabWidget.tabCloseRequested.connect(lambda index: close_tab(index))  # pass index to function
	mainTabWidget.setMovable(True)
	tabs = {}  # store QWidget Objects by name

	def add_new_tab(target_module, Name):
		#global tabs
		try:
			exec('from Add_on import ' +target_module)
			if Name[-1].isnumeric():
				Tab_name = Name
			else:
				Tab_name = Name + '0'
			while Tab_name in [x for x, y in tabs.items()]:  # duplicate will cause confusion in dict
				Tab_name = str(Tab_name[:-1]) + str(int(Tab_name[-1]) + 1)  # if number exist
			i = Tab_name
			tabs[i] = QWidget()
			tabs[i].setObjectName(f'{target_module}')
			exec(f'tabs[i].setLayout({target_module}.{target_module}({screen_width},{screen_height}))')
			mainTabWidget.addTab(tabs[i],Tab_name)

		except Exception as e:

			alert = QMessageBox()
			alert.setWindowTitle('ERROR')
			alert.setWindowIcon(QIcon('pic/icon/warning.png'))
			alert.setText(str(e))
			alert.exec()
			alert.deleteLater()

		gc.collect()

	def close_tab(index_of_tab):  # the index was passed in by tab Close Request
		#global tabs
		a = mainTabWidget.tabText(index_of_tab)  # key to delete from dict
		tab = mainTabWidget.widget(index_of_tab)
		mainTabWidget.removeTab(index_of_tab)
		tab.close()
		tab.deleteLater()
		gc.collect()
		tabs[a].deleteLater()
		del tabs[a] , tab # delet from dict
		gc.collect() #collect it imediatly

	def choose_new_tab():  # choose from a new window
		from os import walk
		from functools import partial
		box = QDialog(window)
		box.setGeometry(int(screen_width/6),int(screen_height/6)
						,int(screen_width*2/3),int(screen_height*2/3))
		box.setStyleSheet("background-color: white;")
		box_layout = QGridLayout()
		scroll = QScrollArea()
		scroll.setLayout(box_layout)
		scroll.setWidgetResizable(True)
		paths = [x[0] for x in walk("""Add_on""")]
		fLable = QLabel('frequently use:')
		fLable.setMaximumWidth(int(screen_width*2/9))
		fLable.setMaximumHeight(int(screen_height/25))
		fLable.setFont(QFont("Times New Roman", 15))
		scroll.setWidget(fLable)
		#box_layout.addWidget(fLable,0,0,1,10)
		icon_width = scroll.width()/6
		x = 0
		y=0
		for i in modules:
			a = QPushButton(str(i))
			#a.setFixedHeight(icon_width)
			#a.setFixedWidth(icon_width)
			#a.setFlat(True)
			def add_tab(a,b):
				box.deleteLater()
				box.close()
				add_new_tab(a,b)
			exec(f"a.clicked.connect(partial(add_tab,'{i}','{i}'))")
			box_layout.addWidget(a, y, x,1,1)
			x+=1
			if x==5:
				y+=1
				x=0
		gc.collect()
		layout = QVBoxLayout()
		layout.addWidget(scroll)
		box.setLayout(layout)
		box.setWindowTitle('choose new tab')
		box.exec()
		gc.collect()

	################### set up preference ######################
	def set_up_preference():
		print('reading config file...')
		o = open('preference.cfg', 'r')
		config = o.read()
		o.close()
		if config:
			listTabs = [[y for y in x.split("""', '""")]  # list from string
						for x in config.replace("[['", '').replace("']]", '').split("""'], ['""")]
			listTabs = sorted(listTabs, key=lambda x: (int(x[0])))  # sort order of tabs

			print('loading tabs from file...')
			for i in listTabs:
				add_new_tab(i[2], i[1])
			del listTabs, i, config, o
			gc.collect()

	set_up_preference()  # local variables for better performance
	del set_up_preference
	print('finish setup')

	################### set up layout ##########################
	layout = QVBoxLayout()
	window.setLayout(layout)
	blank_spacer = QLabel()
	layout.addWidget(blank_spacer)
	layout.addWidget(mainTabWidget)

	#################### Menu section #########################
	bar = QMenuBar(window)
	bar.setStyleSheet('background-color:white; color:black;')
	bar.setMinimumWidth(window.frameGeometry().width())
	file = bar.addMenu("&File")
	file.addAction("Save")#.setShortcut("Ctrl+S")
	file.addAction('&Open...').triggered.connect(pick_sys_file)
	file.addAction("E&xit").triggered.connect(sys.exit)
	menuImport = file.addMenu('&Import')
	menuExport = file.addMenu('&Export')
	menuStartup = file.addMenu('Startup')
	menuStartup.addAction('&Save Start up Settings').triggered.connect(save_preference)
	menuStartup.addAction('&Load Factory Settings')
	file.addAction('Add On').triggered.connect(addOnDialog)
	edit = bar.addMenu("Edit")
	edit.addAction("cu&t")#.setShortcut("Ctrl+X")
	edit.addAction("copy")#.setShortcut("Ctrl+C")
	edit.addAction("paste")#.setShortcut("Ctrl+V")
	viewTask = bar.addMenu('&View')
	viewTask.addAction("Current Task").triggered.connect(lambda :get_background_task(os.getpid()))

	link = bar.addMenu('Link')
	link.addAction('Between Tabs').triggered.connect(link_options)
	bar.addAction('console').triggered.connect(console)
	add_tab_bt = QPushButton('+')
	add_tab_bt.setFont(QFont("Times New Roman", 15))
	add_tab_bt.setStyleSheet("QPushButton { text-align: top left; }")
	add_tab_bt.setFlat(True)
	add_tab_bt.clicked.connect(choose_new_tab)
	bar.setCornerWidget(add_tab_bt)
	blank_spacer.setFixedHeight(int(bar.height()*0.6))
	####################### Exec ##########################
	window.show()
	window.setWindowState(Qt.WindowMaximized)
	print('Exec application')
	gc.collect()
	app.exec_()

if __name__ == '__main__':
	main()
	import psutil
	process  = psutil.Process(os.getpid())
	for proc in process.children(recursive =True): #make sure every child is killed
		proc.kill()
	process.kill()
	sys.exit()