import socket
import time
from datetime import datetime

HOST_IP = "172.20.10.6" # 接続するサーバーのIPアドレス
PORT = 10000 # 接続するサーバーのポート
DATESIZE = 1024  # 受信データバイト数

class SocketClient():

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def send_recv(self, input_data):        
        print('[{0}] input data : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), input_data) )
        # 入力データをサーバーへ送信
        sock.send(input_data.encode('utf-8'))

if __name__ == '__main__':

    client = SocketClient(HOST_IP, PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ソケットをオープンにして、サーバーに接続
    sock.connect((HOST_IP, PORT))
    while True:
        input_data = input("send data:") # ターミナルから入力された文字を取得
        client.send_recv(input_data)