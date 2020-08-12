import tkinter
from tkinter import *
from tkinter import filedialog
import os
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mbox
import cv2
from store_images import *


def add_new_route_page(self):
    cv2.destroyAllWindows()  
    #refresh the right side GUI
    self.root.update()
    
    rightframe = Frame(self.root,bg='black')
    rightframe.pack(side = RIGHT)  
    rightframe.place(height=800, width=800, x=200, y=0)
    #heading label
    top_heading = Label(rightframe, text="Insert New Bus Route", font=("Helvetica", 16),bg ='black',fg = 'WHITE')
    top_heading.place(x=10, y = 20)
    # description label
    desc_label = Label(rightframe, text="Please Upload a new video, the video submitted here will be processed into frames and will create a new database of images, \nthat particular bus route ", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    desc_label.place(x=10, y = 58)
 
    #video label
    route_vid_label = Label(rightframe, text=" Route Video Name", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    route_vid_label.place(x=10, y = 120)

    global video_name_text_box 
    video_name_text_box = Entry(rightframe)
    video_name_text_box.place(x = 150, y = 120,width = 590)  

    video_location_label = Label(rightframe, text="Route Video Location", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    video_location_label.place(x=10, y = 160)
   
    global video_location_text_box
    video_location_text_box = Entry(rightframe)
    video_location_text_box.place(x = 150, y = 160,width = 590)  


    Browse_video_button = Button(rightframe, text="Load Video", width = 15,command = lambda:openVideo(self) )
    Browse_video_button.place(x = 625, y = 200)


    next_step_button = Button(rightframe, text=" Next ",width = 15,command = lambda:upload_route(self) )
    next_step_button.place(x = 625, y = 600)
    

    

# Open a video file
def openVideo(self):
        fullfilename = filedialog.askopenfilename(initialdir="//Gui", title="Select a file", filetypes=[("Video file", "*.mp4; *.avi ")]) # select a video file from the hard drive
        if(fullfilename != ''):
             video_location_text_box.delete(0,END)
             video_location_text_box.insert(0,fullfilename)
      
    

def field_validation():
    if(video_name_text_box.get() == ''):
        mbox.showerror("Missing Route Name","Route Name Missing")
        return False
    elif(video_location_text_box.get() == ''):
        mbox.showerror("Missing File Path","video path is missing")
        return False
    return True


def upload_route(self):
    if(field_validation()):
        video_details(self,str(video_location_text_box.get()),str(video_name_text_box.get()))


