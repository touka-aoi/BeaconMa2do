from pythonosc import dispatcher
from pythonosc import osc_server

def processing(unused_addr, command):
    exec(command)
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/command", processing)

server = osc_server.ThreadingOSCUDPServer(("192.168.128.101", 7000), dispatcher)
server.serve_forever()
