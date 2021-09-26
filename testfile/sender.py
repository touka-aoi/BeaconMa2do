import socket
import time
from datetime import datetime


HOST = '10.200.162.83'
PORT = 10000

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    senddata = input()
    client.sendto(senddata.encode('utf-8'),(HOST,PORT))
    print('[{0}] input data : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), senddata))