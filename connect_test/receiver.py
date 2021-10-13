import socket

M_SIZE = 8192
HOST = "10.205.119.99"
PORT = 9000

sock =socket.socket(socket.AF_INET,type=socket.SOCK_DGRAM)
sock.bind((HOST,PORT))

mylist = []

while True: #データ受け取りまで
    #受信しない場合はここで止まる
    ##recvfromだったからおわってた
#    print("test")
    message = sock.recv(M_SIZE)
#    print(1)
    message = message.decode("utf-8")
    print(message)
    msg = message.split(":")
    print(msg[2])
    mylist.append(float(msg[2]))
    print( sum(mylist) / len(mylist) )
