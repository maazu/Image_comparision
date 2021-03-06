from tkinter import *
from bus_page import *
from predict_roi import *
from display_buses import *
from image_operations import *
        
class GUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Maion | Bus ')
        self.root.resizable(False, False)
        self.root.geometry('1000x700')
        
        frame = Frame(self.root)  
        frame.pack()  
        self.root.update() 
        #left frame  - MENU SIDE

        leftframe = Frame(self.root,bg ='#001f42')  
        leftframe.pack(side = LEFT)  
        leftframe.place(height=800, width=280, x=0, y=0)

        #right frame - DISPAY SIDE
        rightframe = Frame(self.root,bg='#003e85')  
        rightframe.pack(side = RIGHT)  
        rightframe.place(height=800, width=800, x=200, y=0)

        
        #Project Logo
        project_logo = Label(leftframe, text=" MAION \n Bus Tracker", font=("Helvetica", 16),bg='#001f42',fg = 'WHITE')
        project_logo.place(x=35, y=20)

        #Footer Note
        footer_note = Label(leftframe, text=" Capstone Project Created  by \n Muhammad Maaz\n Supervisied by: Dr Stephen Sangwine \nSecond Assessor: Dr Serafeim Perdikis \n CSEE Department \n University Of Essex", font=("Helvetica", 8),bg='#001f42',fg = 'WHITE')
        footer_note.place(x=0, y=600)


        #Server Button
        #Server_button = Button(leftframe, text="Server", fg="black", width = 20, command= lambda:server_page(self))  
        #Server_button.place(x=25, y=150)

        #Live Buses Button
        Buses_button = Button(leftframe, text="Live Buses", fg="black", width = 20,command = lambda:display_buses(self))  
        Buses_button.place(x=25, y=200)

        #Add Bus Button
        bus_route_button = Button(leftframe, text="New Bus Route", fg="black", width = 20,command = lambda:add_new_route_page(self))  
        bus_route_button.place(x=25, y=250)
        
        #Predict ROI Button
        predict_button = Button(leftframe, text="Predict ROI", fg="black", width = 20, command = lambda:predict_roi_panel(self))  
        predict_button.place(x=25, y=300)

        
        #Help Button
        immage_operation_button = Button(leftframe, text="Features", fg="black", width = 20, command = lambda:show_Img_Operation(self))  
        immage_operation_button.place(x=25, y=350)


        
        #Map Button
        Map_button = Button(leftframe, text="Map View", fg="black", width = 20,command=self.map_page)  
        Map_button.place(x=25, y=400)


        Quit_button = Button(leftframe, text="Quit", fg="black", width = 20,command=self.quit_page)  
        Quit_button.place(x=25, y=450)



          
    def map_page(self):
        self.root.update() 
        rightframe = Frame(self.root,bg='black')  
        rightframe.pack(side = RIGHT)  
        rightframe.place(height=800, width=800, x=200, y=0)
        project_logo = Label(rightframe, text="Map View", font=("Helvetica", 16),bg ='black',fg = 'WHITE')
        project_logo.place(x=35, y=20)


        
    def quit_page(self):
        self.root.update() 
        rightframe = Frame(self.root,bg='black')  
        rightframe.pack(side = RIGHT)  
        rightframe.place(height=800, width=800, x=200, y=0)
        quit_heading = Label(rightframe, text="Quit", font=("Helvetica", 16),bg ='black',fg = 'WHITE')
        quit_heading.place(x=35, y=20)

        quit_note = "Pressing Yes button will shut the entirely."
        quit_heading = Label(rightframe, text=quit_note, font=("Helvetica", 11),bg ='black',fg = 'WHITE')
        quit_heading.place(x=35, y=50)
        quit_button = Button(rightframe, text="Yes", fg="black", width = 20,command=lambda:quit_program())  
        quit_button.place(x=35, y=100)


    
    def start(self):
        self.root.mainloop()


def quit_program():
    print("Closing program")
    exit(0)  
         
if __name__ == "__main__":  
    appstart = GUI()
    appstart.start()
   
