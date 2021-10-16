import socket

sock =socket.socket(socket.AF_INET,type=socket.SOCK_DGRAM)
sock.bind(("192.168.128.101",8000))

msg = sock.recv(8191)

print(msg)
