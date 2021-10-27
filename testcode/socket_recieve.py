import socket
M_SIZE = 1024
UDP_IP = "172.20.10.6"
UDP_PORT = 9000


sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)

sock.bind((UDP_IP, UDP_PORT))
message, cli_addr = sock.recvfrom(M_SIZE)
message = message.decode(encoding='utf-8')
print(message)