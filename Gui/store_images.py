import os
import time
import uuid
from itertools import cycle
import cv2
import tkinter
from tkinter import *
import threading

def video_details(self,video_path,video_name):
    
    self.root.update()
    rightframe = Frame(self.root,bg='black')
    rightframe.pack(side = RIGHT)  
    rightframe.place(height=800, width=800, x=200, y=0)
    top_heading = Label(rightframe, text="Route Header Details", font=("Helvetica", 16),bg ='black',fg = 'WHITE')
    top_heading.place(x=10, y = 20)

   
    global vidcap,fps,total_frame,duration,route_name
    vidcap = cv2.VideoCapture(video_path)
    # detects the rate
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    total_frame = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = float(total_frame) / float(fps)

    
    #labels
    route_name_label = Label(rightframe, text="Route Name", font=("Helvetica", 14),bg ='black',fg = 'WHITE')
    route_name_label.place(x=10, y = 60)
    frame_rate_label = Label(rightframe, text="Frame rate p/s", font=("Helvetica", 14),bg ='black',fg = 'WHITE')
    frame_rate_label.place(x=10, y = 90)
    total_frames_label = Label(rightframe, text="Total Frames", font=("Helvetica", 14),bg ='black',fg = 'WHITE')
    total_frames_label.place(x=10, y = 120)
    video_duration_label = Label(rightframe, text="Video Duration", font=("Helvetica", 14),bg ='black',fg = 'WHITE')
    video_duration_label.place(x=10, y = 150)
    
    
    #values 
    route_name = Label(rightframe, text = str(video_name), font=("Helvetica", 14),bg ='black',fg = 'WHITE')
    route_name.place(x=150, y = 60)
    frame_rate = Label(rightframe, text= str(fps), font=("Helvetica", 14),bg ='black',fg = 'WHITE')
    frame_rate.place(x=150, y = 90)
    total_frames = Label(rightframe, text= str(total_frame), font=("Helvetica", 14),bg ='black',fg = 'WHITE')
    total_frames.place(x=150, y = 120)
    video_duration = Label(rightframe, text= str(duration), font=("Helvetica", 14),bg ='black',fg = 'WHITE')
    video_duration.place(x=150, y = 150)


    global status_window
    status_window = tkinter.Text(rightframe, height=25, width=80)
    status_window.place(x=10, y = 190)


    global next_step_button
    next_step_button = Button(rightframe, text=" Store Images ",width = 15,command = lambda:break_video(str(video_name)))
    next_step_button.place(x = 650, y = 600)

    print('Frame rate per second = ' + str(fps))
    print('Total Number of frames = ' + str(total_frame))
    print('Total duration of Video in Seconds = ' + str(duration))



def getFrame(sec,count,path_name):    
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite(os.path.join(path_name , 'train'+str(count)+'.jpg'), image)
        status = "Frame number "+str(count)+ " Added in file directoy "+path_name+ "\n"
        status_window.insert(tkinter.END, status)
        status_window.see("end")
    return hasFrames


def break_video(video_path):
    status_window.insert(tkinter.END, "Please wait few seconds processing the video.\n")
    print( "Please wait few seconds processing the video.")
    os.mkdir(video_path)
    path_name = video_path + "\\"
    sec = 0
    frameRate =  0.5 #//it will capture image in each 0.5 second
    count=10
    success = getFrame(sec,count,path_name)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 1)
        success = getFrame(sec,count,path_name)
       
  
    status_window.insert(tkinter.END, "End of the Video.\n")
    status_window.insert(tkinter.END, "Video Processed Successfully.")
