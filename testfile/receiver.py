import socket
import time
import pickle
import csv
import pandas as pd
from datetime import datetime

M_SIZE =1024
HOST = '10.200.162.83'
PORT = 10000

sock =socket.socket(socket.AF_INET,type=socket.SOCK_DGRAM)
sock.bind((HOST,PORT))

while True: #データ受け取りまで
    #受信しない場合はここで止まる
    message, cli_addr = sock.recvfrom(M_SIZE)
    print(1)
    message = message.decode("utf-8")
    print(message)