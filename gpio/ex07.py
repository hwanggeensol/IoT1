import RPi.GPIO as GPIO

import time

from tkinter import *  

import spidev

frame=Tk()

 

# 불필요한 warning 제거, GPIO핀의 번호 모드 설정

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

 

led_pin = 12

# GPIO 18번 핀을 출력으로 설정

GPIO.setup(led_pin, GPIO.OUT)

 

# GPIO 18번 핀을 출력으로 설정 

GPIO.setup(18, GPIO.OUT)

# PWM 인스턴스 p를 만들고  GPIO 18번을 PWM 핀으로 설정, 주파수  = 100Hz

p = GPIO.PWM(18, 100)  

 

# 4옥타브 도~시 , 5옥타브 도의 주파수 

Frq=[392, 392,440,440,392,392,330,330,    392,392,330,330,294,294, 294,294,       392, 392,440,440,392,392,330,330,       392,330,294,330,262,262,262]

 

speed = 0.5 # 음과 음 사이 연주시간 설정 (0.5초)

 

 

# boolean 변수 설정 

light_on = False

music_on = False

 

def ledon():                                

    try:

       global light_on    # Global 변수선언 

       if light_on == False:  # LED 불이 꺼져있을때 

           GPIO.output(led_pin,1)   # LED ON 

           button1.config(text="LED OFF")

       else:                                # LED 불이 져있을때 

           GPIO.output(led_pin,0)  # LED OFF

           button1.config(text="LED ON")

       light_on = not light_on  # False <=> True

    except:

        print("\n뭔가 잘못된 경우입니다. 다시입력하세요.")

 

def musicon():                                

    try:

        global music_on

        if music_on==False:

           button2.config(text="MUSIC OFF")

           p.start(10) 

           for fr in Frq:

                p.ChangeFrequency(fr)    #주파수를 fr로 변경

                time.sleep(speed)       #speed 초만큼 딜레이 (0.5s) 

                

           

        else:

            button2.config(text="MUSIC ON")

            p.stop()                        # PWM을 종료

            time.sleep(speed)

        music_on = not music_on  # False <=> True

    except:

        print("\n뭔가 잘못된 경우입니다. 다시입력하세요.")

 

button1 = Button(frame, command=ledon, text="LED ON")

button1.grid(row=0)

button2 = Button(frame,command=musicon, text="MUSIC ON")

button2.grid(row=2)

 

frame.mainloop()