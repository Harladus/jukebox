import time
import serial
import RPi.GPIO as GPIO
import random
import pygame
from os import walk
from time import sleep
mapje = None
counter = 0
stringCounter = 0
x = 0
randomarray = []
queueArray = []
stringsartists = [] #Array of folder names to navigate to
artistcount = 0;
artists = []
t = open("/media/pi/F805-2EB1/tags.txt", "r") #For all ID's in the text file
tags = t.readlines()                          #Put them in a list
tags = [x.strip() for x in tags]              #Delete white spaces, like \n
for tag in tags:
    if tag == '':
        tagindex = tags.index(tag)
        del tags[tagindex]
print(tags)
for (dirpath, dirnames, filenames) in walk("/media/pi/F805-2EB1/Muziekjes"):
    if len(dirnames) != 0:
        maximum = len(dirnames)-1
    stringsartists.extend(dirnames)
    artistcount += 1
    if artistcount != maximum:
        artists.append([])
print(stringsartists)
print(artists)

GPIO.setmode(GPIO.BCM)

IN1 = 6
IN2 = 13
IN3 = 19
IN4 = 26
inputs = [IN1,IN2,IN3,IN4]
for pins in inputs:
    GPIO.setup(pins,GPIO.OUT)    
    GPIO.output(pins,False)

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


for people in stringsartists:                                                                   #For all songs that there are per artist
    for (dirpath, dirnames, filenames) in walk("/media/pi/F805-2EB1/Muziekjes/"+people):
        artists[counter].extend(filenames)                                                            #Add them to the arraylist
        print(artists[counter])
        break
    counter += 1

PortRF = serial.Serial('/dev/ttyS0', 9600)              #Serial communication for RFID reader

pygame.mixer.init()                                     #Initialize mixer
pygame.mixer.set_num_channels(1)                        #Make sure there is one channel to play from

playing_ID = ""
ID = ""

def queue():
    stepCounter = 0
    pos = pygame.mixer.music.get_pos()                  #Check for how long the song is running
    stop = 0
    while stop == 0:
        pos = pygame.mixer.music.get_pos()
        if int(pos) == -1 and len(queueArray) > 0:
            pygame.mixer.music.load(queueArray.pop())       #Get next element from the queue 
            pygame.mixer.music.play()
        elif int(pos) == -1 and len(queueArray) == 0:
            stop = 1
        for pin in range(0,3):
            xpin = inputs[pin]
            if seq[stepCounter][pin] != 0:
                GPIO.output(xpin,True)
            else:
               GPIO.output(xpin,False)
        stepCounter += 1
        if stepCounter == stepCount:
            stepCounter = 0
        if stepCounter < 0:
            stepCounter = stepCount
        sleep(time)
        doublecheck()

def play_music(playing_ID):
    mapje = None
    found = 0
    if pygame.mixer.get_busy():
        pygame.mixer.music.stop()
    first = True
    for tag in tags:
        if tag == playing_ID:
            mapje = tags.index(tag)
            print(artists[mapje])
            found = 1
            break
    if found == 0:
        with open("/media/pi/F805-2EB1/tags.txt", "a") as t:
            if len(tags) < len(artists):
                mapje = len(tags)
                t.write(playing_ID+"\n")
                tags.extend(playing_ID)
                print(artists[mapje])
            else:
                print("Not found, no muziekjes left")
    if mapje is not None:
        randnums = random.sample(range(0, len(artists[mapje])-1), len(artists[mapje])-1)                                    #Generate a random order of songs
        print(randnums)
        for number in randnums:
            if first == True:
                pygame.mixer.music.load("/media/pi/F805-2EB1/Muziekjes/"+stringsartists[mapje]+"/"+artists[mapje][number])     #Load the first song in
                print(artists[mapje][number])
                print(pygame.mixer.get_num_channels())
                pygame.mixer.music.play()
                first = False
            else:
                queueArray.append("/media/pi/F805-2EB1/Muziekjes/"+stringsartists[mapje]+"/"+artists[mapje][number])          #Load the rest of the songs in the queue
        print(stringsartists[mapje])

def check():
    global playing_ID
    global ID
    while True:
        if PortRF.in_waiting > 0:
            read_byte = PortRF.read()
            if read_byte == "\x02":
                ID = ""
                for Counter in range(12):
                    read_byte=PortRF.read()
                    ID = ID+str(read_byte)
            if ID != playing_ID:
                playing_ID = ID
                play_music(playing_ID)
                queue()

def doublecheck():
    global playing_ID
    global ID
    global queueArray
    if PortRF.in_waiting > 0:
            read_byte = PortRF.read()
            if read_byte == "\x02":
                ID = ""
                for Counter in range(12):
                    read_byte=PortRF.read()
                    ID = ID+str(read_byte)
            if ID != playing_ID:
                queueArray = []
                playing_ID = ID
                play_music(playing_ID)
                queue()

check()



