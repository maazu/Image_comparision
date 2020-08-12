import PIL
from PIL import Image,ImageTk
import pytesseract
import cv2
from tkinter import *


width, height = 200, 50
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root = Tk()
root.bind('<Escape>', lambda e: root.quit())
lmain = Label(root)
lmain.pack()

def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

show_frame()
root.mainloop()






















'''
def live_footage():
    cap = cv2.VideoCapture(0) 
    count = 0
    success = True
    while success:
        ret, frame = cap.read() 

        # Our operations on the frame come here 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

        # Display the resulting frame 
        cv2.imshow('frame',gray)
        #cv2.imwrite("frame%d.jpg" % count, frame)
        print ('Read a new frame: ', ret)
        count += 1


live_footage()
'''
