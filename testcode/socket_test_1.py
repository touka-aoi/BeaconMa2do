import socket
import time
from datetime import datetime

HOST1 = '172.20.10.6'
#HOST2 = "10.200.162.82"
PORT = 10000

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    senddata = input()
    client.sendto(senddata.encode('utf-8'),(HOST1,PORT))
    #client.sendto(senddata.encode('utf-8'),(HOST2,PORT))
    print('[{0}] input data : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), senddata))