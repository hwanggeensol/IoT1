from flask import Flask, render_template, Response, request 
import spidev
import cv2
import RPi.GPIO as GPIO
import time
import threading
import picamera
import time
from PIL import Image

app = Flask(__name__)
GPIO.setmode(GPIO.BCM) 
vc = cv2.VideoCapture(0)
print(0)

BELL = 15   # 초인종 버튼 - 스위치
LED = 12    # 초인종 불 - Led
MUSIC = 18  # 초인종 소리 - 부저
DOOR = 13   # 문 잠금장치 - 모터
L1 = 16     # 거실
L2 = 20     # 큰방
L3 = 21     # 작은방

GPIO.setwarnings(False)
GPIO.setup(BELL, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT, initial = GPIO.LOW) 
GPIO.setup(18, GPIO.OUT)
mu = GPIO.PWM(18, 100)
GPIO.setup(DOOR, GPIO.OUT)
do = GPIO.PWM(DOOR,50)
GPIO.setup(L1, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(L2, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(L3, GPIO.OUT, initial = GPIO.LOW)

pin1 = False
pin2 = False
pin3 = False
btn = False

music_fr = [440, 440, 262, 440, 392, 349, 330, 349, 466, 466, 466,
            440, 440, 277, 440, 392, 349, 330, 349, 392, 392, 392]


# 벨이 눌리면 
# 부저, LED, 카메라 작동
def button_callback(channel):
    filename=time.strftime("%Y%m%d-%H%M%S")
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


# 웹 실행
# 홈 화면 띄움
@app.route("/")
def home():
    return render_template('home.html')


# 웹에서 방문자를 누르면
# 문 앞 카메라가 실행되면서 밖이 보임
# 문 열림 , 홈으로
@app.route("/visitor")
def visitor():
    return render_template('cam.html')


def gen():
    while True:
        rval, frame = vc.read()
        cv2.imwrite('pic.jpg',frame)
        print(2)
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n'+open('pic.jpg','rb').read()+b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/music")
def music():
    do.start(0)
    do.ChangeDutyCycle(7.5)
    time.sleep(3)
    do.ChangeDutyCycle(2.5)
    time.sleep(1)
    do.stop()
    return "ok"
    

# 웹에서 제어를 누르면
# 집 안 불을 제어할 수 있음
# 거실, 안방, 작은방, 홈으로
@app.route("/control")                      
def control():
    return render_template('ctrl.html')

@app.route("/control/1")
def room1():
    try:
        global pin1
        if(pin1 == False):
            GPIO.output(L2, GPIO.HIGH)      
            pin1 = not pin1 
            return "on" 
        else:
            GPIO.output(L2, GPIO.LOW)
            pin1 = not pin1
            return "off" 
    except :
        return "fail"

@app.route("/control/2")
def room2():
    try:
        global pin2
        if(pin2 == False):
            GPIO.output(L1, GPIO.HIGH)      
            pin2 = not pin2 
            return "on" 
        else:
            GPIO.output(L1, GPIO.LOW)
            pin2 = not pin2 
            return "off" 
    except :
        return "fail"

@app.route("/control/3")
def room3():
    try:
        global pin3
        if(pin3 == False):
            GPIO.output(L3, GPIO.HIGH)      
            pin3 = not pin3 
            return "on" 
        else:
            GPIO.output(L3, GPIO.LOW)
            pin3 = not pin3 
            return "off" 
    except :
        return "fail"







# 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0")




