from device import Device
import machine
import utime
dev=Device()
dev.connect_to_lora()
dev.send_data()