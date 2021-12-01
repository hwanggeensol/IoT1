#-*-coding:utf-8-*-

# 필요한 라이브러리를 불러옵니다. 
import RPi.GPIO as GPIO
import time

#  노란색 LED, 빨간색 LED, 센서 입력핀 번호 설정 
led_pin = 12
sensor = 6
SERVO_PIN = 13


# 불필요한 warning 제거,  GPIO핀의 번호 모드 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# LED 핀의 IN/OUT(입력/출력) 설정 
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(sensor, GPIO.IN)

# 서보핀의 출력 설정 
GPIO.setup(SERVO_PIN, GPIO.OUT)

# GPIO 18번 핀을 출력으로 설정 
GPIO.setup(18, GPIO.OUT)
# PWM 인스턴스 p를 만들고  GPIO 18번을 PWM 핀으로 설정, 주파수  = 100Hz
p = GPIO.PWM(18, 100)  





# PWM 인스턴스 servo 생성, 주파수 50으로 설정 
servo = GPIO.PWM(SERVO_PIN,50)
# PWM 듀티비 0 으로 시작 
servo.start(0)



print ("PIR Ready . . . . ")
time.sleep(5)  # PIR 센서 준비 시간 


try:
    while True:
        if GPIO.input(sensor) == 1: 	#센서가 High(1)출력 
                GPIO.output(led_pin, 1)   # 노란색 LED 켬 
                servo.ChangeDutyCycle(7.5)  # 90도 
                p.start(10)
                p.ChangeFrequency(262)
                print("Motion Detected !")
                time.sleep(0.2)
                
        if GPIO.input(sensor) == 0:      #센서가 Low(0)출력  
                GPIO.output(led_pin, 0)   # 노란색 LED 끔 
                servo.ChangeDutyCycle(2.5)  # 0도 
                p.stop()     
                time.sleep(0.2)

except KeyboardInterrupt:
                print("Stopped by User")
                GPIO.cleanup()
