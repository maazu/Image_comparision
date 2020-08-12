import tkinter
import tkinter
from tkinter import *
from tkinter import filedialog
import os
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mbox
from roi import *

def show_Img_Operation(self):
    cv2.destroyAllWindows()  
    #refresh the right side GUI
    self.root.update()
    
    rightframe = Frame(self.root,bg='black')
    rightframe.pack(side = RIGHT)  
    rightframe.place(height=800, width=800, x=200, y=0)
    #heading label
    top_heading = Label(rightframe, text="Image Operation", font=("Helvetica", 16),bg ='black',fg = 'WHITE')
    top_heading.place(x=10, y = 20)
    # description label
    desc_label = Label(rightframe, text="This tabs allow you to experiment the images by applying different techniques.", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    desc_label.place(x=10, y = 58) 

    image1_location_label = Label(rightframe, text="Image 1", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    image1_location_label.place(x=10, y = 100)   
    
    image2_location_label = Label(rightframe, text="Image 2", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    image2_location_label.place(x=10, y = 130)
    
    global image1_location_text_box,image2_location_text_box ,result_label,result_label_2
    image1_location_text_box = Entry(rightframe)
    image1_location_text_box.place(x = 100, y = 100,width = 590)

    image2_location_text_box = Entry(rightframe)
    image2_location_text_box.place(x = 100, y = 130,width = 590)  

    img_load_button = Button(rightframe, text="Image 1", width = 10,command = lambda:openImage1(self) )
    img_load_button .place(x = 700 , y = 100)

    img2_load_button = Button(rightframe, text="Image 2", width = 10,command = lambda:openImage2(self) )
    img2_load_button .place(x = 700, y = 130) 

    img_sim_button = Button(rightframe, text="Image Similarity", width = 15,command = lambda:apply_technique('Image Similarity') )
    img_sim_button.place(x = 10, y = 190) 
    
    img_sim_button = Button(rightframe, text="ORB", width = 15,command = lambda:apply_technique('ORB') )
    img_sim_button.place(x = 200, y = 190)
    
    img_sim_button = Button(rightframe, text="Search In Dataset", width = 15,command = lambda:apply_technique('Image Similarity') )
    img_sim_button.place(x = 350, y = 190)

    result_label = Label(rightframe, text="Result", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    result_label.place(x=20, y = 310)

    result_label_2 = Label(rightframe, text="", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    result_label_2.place(x=20, y = 360)


# Open a video file
def openImage1(self):
        fullfilename = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=[("img file", "*.jpg; *.jpeg; *.png ")]) # select a video file from the hard drive
        if(fullfilename != ''):
             image1_location_text_box.delete(0,END)
             image1_location_text_box.insert(0,fullfilename)
      
    
def openImage2(self):
        fullfilename = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=[("img file", "*.jpg; *.jpeg; *.png ")]) # select a video file from the hard drive
        if(fullfilename != ''):
             image2_location_text_box.delete(0,END)
             image2_location_text_box.insert(0,fullfilename)


def field_validation():
    if(image1_location_text_box.get() == '' or image2_location_text_box.get() == ''):
        mbox.showerror("Missing Image ","Image path missing")
        return False
    return True

#D:/Agitlab/ce301_maaz_m/project/Gui/detect_region11.png

def apply_technique(technique):
    if(field_validation()):
        if(technique == "Image Similarity"):
            similarity = structual_similarity(image1_location_text_box.get() ,image2_location_text_box.get())
            result_label_2.configure(text = "Found Similarity Rate: " + str(similarity))
            print('worked', similarity)
        elif(technique == "ORB"):
            print(compare_features(image1_location_text_box.get() ,image2_location_text_box.get()))
