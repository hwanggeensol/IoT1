from tkinter import *
frame = Tk()

import picamera
import time
from PIL import Image

def take():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_preview()
        time.sleep(1)
        camera.capture('cos.jpg')
        camera.stop_preview()

def show():
    a = Image.open('cos.jpg')
    a.show()
    
button1 = Button(frame, command=take, text="Take Picture")
button1.pack()

button2 = Button(frame, command=show, text="Show Picture")
button2.pack()


frame.mainloop()