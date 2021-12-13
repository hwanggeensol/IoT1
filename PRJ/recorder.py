from tkinter import *
from time import *

fList = ["jeju1.gif", "jeju2.gif", "jeju3.gif", "jeju4.gif", "jeju5.gif",
         "jeju6.gif", "jeju7.gif", "jeju8.gif", "jeju9.gif"]

photoList = [None]*9
num = 0

def clickNext():
    global num
    num += 1
    if num > 8:
        num = 0
    photo = PhotoImage(file="../CookPython/gif/"+fList[num])
    pLabel.configure(image=photo)
    pLabel.image = photo

def clickPrev():
    global num
    num -= 1
    if num < 0:
        num = 8
    photo = PhotoImage(file="../CookPython/gif/"+fList[num])
    pLabel.configure(image=photo)
    pLabel.image = photo

w = Tk()
w.geometry("700x500")
w.title("앨범 보기")

btnPrev = Button(w, text="<< 이전", command=clickPrev)
btnNext = Button(w, text="다음 >>", command=clickNext)

photo = PhotoImage(file="../CookPython/gif/"+fList[0])
pLabel = Label(w, image=photo)

btnPrev.place(x=250, y=10)
btnNext.place(x=400, y=10)
pLabel.place(x=15, y=50)

w.mainloop()