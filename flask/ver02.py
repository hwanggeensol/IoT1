# 웹서버 프로그램 웹 브라우저에서 http://localhost:5000/led/on 의 형식으로 접근

from flask import Flask
app = Flask(__name__)           # Flask 서버 객체를 이 모듈로 생성

@app.route("/")                 # 웹에서 적속할 때의 최상위 폴더를 의미
def helloworld():               # 그 폴더를 접근했을 때 실행하는 함수는 바로 밑에 줄에 써 주어야 함
    return "Hello World"

@app.route("/led/on")           # 웹에서 접속할 때 이 경로명을 주면 아래의 함수가 실행됨
def led_on():               
    return "LED ON"

@app.route("/led/off")          # 웹에서 접속할 때 이 경로명을 주면 아래의 함수가 실행됨
def led_off():               
    return "LED OFF"

if __name__ == "__main__":      
    app.run(host="0.0.0.0")     