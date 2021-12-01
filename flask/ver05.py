# 웹서버 프로그램 웹 브라우저에서 http://localhost:5000/led?state=on 과 같은 형식으로 접근 (get 방식)
# 이렇게 하여 LED 작동시킴
from flask import Flask, request
import RPi.GPIO as GPIO

app = Flask(__name__)

LED = 12
GPIO.setmode(GPIO.BCM)        #BOARD는 커넥터 pin번호 사용
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

@app.route("/")
def helloworld():
    return "Hello World"

@app.route("/led")
def led():
    state = request.args.get("state")       # URL에 ?state=on 과 같은 형식으로 쿼리 전달 (get 방식)
    if state == 'on':
        GPIO.output(LED, GPIO.HIGH)
    else:
        GPIO.output(LED, GPIO.LOW)
    return "LED " + state

@app.route("/gpio/cleanup")
def gpio_cleanup():
    GPIO.cleanup()
    return "GPIO CLEANUP" 

if __name__ == "__main__":
    app.run(host="0.0.0.0")