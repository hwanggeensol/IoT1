#-*-coding:utf-8-*-

#-*-coding:utf-8-*-

import spidev
import time
import RPi.GPIO as GPIO
import time

# 불필요한 warning 제거,  GPIO핀의 번호 모드 설정
GPIO.setwarnings(False)  
GPIO.setmode(GPIO.BCM)

# GPIO 18번 핀을 출력으로 설정 
GPIO.setup(12, GPIO.OUT)  
# PWM 인스턴스 p를 만들고  GPIO 18번을 PWM 핀으로 설정, 주파수  = 50Hz
p = GPIO.PWM(12, 50) 

p.start(0)

delay = 0.5

pot_channel = 0

spi = spidev.SpiDev()

spi.open(0,0)
spi.max_speed_hz = 1000000

def readadc(adcnum):
    if adcnum > 7 or adcnum < 0:
        return -1
    
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1]&3)<< 8)+r[2]
    return data
    
try:               
    while 1:   
        p.ChangeDutyCycle(readadc(pot_channel)/100)     # dc의 값으로 듀티비 변경  
        time.sleep(0.1)                  #  0.1초 딜레이       
except KeyboardInterrupt:   # 키보드 Ctrl+C 눌렀을 때 예외발생 
    pass                   # 무한반복을 빠져나와 아래의 코드를 실행  
p.stop()                    # PWM을 종료
GPIO.cleanup()
