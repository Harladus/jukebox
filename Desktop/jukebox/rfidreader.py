import time
import serial
import RPi.GPIO as GPIO
ID = ""
GPIO.setmode(GPIO.BCM)
PortRF = serial.Serial('/dev/ttyS0', 9600)
while True:
    read_byte = PortRF.read()
    if read_byte == "\x02":
        ID = ""
        for Counter in range(12):
            read_byte=PortRF.read()
            ID = ID+str(read_byte)
        print(ID)
