#-*-coding:utf-8-*-

# 필요한 라이브러리를 불러옵니다. 
import RPi.GPIO as GPIO
import time

#서보모터를 PWM으로 제어할 핀 번호 설정 
SERVO_PIN = 13

button_pin = 15


# 불필요한 warning 제거
GPIO.setwarnings(False)

# GPIO핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM)

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 서보핀의 출력 설정 
GPIO.setup(SERVO_PIN, GPIO.OUT)

# PWM 인스턴스 servo 생성, 주파수 50으로 설정 
servo = GPIO.PWM(SERVO_PIN,50)
# PWM 듀티비 0 으로 시작 
servo.start(0)

open = False

def button_callback(channel):
    global open    # Global 변수선언 
    if open == False: 
        servo.ChangeDutyCycle(7.5)  # 90도 
    else:                                # LED 불이 져있을때 
        servo.ChangeDutyCycle(2.5)  # 0도 
    open = not open  # False <=> True

GPIO.add_event_detect(button_pin,GPIO.RISING,callback=button_callback, bouncetime=300)      
        
while 1:
    time.sleep(0.1)  # 0.1초 딜레이

