from digi.xbee.devices import XBeeDevice
"""
Modify the device_url based on your port name
For Windows, go to Device Manage > Ports (typically COM7)
For Mac, do ‘ls /dev/cu.*’ in terminal (typically /dev/cu.usbserial-00000000)
For RPi, do ‘ls /dev/ttyUSB*’ in terminal (typically /dev/ttyUSB0)
"""
device_url = "COM9"
device = XBeeDevice(device_url, 9600)
device.open()
while True:
 xbee_message = device.read_data()
 if xbee_message:
  data = xbee_message.data
  sender = xbee_message.remote_device
  timestamp = xbee_message.timestamp
  msg = """{time} from {sender}\n{data}""".format(time=timestamp, sender=sender,
  data=data.decode('UTF8'))
  print(msg)
device.close()