
import numbers
from tkinter import *
from tkinter import ttk
import RPi.GPIO as GPIO 
import time
import threading
import picamera
from PIL import Image

frame = Tk()
frame.title("HOME")
frame.geometry("300x500")

BELL = 15   # 초인종 버튼 - 스위치
LED = 12    # 초인종 불 - Led
MUSIC = 18  # 초인종 소리 - 부저
DOOR = 13   # 문 잠금장치 - 모터
L1 = 16     # 거실
L2 = 20     # 큰방
L3 = 21     # 작은방

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 
GPIO.setup(BELL, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT, initial = GPIO.LOW) 
GPIO.setup(MUSIC, GPIO.OUT)
mu = GPIO.PWM(18, 100)
GPIO.setup(DOOR, GPIO.OUT)
do = GPIO.PWM(13,50)
GPIO.setup(L1, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(L2, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(L3, GPIO.OUT, initial = GPIO.LOW)

led = False
btn = False

music_fr = [440, 440, 262, 440, 392, 349, 330, 349, 466, 466, 466,
            440, 440, 277, 440, 392, 349, 330, 349, 392, 392, 392]

fList = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg",
         "6.jpg", "7.jpg", "8.jpg", "9.jpg"]

# 벨이 눌리면 
# 부저, LED, 카메라 작동
def button_callback(channel):
    filename = time.strftime("%Y%m%d-%H%M%S")  
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_preview()
        time.sleep(1)
        camera.capture(str(filename)+'.jpg')
        camera.stop_preview()

    t1 = threading.Thread(target=Musicctl)
    t1.start()
    for i in range(20):
        GPIO.output(LED,1)    
        time.sleep(0.1)   
        GPIO.output(LED,0)   
        time.sleep(0.1)     

def Musicctl():
    mu.start(10)
    for j in music_fr:
        mu.ChangeFrequency(j)
        time.sleep(0.2)
    mu.stop()

GPIO.add_event_detect(BELL,GPIO.RISING,callback=button_callback)

# 방문자
# 방문객 목록 보기
def visitor():
    btn=Button(frame, text='종료', command=quit)
    btn.pack()

# 제어
# 거실, 안방, 작은방 조명 제어
def control():
    la1.pack()
    btn1.pack(side=LEFT)

    la2.pack()
    btn2.pack(side=TOP)

    la3.pack()
    btn3.pack(side=LEFT)

def led1():
    global led
    if led == False:
        btn1.config(text="Led OFF")
        GPIO.output(L1,1)
    else:
        btn1.config(text="Led ON")
        GPIO.output(L1,0)
    led = not led

def led2():
    global led
    if led == False:
        btn2.config(text="Led OFF")
        GPIO.output(L2,1)
    else:
        btn2.config(text="Led ON")
        GPIO.output(L2,0)
    led = not led

def led3():
    global led
    if led == False:
        btn3.config(text="Led OFF")
        GPIO.output(L3,1)
    else:
        btn3.config(text="Led ON")
        GPIO.output(L3,0)
    led = not led

# 버튼
label1=Label(frame, text="HOME")
label1.pack()

button1=ttk.Button(frame, text="방문자", command=visitor)
button1.grid(row=1, column=0)
button2=Button(frame, command=control, text="제어")
button2.pack()

la1=Label(frame, text="거실")
la2=Label(frame, text="안방")
la3=Label(frame, text="작은방")

btn1=Button(frame, command=led1, text="LED ON")
btn2=Button(frame, command=led2, text="LED ON")
btn3=Button(frame, command=led3, text="LED ON")

frame.mainloop()