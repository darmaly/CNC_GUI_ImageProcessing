import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
from pathlib import Path
import cv2
import os
import imgToSVG
import trace_image


# global variable 
saved=0
myFont=0
filteredContourGlob=None
originalSize=[640, 480]
image_to_svg_size_reduction=2
min=120
max=180

#creates the GUI interface
class ImageUploader:

    def __init__(self, master):
        self.master = master
        
        #define font
        global myFont
        myFont = font.Font(family='Courier New')
        self.master.title("Image Uploader")
        
        #adds label to define GUI
        myLabel = Label(self.master, text = "Welcome to Riggs Rat's CNC Machine", borderwidth=2, relief='solid', padx=10, pady=5, font=myFont, )
        myLabel.pack()
        
        #makes background of GUI orange
        self.master.configure(background='#FF5F1F')
        self.image_label = tk.Label(self.master, font=myFont, borderwidth=2)
        self.image_label.pack()

        #creates button to upload image from current directory
        self.upload_button = tk.Button(self.master, text="Upload Image", borderwidth=0, relief=RAISED, activebackground="#000", activeforeground="#fff", command=self.upload_image)
        self.upload_button['font'] = myFont
        self.upload_button.pack()
        self.master.geometry("600x500")
        
    #callback for upload button    
    def upload_image(self):
        #opens png and jpeg files in current directory
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpeg *.jpg")])
        if not file_path:
            return  # User cancelled the dialog
        #displays image on the GUI
        image = Image.open(file_path)
        image = image.resize((400, 400), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        
        #resive image again to cv2 format
        image2 = imgToSVG.resizeImage(file_path, 80)
        #calls & detects Canny from imgToSVG.py file
        edges = imgToSVG.detectEdges_canny(image2, thresh_min=20, thresh_max=100)
        contours, hierarchy = imgToSVG.detectContours(file_path)
        #calls function print_pixel_path from imgToSVG to make file of contour points (imagePathPoints.CNC)
        imgToSVG.print_pixel_path(contours, 3000, hierarchy) 

        # Save the edge-detected image as a new .ppm file in the current working directory
        file_name, _ = os.path.splitext(file_path)
        edge_file_path = f"{file_name}_edge.jpg"
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cv2.imwrite(os.path.join(os.getcwd(), edge_file_path), edges_bgr, [cv2.IMWRITE_PXM_BINARY, 1])
        print(f"Edge-detected image saved in {edge_file_path}")

        #creates button to view edge-detected image
        self.view_button = tk.Button(self.master, text="View Edge Detected Image", borderwidth=0, relief=RAISED, activebackground="#000", activeforeground="#fff", command=lambda: self.view_image(edge_file_path))
        self.view_button['font'] = myFont
        self.view_button.pack()

    #call back for edge detected image
    def view_image(self, edge_file_path):
        #replaces image in GUI to be edge detected version
        image = Image.open(edge_file_path)
        print(image)
        image = image.resize((400, 400), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        self.view_button.destroy()
        #ccreates button for drawing
        self.view_button = tk.Button(self.master, text="Start", borderwidth=0, relief=RAISED, activebackground="#000", activeforeground="#fff", command=lambda: self.start())
        self.view_button['font'] = myFont
        self.view_button.pack()

    #call back for start button
    #draws
    def start(self):
        #set placement of start
        trace_image.goxy(0,-1350,4000,"m")
        trace_image.setHome()
        trace_image.goxy(250, 300,4000, "m")
        trace_image.setHome()
        #trace image & draw on paper
        trace_image.traceImage("imagePathPoints.CNC")  
        #return pen to "home" location
        trace_image.goHome(4000)
        trace_image.setHome()
        trace_image.goxy(-260,1025, 4000, "m")
        trace_image.setHome()
        
        
if __name__ == "__main__":
    root = tk.Tk()
    image_uploader = ImageUploader(root)
    root.mainloop()