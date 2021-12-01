#-*-coding:utf-8-*-

# 필요한 라이브러리를 불러옵니다. 
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#센서에 연결한 Trig와 Echo 핀의 핀 번호 설정 
TRIG = 23
ECHO = 24
print("Distance measurement in progress")

# GPIO 18번 핀을 출력으로 설정 
GPIO.setup(18, GPIO.OUT)

# PWM 인스턴스 p를 만들고  GPIO 18번을 PWM 핀으로 설정, 주파수  = 100Hz
p = GPIO.PWM(18, 100)  

# 사용할 GPIO핀의 번호를 선정합니다.(BCM 모드)
led_pin = 12     #GPIO12

# LED 핀의 IN/OUT 설정
GPIO.setup(led_pin, GPIO.OUT)

#Trig와 Echo 핀의 출력/입력 설정 
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

#Trig핀의 신호를 0으로 출력 
GPIO.output(TRIG, False)
print("Waiting for sensor to settle")
time.sleep(2)

p.start(10)  # PWM 시작 , 듀티사이클 10 (충분)

try:
    while True: 			     
        GPIO.output(TRIG, True)   # Triger 핀에  펄스신호를 만들기 위해 1 출력
        time.sleep(0.00001)       # 10µs 딜레이 
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO)==0:
            start = time.time()	 # Echo 핀 상승 시간 
        while GPIO.input(ECHO)==1:
            stop = time.time()	 # Echo 핀 하강 시간 
            
        check_time = stop - start
        distance = check_time * 34300 / 2
        time.sleep(0.4)	# 0.4초 간격으로 센서 측정 

        if distance <= 30:
            p.start(10)  # PWM 시작 , 듀티사이클 10 (충분)
            GPIO.output(led_pin,1)    # LED ON
            p.ChangeFrequency(262) 
                
        else:
            GPIO.output(led_pin,0)    # GPIO 설정 초기화 
            p.stop()
        
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()


