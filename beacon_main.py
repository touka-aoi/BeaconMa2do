import asyncio
import socket
from bleak import BleakScanner
from Windows.Devices.Bluetooth.Advertisement import BluetoothLEAdvertisementFilter, BluetoothLEAdvertisement
import time
import numpy as np

mac = "F5:B1:3A:FE:66:40"
HOST = '10.205.119.99'
PORT = 9000
num = 0 #セントラル番号


def detection_callback(device, advertisement_data):
    if ("77:2F:B8:15:61:5C" == device.address):
        print(device.address, "RSSI:", device.rssi, advertisement_data, "UUIDS :" ,device.metadata["uuids"])
        print(time.time())
        senddata = str(device.rssi)
        client.sendto(senddata.encode('utf-8'),(HOST,PORT))



async def run():
    #BLEDeviceを探索する
    scanner = BleakScanner()
    #デバイスが見つかったときのコールバック関数を登録する 
        #t登録する関数は2つの引数を持つ(device, advetisement_data)
    scanner.register_detection_callback(detection_callback)
    scanner.set_scanning_filter()
    await scanner.start()
    await scanner.stop()


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
loop = asyncio.get_event_loop()
loop.run_until_complete(run())
