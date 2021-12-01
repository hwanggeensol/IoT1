#-*-coding:utf-8-*-

# 필요한 라이브러리를 불러옵니다.
import RPi.GPIO as GPIO 
import time

# 사용할 GPIO핀의 번호를 선정합니다.
button_pin = 15
led_pin1 = 4
led_pin2 = 23
count = 0

 # 불필요한 warning 제거
GPIO.setwarnings(False) 
# GPIO핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM) 
# 버튼 핀의 INPUT설정 , PULL DOWN 설정 
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# LED 핀의 OUT설정
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)

# button_callback 함수를 정의합니다.
def button_callback(channel):
    global count
    count = count+1

    if count == 1:  # LED 불이 꺼져있을때 
        GPIO.output(led_pin1,1)   # LED ON 
        GPIO.output(led_pin2,0)
        print("LED1 ON!")
    elif count == 2:       
        GPIO.output(led_pin1,1)                        
        GPIO.output(led_pin2,1)  # LED OFF
        print("LED2 ON!")
    elif count == 3:
        GPIO.output(led_pin1,0)  # LED OFF
        GPIO.output(led_pin2,0)  # LED OFF
        print("LED1,2 OFF!")
        count = 0


# Event 알림 방식으로 GPIO 핀의 Rising 신호를 감지하면 button_callback 함수를 실행합니다. 300ms 바운스타임을 설정하여 잘못된 신호를 방지합니다.
GPIO.add_event_detect(button_pin,GPIO.RISING,callback=button_callback, bouncetime=300)      
        
while 1:
    time.sleep(0.1)  # 0.1초 딜레이
