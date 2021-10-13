import socket
import csv
from datetime import datetime

M_SIZE =1024
HOST = ''
PORT = 10000

sock =socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #AF_INET→ipv4 SOCK_DGRAM→UDP
sock.bind((HOST,PORT))

while True: #データ受け取りまで
    message, cli_addr = sock.recvfrom(M_SIZE)
    message = message.decode('utf-8')  #strで送られてくる
    print(message)  #確認用

    message =message.split("?") #送られてきたstrを?で分割
    print(message) #確認用 この時点ではリスト型っぽい
    with open("tojozahyo.csv","a")as f: #ファイル内とき勝手に作ってくれる
        writer = csv.writer(f, lineterminator='\n')  #行ごとに改行
        writer.writerow(message)
