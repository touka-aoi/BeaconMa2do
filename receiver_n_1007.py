import socket
import csv
import sqlite3
from datetime import datetime


M_SIZE =1024
HOST = ''
PORT = 10000
dbname = "tonokaiyu.db"

sock =socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #AF_INET→ipv4 SOCK_DGRAM→UDP
sock.bind((HOST,PORT))

while True: #データ受け取りまで
    message, cli_addr = sock.recvfrom(M_SIZE)
    message = message.decode('utf-8')  #strで送られてくる
    print(message)  #確認用

    message =message.split("?") #送られてきたstrを?で分割
    print(message) #確認用 この時点ではリスト型っぽい
    
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    #テーブルの作成
    cur.execute("CREATE TABLE IF NOT EXISTS kaiyu (port text, rssi text, xcoord text, ycoord text )")
    cur.execute("INSERT INTO kaiyu VALUES (?,?,?,?)",(message))

    conn.commit()  #これがないと反映されん
    conn.close()
