import os, hashlib, socket, threading, time, smtplib, ssl

client_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
class server():
    def send(self,msg, conn):
        conn.send(msg.encode('UTF-8'))

    def recv(self,conn):
        msg_l = conn.recv(64).decode('UTF-8')
        if msg_l:
            msg = conn.recv(int(msg_l)).decode('UTF-8')
        return msg
    def listen_for_connect(self,port):

        server_addr = ('0.0.0.0', port)
        server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_soc.bind(server_addr)
        server_soc.listen()
        conn, addr = server_soc.accept()
        #print('connect from ' + str(addr))
        return conn, addr
    def disconnect(self,conn,addr):
        conn.close()
        #print(f'disconnect from {addr}')
    def get_host_addr(self):
        server = socket.gethostbyname(socket.gethostname())
        return server

class client():
    def send(self,msg):
        message = msg.encode('UTF-8')
        send_l = str(len(message)).encode('UTF-8')
        send_l += b' ' * (64 - len(send_l))
        client_soc.send(send_l)
        time.sleep(0.1)
        client_soc.send(message)
    def recv(self):
        msg = client_soc.recv(1024).decode('UTF-8')
        return msg
    def connect_to_server(self,addr,port):
        try:
            client_soc.connect((addr,port))
        except Exception as e:
            print(e)
    def disconnect(self):
        client.send('!disconnect')
    def get_host_addr(self):
        server = socket.gethostbyname(socket.gethostname())
        return server