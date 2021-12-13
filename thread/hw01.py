from tkinter import *
frame = Tk()

import RPi.GPIO as GPIO 
import time

import threading

ledpin = 12

# 불필요한 warning 제거
GPIO.setwarnings(False) 
# GPIO핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM) 
# LED 핀의 OUT설정
GPIO.setup(ledpin, GPIO.OUT)
# GPIO 18번 핀을 출력으로 설정 
GPIO.setup(18, GPIO.OUT)
# PWM 인스턴스 p를 만들고  GPIO 18번을 PWM 핀으로 설정, 주파수  = 100Hz
p = GPIO.PWM(18, 100)
# 4옥타브 도~시 , 5옥타브 도의 주파수 
Frq = [ 392, 392, 440, 440, 392, 392, 330, 330, 392, 392, 330, 330, 294, 294, 294, 294,
        392, 392, 440, 440, 392, 392, 330, 330, 392, 330, 294, 330, 262, 262, 262]
speed = 0.5

led = False
music = False

def led():
    global led
    if led == False:
        button1.config(text="Led OFF")
        GPIO.output(ledpin,1)
    else:
        button1.config(text="Led ON")
        GPIO.output(ledpin,0)
    led = not led

def  musictl():
    global music
    if music == False: 
        t1 = threading.Thread(target=musicon)
        t1.start()
    else:
        t2 = threading.Thread(target=musicoff)
        t2.start()
   


def musicoff():
    global music
    music = not music
    button2.config(text="Music ON")
    p.stop()
    time.sleep(speed)
      

   
def musicon():
    global music
    music = not music
    button2.config(text="Music OFF")

 
    p.start(10)  # PWM 시작 , 듀티사이클 10 (충분)
    while 1:
        for fr in Frq:
            lock.acquire()
            p.ChangeFrequency(fr)    #주파수를 fr로 변경
            time.sleep(speed)
            lock.release()
   


button1 = Button(frame, command=led, text="Led ON")
button1.pack()

button2 = Button(frame, command=musictl, text="Music ON")
button2.pack()

lock = threading.Lock()

frame.mainloop()