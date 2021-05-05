from Crypto.Cipher import AES
import time, os, sys
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt

def file_encryptor(screen_width,screen_height):
    files = {}
    def get_file():
        file, filter = QFileDialog.getOpenFileName()
        files['new']=file
        if '.aes256' in file:
            decrypt_bt.setDisabled(False)
            decrypt_save_bt.setDisabled(False)
        else:
            encrypt_bt.setDisabled(False)

    def encrypt():
        key = edit_key.text()
        key_num = len(key)
        if key_num <16:
            key += '0'*(16-key_num)
        elif key_num >16 and key_num <32:
            key +='0'*(32-key_num)
        elif key_num >32:
            box = QMessageBox()
            box.setWindowTitle('key length exceed 32')
            box.setStyleSheet('color:red;')
            box.setText('Error : key length exceed 32')
            box.exec_()
        with open(files['new'], 'r') as f:
            message = f.read()
            f.close()
        key = key.encode()
        obj = AES.new(key, AES.MODE_EAX)
        nonc = obj.nonce
        ciphertext = obj.encrypt(message)
        with open(files['new']+'.aes256','w') as f:
            f.write(ciphertext+'nonc:'.encode()+nonc)
            f.close()

    def decrypt(file):
        with open(file,'r')as f:
            encrypted = f.read()
            f.close()
        key = edit_key.text().encode()
        encrypted , nonc = encrypted.split('nonc:')
        obj2 = AES.new(key, AES.MODE_EAX, nonc)
        a = obj2.decrypt(encrypted)
        print(a)
        return a

    def gen_random_key():
        edit_key.setText(os.urandom(32).decode())


    # print(message)

    # print(ciphertext)

    class dropArea(QLabel):
        def __init__(self):
            super().__init__()
            self.setText('drop or select file')
            self.setAcceptDrops(True)
            self.setFixedSize(screen_width/2,screen_height/3)
            self.setAlignment(Qt.AlignCenter)
            self.setStyleSheet('background-color:white ;border: 3px solid;border-color:blue ;border-style:dashed;')

        def dragEnterEvent(self, event):
            print('drag-enter')
            if event.mimeData().hasUrls():
                print('has urls')
                event.accept()
            else:
                event.ignore()

        def dropEvent(self, event):
            lines = []
            for url in event.mimeData().urls():
                lines.append('dropped: %r' % url.toLocalFile())
            self.setText('\n'.join(lines))

    drop_area = dropArea()
    file_bt = QPushButton('select a file')
    file_bt.setStyleSheet('color:white;background-color:blue;')
    file_bt.clicked.connect(get_file)
    dropLayout = QHBoxLayout()
    dropLayout.addWidget(file_bt,alignment=Qt.AlignBottom)
    drop_area.setLayout(dropLayout)
    encrypt_bt = QPushButton('encrypt and save')
    encrypt_bt.setMaximumWidth(screen_width/4)
    encrypt_bt.setDisabled(True)
    decrypt_bt = QPushButton('decrypt and read')
    decrypt_bt.setMaximumWidth(screen_width/4)
    decrypt_bt.setDisabled(True)
    decrypt_save_bt = QPushButton('decrypt and save')
    decrypt_save_bt.setMaximumWidth(screen_width/4)
    decrypt_save_bt.setDisabled(True)
    edit_key = QLineEdit()
    gen_bt = QPushButton('generate random key')
    layout = QGridLayout()

    layout.addWidget(drop_area,0,2,1,1)
    layout.addWidget(QLabel('Enter key'),1,1,1,1)
    layout.addWidget(edit_key,1,2,1,1)
    layout.addWidget(gen_bt,1,3,1,1)
    buttons = QHBoxLayout()
    buttons.addWidget(encrypt_bt)
    buttons.addWidget(decrypt_bt)
    buttons.addWidget(decrypt_save_bt)
    layout.addLayout(buttons,2,0,1,4)

    return layout