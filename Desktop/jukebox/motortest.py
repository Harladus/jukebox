import RPi.GPIO as GPIO
from time import sleep
import os
import random

GPIO.setmode(GPIO.BCM)

IN1 = 6
IN2 = 13
IN3 = 19
IN4 = 26
inputs = [IN1,IN2,IN3,IN4]
for pins in inputs:
    GPIO.setup(pins,GPIO.OUT)    
    GPIO.output(pins,False)

stepCounter = 0
time = 0.001 
        

#Defining sequence
stepCount = 8
seq = []
seq = range(0,stepCount)
seq[0] = [1,0,0,0]
seq[1] = [1,1,0,0]
seq[2] = [0,1,0,0]
seq[3] = [0,1,1,0]
seq[4] = [0,0,1,0]
seq[5] = [0,0,1,1]
seq[6] = [0,0,0,1]
seq[7] = [1,0,0,1]

stop = 0
degree = 0
while stop == 0:
    for pin in range(0,3):
        xpin = inputs[pin]
        print(stepCounter,pin)
        if seq[stepCounter][pin] != 0:
            GPIO.output(xpin,True)
        else:
           GPIO.output(xpin,False)
    stepCounter += 1

    if stepCounter == stepCount:
        stepCounter = 0
        degree += 1
    if degree == 360:
        stop = 1
    if stepCounter < 0:
        stepCounter = stepCount
    sleep(time)
GPIO.cleanup()
