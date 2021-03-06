from PySide2.QtWidgets import QApplication

from qtpy.QtGui import QImage
from qtpy.QtCore import QRectF
from qtpy.QtWidgets import QLabel

from nodeeditor.node_editor_window import NodeEditorWindow
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_socket import LEFT_CENTER, RIGHT_CENTER
from nodeeditor.utils import dumpException


class CalcGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        self.icons = QImage("icons/status_icons.png")

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 24.0
        if self.node.isDirty(): offset = 0.0
        if self.node.isInvalid(): offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )


class CalcContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)


class CalcNode(Node):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"

    GraphicsNode_class = CalcGraphicsNode
    NodeContent_class = CalcContent

    def __init__(self, scene, inputs=[2,2], outputs=[1]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)

        self.value = None

        # it's really important to mark all nodes Dirty by default
        self.markDirty()


    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

    def evalOperation(self, input1, input2):
        return 123

    def evalImplementation(self):
        i1 = self.getInput(0)
        i2 = self.getInput(1)

        if i1 is None or i2 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.grNode.setToolTip("Connect all inputs")
            return None

        else:
            val = self.evalOperation(i1.eval(), i2.eval())
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.grNode.setToolTip("")

            self.markDescendantsDirty()
            self.evalChildren()

            return val

    def eval(self):
        if not self.isDirty() and not self.isInvalid():
            print(" _> returning cached %s value:" % self.__class__.__name__, self.value)
            return self.value

        try:

            val = self.evalImplementation()
            return val
        except ValueError as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            self.markDescendantsDirty()
        except Exception as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            dumpException(e)



    def onInputChanged(self, socket=None):
        print("%s::__onInputChanged" % self.__class__.__name__)
        self.markDirty()
        self.eval()


    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized CalcNode '%s'" % self.__class__.__name__, "res:", res)
        return res
#app = QApplication()
#wnd  = NodeEditorWindow()

#CalcNode(wnd.nodeeditor)
#wnd.nodeeditor.addNodes()
#app.exec_()
def chudnovsky(digits=0):
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
            compiled = True  # remove it if not using linux

            if compiled == False:
                #try:
                    p = subprocess.Popen(
                        ['gcc', '-s', '-Wall', '-o', 'gmp-chudnovsky', 'gmp-chudnovsky.c', '-lgmp', '-lm'],
                        stdout=subprocess.PIPE, stdin=subprocess.PIPE)
                    out, err = p.communicate()
                    print(out)
                    print(err)
                #except Exception as e:
                    #QMessageBox(text=e).exec_()
            path = pathlib.Path().absolute()
            if sys_name == 'Linux' or sys_name == 'Darwin':
                p = subprocess.Popen(['Add_on/scientific_calculator/gmp-chudnovsky', str(digits), '1'],
                                     stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE, cwd=path)
            elif sys_name == 'Windows':
                p = subprocess.Popen(['gmp-chudnovsky.exe', str(digits), '1'], stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE, cwd=path)

            out, err = p.communicate()
            pi = out.decode()
            #if self.digit > 10000:
                #edit.append('result too large\nyou can choose to save into file\n')
            #else:
                #edit.append(pi + '\n')
            #resultPI['pi'] = pi
            return pi

import pyttsx3, os
import math
engine =pyttsx3.init()
voices = engine.getProperty('voices')
print([i.gender for i in voices])
#
engine.setProperty('voice', voices[0].id)
engine.setProperty('volume', 1)
engine.setProperty('rate',150)
engine.say(chudnovsky(10000))
engine.runAndWait()


import wave
import random
import struct
import datetime

SAMPLE_LEN = 44100 * 300 # 300 seconds of noise, 5 minutes

print("Create file using wave, storing frames in an array and using writeframes only once")

noise_output = wave.open('noise2.wav', 'w')
noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))

d1 = datetime.datetime.now()
values = []

for i in range(0, SAMPLE_LEN):
	value = random.randint(-32767, 32767)
	packed_value = struct.pack('h', value)
	values.append(packed_value)
	values.append(packed_value)

value_str = b''.join(values)
noise_output.writeframes(value_str)

d2 = datetime.datetime.now()
print((d2 - d1), "(time for writing frames)")

noise_output.close()

d3 = datetime.datetime.now()
print((d3 - d2), "(time for closing the file)")