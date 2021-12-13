# 웹서버 프로그램 웹 브라우저에서 http://localhost:5000/로 접속하면 
# index.html을 실행하고 버튼을 이용하여 LED 작동시킴

from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)                    #BOARD는 커넥터 pin번호 사용
LED=12                                       # 7번 pin. 즉, GPIO4 사용
MUSIC=18
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
p = GPIO.PWM(18, 100)
pin = False

DOOR = 13
GPIO.setup(DOOR, GPIO.OUT)
do = GPIO.PWM(DOOR,50)

Frq = [ 392, 392, 440, 440, 392, 392, 330, 330, 392, 392, 330, 330, 294, 294, 294, 294,
        392, 392, 440, 440, 392, 392, 330, 330, 392, 330, 294, 330, 262, 262, 262]
speed = 0.5

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/led")                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def led():
    try:
        global pin
        if(pin == False):
            GPIO.output(LED, GPIO.HIGH)         # 불을 켜고
            pin = not pin 
            return "on" 
        else:
            GPIO.output(LED, GPIO.LOW)
            pin = not pin 
            return "off" 
    except :
        return "fail"


@app.route("/music")
def music():
    try:
        do.start(0)
        do.ChangeDutyCycle(7.5)
        time.sleep(3)
        do.ChangeDutyCycle(2.5)
        time.sleep(1)
    except:
        pass
    do.stop()
    GPIO.cleanup()


if __name__ == "__main__":
    app.run(host="0.0.0.0")