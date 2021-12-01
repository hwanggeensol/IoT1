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
    p.start(10)  # PWM 시작 , 듀티사이클 10 (충분)

    try:
        for fr in Frq:
            p.ChangeFrequency(fr)    #주파수를 fr로 변경
            time.sleep(speed)
             
    except KeyboardInterrupt:       # 키보드 Ctrl+C 눌렀을때 예외발생 
        pass                       # 무한반복을 빠져나와 아래의 코드를 실행  
    p.stop()                        # PWM을 종료


if __name__ == "__main__":
    app.run(host="0.0.0.0")