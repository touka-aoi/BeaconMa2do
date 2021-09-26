##インポート##
import asyncio #非同期
from bleak import BleakScanner #Bluetooth
from pythonosc.udp_client import SimpleUDPClient #OSC


# 変数宣言 #
#OSC
ip = "127.0.0.1" #IPアドレス
port = 1337 #ポート番号

#ビーコン
#MACアドレス
mac = "E3:AF:50:99:24:50"

# クライアント作成 #
client = SimpleUDPClient(ip, port)  # Create client

#