import asyncio
from bleak import BleakScanner
from Windows.Devices.Bluetooth.Advertisement import BluetoothLEAdvertisementFilter, BluetoothLEAdvertisement
from System import Guid

adv_filter = BluetoothLEAdvertisementFilter()
adv_filter.Advertisement = BluetoothLEAdvertisement()
adv_filter.Advertisement.ManufacturerData = b'\x02\x15\xe0,\xc2^\x00IA\x85\x83,:e\xdbu]\x01\x0b\xb8\x04\x04\xb5'

#MACはGATTっぽいからその手前のUUIDとかではじかないとだめっぽいな