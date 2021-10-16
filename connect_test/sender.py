import socket
import time
from datetime import datetime


HOST = '192.168.128.101'
PORT = 8000

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    senddata = input()
    client.sendto(senddata.encode('utf-8'),(HOST,PORT))
    print('[{0}] input data : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), senddata))