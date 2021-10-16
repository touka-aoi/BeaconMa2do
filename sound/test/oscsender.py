import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="192.168.128.101")
    parser.add_argument("--port", type=int, default=7000)
    args = parser.parse_args()

    client = udp_cliepadnt.SimpleUDPClient(args.ip, args.port)
    while True:
        client.send_message("/command", input())