import time
import serial
import RPi.GPIO as GPIO
import pygame
ID = ""
songs = ['/home/pi/Desktop/jukebox/moon.mp3', '/home/pi/Desktop/jukebox/fireflies.mp3']
pygame.mixer.init()
counter = 0
playing_ID = ""
GPIO.setmode(GPIO.BCM)

PortRF = serial.Serial('/dev/ttyS0', 9600)

def play_music(playing_ID):
    if playing_ID == "6400AECB5253":
            pygame.mixer.music.load("/home/pi/Desktop/jukebox/moon.mp3")
            pygame.mixer.music.play()
            print("Ik speel nu moon af")
    elif playing_ID == "65005885C870":
            pygame.mixer.music.load("/home/pi/Desktop/jukebox/fireflies.mp3")
            pygame.mixer.music.play()
            print("Ik speel nu fireflies af")
while True:
    read_byte = PortRF.read()
    if read_byte == "\x02":
        ID = ""
        for Counter in range(12):
            read_byte=PortRF.read()
            ID = ID+str(read_byte)
    if ID != playing_ID:
        playing_ID = ID
        play_music(playing_ID)
   






