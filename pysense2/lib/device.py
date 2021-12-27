import socket
import _thread
from SI7006A20 import SI7006A20
from pycoproc_1 import Pycoproc
from LTR329ALS01 import LTR329ALS01
import binascii
import time
from ultrason import Ultrason
from machine import I2C
from network import LoRa
import json

class Device:
    def __init__(self):
        self.py= Pycoproc(Pycoproc.PYSENSE)
        self.sensorTH = SI7006A20(self.py)
        self.sensorLight= LTR329ALS01(self.py)
        self.out=0
    def connect_to_lora(self):
        lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
        DevEUI = binascii.unhexlify('70B3D57ED0048B75')
        AppEUI = binascii.unhexlify('0000000000000000')
        AppKey = binascii.unhexlify('FBD732E768272F9CF5E5F9EBC4BDC324')
        lora.join(activation=LoRa.OTAA, auth=(DevEUI, AppEUI, AppKey),timeout=0)
        while not lora.has_joined():
            time.sleep(2.5)
            print("Not joined yet")
        print("Joined")
    def send_data(self):
        _thread.start_new_thread(Ultrason.callback,())
        while True:
            out= socket.socket(socket.AF_LORA, socket.SOCK_RAW)
            out.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
            temp= round(self.sensorTH.temperature())
            humidity = round(self.sensorTH.humidity())
            light_b = self.sensorLight.light()[0]
            light_r = self.sensorLight.light()[1]
            data = str(temp)+str(humidity)+str(light_b)+str(Ultrason.number)
            out.send(data)
            print('done')
            time.sleep(20)
            

        

