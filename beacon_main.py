import asyncio
import socket
from bleak import BleakScanner
from Windows.Devices.Bluetooth.Advertisement import BluetoothLEAdvertisementFilter, BluetoothLEAdvertisement

mac = "E3:AF:50:99:24:50"
HOST = '10.200.162.79'
PORT = 10000
num = 0 #セントラル番号


def detection_callback(device, advertisement_data):
    if ("E3:AF:50:99:24:50" == device.address):
        print(device.address, "RSSI:", device.rssi, advertisement_data, "UUIDS :" ,device.metadata["uuids"])
        senddata = str(num) + "?" + str(device.address) + "?" + str(device.rssi)
        client.sendto(senddata.encode('utf-8'),(HOST,PORT))

async def run():
    #BLEDeviceを探索する
    scanner = BleakScanner()
    #デバイスが見つかったときのコールバック関数を登録する 
        #t登録する関数は2つの引数を持つ(device, advetisement_data)
    scanner.register_detection_callback(detection_callback)
    scanner.set_scanning_filter()
    await scanner.start()
    await asyncio.sleep(100000.0) 
    await scanner.stop()


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
loop = asyncio.get_event_loop()
loop.run_until_complete(run())