import tkinter
from tkinter import *
from tkinter import filedialog
import os
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mbox
import cv2
from store_images import *
from roi import *
import glob

def predict_roi_panel(self):
    cv2.destroyAllWindows()  
    #refresh the right side GUI
    self.root.update()
    
    rightframe = Frame(self.root,bg='black')
    rightframe.pack(side = RIGHT)  
    rightframe.place(height=800, width=800, x=200, y=0)
    #heading label
    top_heading = Label(rightframe, text="Predict Region Of Intrest", font=("Helvetica", 16),bg ='black',fg = 'WHITE')
    top_heading.place(x=10, y = 20)
    # description label
    desc_label = Label(rightframe, text="Select the dataset directory which consist of images, pressing predict button will create a new directory and\n save all the predicted region the directory ", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    desc_label.place(x=10, y = 58)
 
    #video label
    dataset_label = Label(rightframe, text="Dataset Name", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    dataset_label.place(x=10, y = 120)

    global dataset_name_text_box 
    dataset_name_text_box = Entry(rightframe)
    dataset_name_text_box.place(x = 150, y = 120,width = 590)  

    dataset_dir_label = Label(rightframe, text="Directory", font=("Helvetica", 10),bg ='black',fg = 'WHITE')
    dataset_dir_label.place(x=10, y = 160)
   
    global dataset_location_text_box
    dataset_location_text_box = Entry(rightframe)
    dataset_location_text_box.place(x = 150, y = 160,width = 590)  

    #status window
    global status_window
    status_window = tkinter.Text(rightframe, height=20, width=85)
    status_window.place(x=10, y = 230)



    Browse_dataset_button = Button(rightframe, text="Select Dataset", width = 15,command = lambda:openDataset(self) )
    Browse_dataset_button.place(x = 625, y = 200)


    next_step_button = Button(rightframe, text=" Next ",width = 15,command = lambda:start_predicting_roi() )
    next_step_button.place(x = 625, y = 600)
    

    

# Open a video file
def openDataset(self):
        fullfilename = filedialog.askdirectory() # select a video file from the hard drive
        if(fullfilename != ''):
             dataset_location_text_box.delete(0,END)
             dataset_location_text_box.insert(0,fullfilename)
      
    

def field_validation():
    if(dataset_name_text_box.get() == ''):
        mbox.showerror("Missing Route Name","Directory Name Missing")
        return False
    elif(dataset_location_text_box.get() == ''):
        mbox.showerror("Missing File Path","dataset path is missing")
        return False
    return True

def look_for_features_pred(image,frame_number):
    path = 'previous_detected_regions\\'
     
    
    score_dic =  {}
    #img1 = get_region(image)
    #score_dic['without'] = detect_features(image)
    
    #uimg1 = upper_half(image)
    #score_dic['upper part'] = detect_features(image)

    #limg1 = lower_half(image)
    #score_dic['Lower part'] = detect_features(image)
    
    first = first_region(image)
    score_dic['first'] = detect_features(image)
  
    second = sec_region(image)
    score_dic['second'] = detect_features(image)

    third = third_region(image)
    score_dic['third'] = detect_features(image)
    
    fourth = fourth_region(image)
    score_dic['fourth'] = detect_features(image)

    maximum = max(score_dic, key=score_dic.get)
    print(score_dic)
    highest = (maximum, score_dic[maximum])
    #print(highest[1])
   
    if(highest[1] > 0.40):  
        if( highest[0] == 'first'):
            #display_histogram(first)
          
            cv2.imwrite(os.path.join(path , 'detect_region'+str(frame_number)+'.png'), first)
            print('first imgae writed')
        elif( highest[0] == 'second'):
            #display_histogram(first)
            cv2.imwrite(os.path.join(path , 'detect_region'+str(frame_number)+'.png'), second)
            print(' second imgae writed')
        elif( highest[0] == 'third'):
            #display_histogram(third)
            cv2.imwrite(os.path.join(path , 'detect_region'+str(frame_number)+'.png'), third)
            print('third imgae writed')
        elif( highest[0] == 'fourth'):
            cv2.imwrite(os.path.join(path , 'detect_region'+str(frame_number)+'.png'), fourth)
            print('fourth imgae writed')
        elif( highest[0] == 'Lower part'): 
            #cv2.imwrite(os.path.join(path , 'detect_region'+str(frame_number)+'.jpg'), Lower part)
            print('Lower part imgae writed')
        elif( highest[0] == 'upper part'):
            #cv2.imwrite(os.path.join(path , 'detect_region'+str(frame_number)+'.jpg'), upper part)
            print('upper part imgae writed')
        else:
            print('Couuld not find the roi.')
    else:
        print('irrelevant img')

    
    return highest


def start_predicting_roi():
    if(field_validation()):
        path = dataset_location_text_box.get().replace('/', '\\')+ "\\"
        print(path)
        frame_number = 10
        print('please wait few seconds looking for featutes and region in the image')
        for file in os.listdir(path):
            filename = os.fsdecode(file)
            if filename.endswith(".jpg"):
                frames_path = os.path.join(path,'train'+str(frame_number)+'.jpg')
                print(frames_path)
                look_for_features_pred(frames_path,frame_number)
                frame_number = frame_number + 1
                status = "Detected ROI frame"+str(frame_number)+ " Added in "+path+ "\n"
                status_window.insert(tkinter.END, status)
                status_window.see("end")
        print('finished')

        status_window.insert(tkinter.END, "All Framses processed.\n")
        status_window.insert(tkinter.END, "ROI has been detected and saved.")


