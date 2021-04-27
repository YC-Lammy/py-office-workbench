import serial,threading
import serial.tools.list_ports
from time import sleep
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import QIcon
import pyqtgraph as pg

def serial_plotter(screen_width,screen_height):
    stop_plot_thread = False
    plot_thread_ended = False
    plot_thread_started = False
    pg.setConfigOptions(useOpenGL=False, crashWarning=True, background='w')
    stop_plot_thread = False
    plot_thread_ended = False
    plot_thread_started = False

    ###################### serial graph functions ########################
    class SignalCommunicate(QObject):
        request_graph_update = Signal(list)
        request_graph_cleared = Signal()
    def get_available_port():
        ports = serial.tools.list_ports.comports()
        current_ports = ['--please select', ' ']
        item_in_port_cb = [port_cb.itemText(i) for i in range(port_cb.count())]
        for port, desc, hwid in sorted(ports):
            print(f"{port}: {desc} [{hwid}]")
            current_ports.append(port)
        for i in current_ports:
            if i not in item_in_port_cb:
                port_cb.addItem(i)
        for i in item_in_port_cb:
            if i not in current_ports:
                port_cb.removeItem(port_cb.findText(i))

    def read_serial(plotGraph):
        global ser, plot_thread, plot_thread_started, serial_signalComm
        serial_signalComm = SignalCommunicate()
        serial_signalComm.request_graph_update.connect(update_serial_graph)
        serial_signalComm.request_graph_cleared.connect(clear_graph)
        try:
            ser = serial.Serial(port_cb.currentText(), int(BAUD_cb.currentText()), timeout=0.1)
            plot_thread = threading.Thread(target=serial_plot_graph, args=(plotGraph))
            plot_thread.daemon = True
            plot_thread.start()
            plot_thread_started = True
        except Exception as e:
            print(e)
            alert = QMessageBox()
            alert.setWindowTitle('ERROR')
            alert.setWindowIcon(QIcon('pic/icon/warning.png'))
            if port_cb.currentText() == ' ' or port_cb.currentText() == '--please select':
                alert.setText('[ERROR]please choose a port')
            else:
                alert.setText(str(e))
            alert.exec()

    def serial_plot_graph(graph1='graph1'): # exec when button pressed
        global curves, serial_signalComm
        global plots, ser, stop_plot_thread, plot_thread_ended, plot_thread_started
        plots = []
        curves = []
        val = str(ser.readline().decode().strip('\r\n'))
        if not dataSplitBox.text():
            split = ','
        else:
            split = dataSplitBox.text()
        number_of_lines1 = len(val.split(split))
        for i in range(int(number_of_lines1)):
            plots.append([])
            curves.append(plotGraph.plot())
        while True:
            try:
                val = str(ser.readline().decode().strip('\r\n'))  # Capture serial output as a decoded string
                text.insertPlainText(val+'\n') # set text in text editor
                valA = val.split("/") # split into list
                if val:
                    serial_signalComm.request_graph_update.emit(valA) #emit signal and pass value
                if stop_plot_thread:
                    ser.close()
                    plot_thread_ended = True
                    serial_signalComm.request_graph_cleared.emit() #emit signal to clear the graph
                    stop_plot_thread = False
                    plot_thread_started = False
                    break
            except Exception as e:
                print(e)
                continue


    def update_serial_graph(valA): # exec when signal is emitted from serial_plot_graph()
        for i in range(0, len(valA)):
            valA[i] = float(valA[i])
            plots[i].append(valA[i])
        for i in range(0, len(curves)):
            curves[i].setData(plots[i])

    # app.processEvents()

    def clear_graph(plot): # exec when signal is emitted from serial_plot_graph()
        #global  plotGraph
        #serial_visualise_box.removeWidget(plot)
        #del plot
        #plotGraph = pg.PlotWidget()
        #serial_visualise_box.addWidget(plotGraph,0,0,1,4)
        global stop_plot_thread, plots, curves
        if plot_thread_started:
            stop_plot_thread = True
            sleep(1)
            if plot_thread_ended:
                for i in range(0, len(plots)):
                    plots[i] = [0.0]
                for i in curves:
                    i.setData([0.0])
                text.clear()
                print('clear')

    serial_visualise_box = QHBoxLayout()
    plotGraph = pg.PlotWidget()
    port_cb = QComboBox()
    port_cb.setMaximumWidth(int(screen_width / 5))
    #port_cb.highlighted.connect(get_available_port)  # get the ports when user clickes into combobox
    port_cb.mousePressEvent = lambda x:get_available_port()
    #port_cb.addItem(' ')  # to use the highlighted signal, an item is required
    BAUD_cb = QComboBox()
    BAUD_cb.setMaximumWidth(int(screen_width / 5))
    BAUD_cb.addItems(['300', '1200', '2400', '4800', '9600', '19200', '38400', '57600', '74880'
                         , '115200', '230400', '250000', '5000000', '10000000', '20000000'])  # default baud rates
    clear_graph_bt = QPushButton('Clear_graph')
    clear_graph_bt.setMaximumWidth(int(screen_width / 5))
    clear_graph_bt.clicked.connect(lambda :clear_graph(plotGraph))
    serial_start_bt = QPushButton('start')
    serial_start_bt.setMaximumWidth(int(screen_width / 5))
    serial_start_bt.clicked.connect(lambda: read_serial(plotGraph))
    dataSplitBox = QLineEdit()
    dataSplitBox.setMaximumWidth(int(screen_width / 5))
    text = QTextEdit()
    text.setReadOnly(True)
    text.setMaximumWidth(screen_width/4)
    text.setMaximumHeight(screen_height)

    formLayout = QFormLayout()
    formLayout.addWidget(text)
    formLayout.addRow(QLabel('port: '),port_cb)
    formLayout.addRow(QLabel('Baud rate: '),BAUD_cb)
    formLayout.addRow(QLabel('split data by: '),dataSplitBox)
    formLayout.addWidget(clear_graph_bt)
    formLayout.addWidget(serial_start_bt)
    serial_visualise_box.addWidget(plotGraph,Qt.AlignHCenter)
    serial_visualise_box.addLayout(formLayout,Qt.AlignRight)

    return serial_visualise_box