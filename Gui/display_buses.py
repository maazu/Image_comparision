import os
import sys
import cv2
import glob
import time
import imageio
import threading
import numpy as np
import tkinter as tk
from tkinter import *
from pathlib import Path
from PIL import Image, ImageTk
from roi import structual_similarity
from roi import look_for_features
from roi import detect_features
from roi import compare_features




def calucat_sim_in_from_databse(region_from_video,rightframe,frame_number):
    region_len = list(glob.glob(os.path.join('previous_detected_regions','*.png')))
    train_dir = "previous_detected_regions\\"
    print(region_from_video)
    similarity_score = {}   
    for file in range(10,50):
        previously_detected_region = os.path.join(train_dir, "detect_region"+str(file)+".png")
        #print(structual_similarity(previously_detected_region,region_from_video))
        found_sim = structual_similarity(previously_detected_region,region_from_video)
        print(previously_detected_region,region_from_video)
        similarity_score[previously_detected_region] = found_sim
        #print(compute_features(img1,img2))
        

    maximum = max(similarity_score, key=similarity_score.get)  # Just use 'min' instead of 'max' for minimum.
    print(maximum, similarity_score[maximum])
  
        
    image_from_databse = Image.open(maximum)
    render = ImageTk.PhotoImage(image_from_databse)
    db_img_label = Label(rightframe, image = render,width = 200, height = 200)
    db_img_label.image = render
    db_img_label.place(x=560, y = 460)
    print('image updated')
   
   


def look_for_image_in_database(detected_region_from_video,rightframe,frame_number):
    print('looking for query in the database......')
    time.sleep(1)
    print('finding the best matching img.....')
    calucat_sim_in_from_databse(detected_region_from_video,rightframe,frame_number)



def update_Video_img_on_gui(detected_region_img,rightframe,frame_number):
    print('GUI update : detected region from video.....')
    img_from_video = Image.open(detected_region_img)
    render = ImageTk.PhotoImage(img_from_video)
    live_img_label = Label(rightframe, image = render,width = 200, height = 200)
    live_img_label.image = render
    live_img_label.place(x=50, y = 460)
    print('GUI Request: Requesting next region.....')
    detected_region_from_video = detected_region_img
    print('looking for following image in image database :', detected_region_from_video)
    look_for_image_in_database(detected_region_from_video,rightframe,frame_number)


def get_roi_from_video(video_img_from_frame,rightframe,frame_number):
    print('image passed succesfully')
    print(video_img_from_frame)
    ## step 1 calling function from ROI.PY
    print('looking for featutes and region in the image')
    look_for_features(video_img_from_frame,frame_number)##### looking for the features and saving in the detected regions directory    
    path = 'detected_regions\\'  
    detected_region_img = os.path.join(path , 'detect_region'+str(frame_number)+'.png') ## path of the detected img
    print('detection completed.....')
    print('saving the region......')
    print(detected_region_img)
    update_Video_img_on_gui(detected_region_img,rightframe,frame_number)
   
    


    
def display_buses(self):
    self.root.update()
   
    global video

    video_name = "test_videos\\train1.mp4" #This is your video file path
    video = imageio.get_reader(video_name)
    
    rightframe = Frame(self.root,bg='black')
    rightframe.pack(side = RIGHT)  
    rightframe.place(height=800, width=800, x=200, y=0)

    top_heading = Label(rightframe, text="Live Bus Footage", font=("Helvetica", 16),bg ='black',fg = 'WHITE')
    top_heading.place(x=10, y = 5)

    desc_text = Label(rightframe, text="The video which is used in this is an example of live footage,in which the program detect each frame from the video and \nsearch it in the database/folder of images", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    desc_text.place(x=10, y = 40)    

    live_region = Label(rightframe, text="Displaying the ROI from Live footage", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    live_region.place(x=50, y = 420)

    database_region = Label(rightframe, text="ROI From Database", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    database_region.place(x=600, y = 420)
    
    # description label
 

    video_label = tk.Label(rightframe)
    video_label.pack()
     
    thread = threading.Thread(target=stream, args=(video_label,rightframe,))
    thread.daemon = 1
    thread.start()
    
 
    

def stream(label,rightframe):
    path = 'captured_frames\\'
    frame_number = 100
    for image in video.iter_data():
        frame_image = ImageTk.PhotoImage(Image.fromarray(image))
        label.place(x=50, y = 80)
        label.config(image=frame_image)
        label.image = frame_image
        #print(image)
        if(frame_number % 10 == 0):
            numpy_image=np.array(Image.fromarray(image))
            opencv_image=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(os.path.join(path , 'frameCaptured'+str(frame_number)+'.png'), opencv_image)
            print('written image')
            written_image_path = os.path.join(path , 'frameCaptured'+str(frame_number)+'.png') ## writing image in captured frame directory
            get_roi_from_video(written_image_path,rightframe,frame_number) 
            ## delaying video frames by 5 secs
        frame_number +=1  ##updating frame number
       

        
if __name__ == '__main__':
    print('\nshowing live bus tab')

