# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 00:36:08 2019

@author: Acer
"""

import tkinter
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import random as rng
import cv2 
import numpy as np  
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from collections import Counter
import copy
import tkinter as tk

lower_red = np.array([160,100,66]) 
upper_red = np.array([179,255,255]) 
  
lower_green = np.array([37,100,100])
upper_green = np.array([75,255,255])

lower_blue = np.array([100,38,0])
upper_blue = np.array([140,255,255])

lower_yellow = np.array([15,150,150])
upper_yellow = np.array([32,255,255])
arr = ["red","blue","green","yellow"]
dictt = {1:[lower_red,upper_red],2:[lower_blue,upper_blue],3:[lower_green,upper_green],4:[lower_yellow,upper_yellow]}


def connectt():
    count= 0
    frame = cv2.imread(B.get())
    # Converts images from BGR to HSV 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    i = arr.index(COLOR.get())
    #i =2
    mask = cv2.inRange(hsv, dictt[(i+1)][0],dictt[(i+1)][1])
    kernel = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    res = cv2.bitwise_and(frame,frame, mask= closing)
    secondframe = copy.deepcopy(frame)
    #cv2.imshow('res',res) 
    #cv2.imshow("closing",closing)
    #cv2.waitKey(0)
    cv2.destroyAllWindows()
    res = cv2.cvtColor(res,cv2.COLOR_BGR2RGB)
    if len(np.unique(res)) >= 2 :
        threshold = 1
        canny_output = cv2.Canny(mask, threshold, threshold * 2)
        _, contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_poly = [None]*len(contours)
        boundRect = [None]*len(contours)
        for i, c in enumerate(contours):
            contours_poly[i] = cv2.approxPolyDP(c, 3, True)
            boundRect[i] = cv2.boundingRect(contours_poly[i])
        drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
        for i in range(len(contours)):
           color = (0,255,0)
           cv2.drawContours(secondframe, contours_poly, i, color,3)
           cv2.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])),(int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 3)
        #cv2.imshow('Contours', drawing)
        #cv2.imshow("cannyouput",canny_output)
        #cv2.imshow('res',secondframe)
        closing = (255-closing)
        cv2.imwrite("colorfind.png",closing)
        #cv2.waitKey(0)
        cv2.destroyAllWindows()
        font = cv2.FONT_HERSHEY_COMPLEX
        res = (255-res)
        #img = cv2.imread(frame, cv2.IMREAD_GRAYSCALE)
        img = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        shape = SHAPE.get()
        TEXT = COLOR.get() + " " + SHAPE.get()
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
            #cv2.drawContours(img, [approx], 0, (0), 5)
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            if (len(approx) == 3):
                if shape == "triangle": 
                    cv2.putText(frame, "Triangle", (x, y-10), font, 1, (0))
                    cv2.drawContours(frame, [approx], 0, (0,255,0),8)
                    count = 1
            elif ( len(approx) == 4 ):
                if shape == "rectangle":
                    cv2.putText(frame,TEXT, (x, y-15), font,1, color=(0),thickness = 2)
                    cv2.drawContours(frame, [approx], 0, (0,255,0),8)
                    count= count +1
            elif (len(approx) == 5):
                if shape == "pentagon":
                    cv2.putText(frame, "Pentagon", (x, y-10), font, 1, (0),thickness = 2)
                    cv2.drawContours(frame, [approx], 0, (0,255,0), 6)
                    count = 1
            elif (6 < len(approx) < 15):
                 if shape == "ellipse":
                     cv2.putText(frame, "Ellipse", (x, y-10), font, 1, (0),thickness = 2)
                     cv2.drawContours(frame, [approx], 0, (0,255,0), 6)
                     count = 1
            else:
                if shape == "circle":
                    cv2.putText(frame, "Circle", (x, y-10), font, 1, (0),thickness = 2)
                    cv2.drawContours(frame, [approx], 0,(0,255,0), 6)
                    count = 1
                
        #cv2.imshow("shapes", img)
        #cv2.imshow("Threshold", threshold)
        #cv2.imshow("final",frame)
        cv2.imwrite("final.png",frame)
        #cv2.waitKey(0)
        cv2.destroyAllWindows()
        window = tk.Toplevel(root)
        window.geometry("1200x900+0+0")
        window.configure(background="#C7F0DB")
        top = Label(window,text = "Color And Shape",width =62,height = 2,fg = "white",anchor = CENTER)
        top.config(font=("Times", 25,'bold'))
        top.configure(background="#464159")
        top.place(x = 0,y = 0)
        color_seperate = Image.open(B.get())
        resized1 = color_seperate.resize((402,270),Image.ANTIALIAS)
        image1 = ImageTk.PhotoImage(resized1)
        Canva3 = Canvas(window,width = 430,height = 300)
        Canva3.configure(background = "#6C7B95")
        Canva3.place(x = 50,y = 90)
        window.image1 = image1
        Canva3.create_image(15,15, image=image1,anchor = NW)
        original = Image.open("colorfind.png")
        resized = original.resize((402,270),Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(resized)
        Canva4 = Canvas(window,width = 432,height = 300)
        Canva4.configure(background = "#6C7B95")
        Canva4.place(x = 602,y = 90)
        window.image2 = image2
        Canva4.create_image(15,15, image=image2,anchor = NW)
        shapeimage = Image.open("final.png")
        resized2 = shapeimage.resize((402,270),Image.ANTIALIAS)
        image3 = ImageTk.PhotoImage(resized2)
        Canva5 = Canvas(window,width = 432,height = 300)
        Canva5.configure(background = "#6C7B95")
        Canva5.place(x =350 ,y = 450)
        window.image3 = image3
        Canva5.create_image(15,15, image=image3,anchor = NW)
        

        labelt= Label(window,text = "Original Image",bg = "#C7F0DB")
        labelt.config(font=("Open Sans", 24))
        labelt.place(x = 140,y = 405)
        
        labelco= Label(window,text = "Color Seperate Image",bg = "#C7F0DB")
        labelco.config(font=("open sans", 24))
        labelco.place(x = 800,y = 405)
        
        labelco= Label(window,text = "Final Image",bg = "#C7F0DB")
        labelco.config(font=("open sans", 24))
        labelco.place(x = 400,y = 753)
        photoq = PhotoImage(file = "C:/Users/Acer/Desktop/error.png")
        FRAME.photoq = photoq
        button1 = Button(window,image = photoq,command = window.destroy,background="#464159",highlightthickness = 0, bd = 0)
        button1.place(x =1120,y =14)
        if SHAPE.get() == "rectangle":
           if  count == 1:
               window.destroy()
               messagebox.showinfo("Reqirment", "Please select a valid input from image")                
        else:
            if count == 0 :
                window.destroy()
                messagebox.showinfo("Reqirment", "Please select a valid input from image")
    else:
        messagebox.showinfo("Reqirment", "Please select a valid input from image")
            
            
        
        
        
def openfilex():
    global c
    file1= filedialog.askopenfilename()
    c = file1
    B.set(file1)
    original = Image.open(file1)
    resized = original.resize((602,310),Image.ANTIALIAS)
    image1 = ImageTk.PhotoImage(resized)
    Canva1 = Canvas(FRAME,width = 670,height = 297,bd = 16)
    Canva1.configure(background = "#6C7B95")
    Canva1.place(x = 230,y = 99)
    FRAME.image1 = image1
    Canva1.create_image(50,5, image=image1,anchor = NW)

root=tkinter.Tk()
root.geometry("1200x900+0+0")
root.configure(background="#C7F0DB")
B = StringVar()
FRAME=Frame(root, width=1200, height =600)
FRAME.configure(background="#C7F0DB")
FRAME.pack()
top = Label(FRAME,text = "Color And Shape",width =62,height = 2,fg = "white",anchor = CENTER)
top.config(font=("Times", 25,'bold'))
top.configure(background="#464159")
top.place(x = 0,y = 0)

Canva = Canvas(FRAME,width = 702,height = 350)
Canva.configure(background = "#6C7B95")
Canva.place(x = 230,y = 99)

COLOR= StringVar()
colorl = Label(FRAME,text = "Select Color",bg = "#C7F0DB")
colorl.config(font=("Open Sans", 24))

colorl.place(x =512,y = 480)
r1  = Radiobutton(FRAME,text = "   Red   ",value = "red",variable = COLOR,bg = "#FF545C",anchor = CENTER, indicatoron=0, highlightthickness = 0, bd = 0, width = 10,padx = 20,pady = 20)
r2  = Radiobutton(FRAME,text = "  Blue   ",value = "blue",variable = COLOR,bg = "#2596D3 ",anchor =CENTER, indicatoron=0, highlightthickness = 0, bd = 0, width = 10,padx = 17,pady = 20)
r3  = Radiobutton(FRAME,text = "  Green  ",value = "green",variable = COLOR,bg = "#66CE63",anchor = CENTER, indicatoron=0, highlightthickness = 0, bd = 0, width = 10,padx = 14,pady = 20)
r4 = Radiobutton(FRAME,text = "  Yellow  ",value = "yellow",variable = COLOR,bg = "#F2F239",anchor =CENTER, indicatoron=0, highlightthickness = 0, bd = 0, width = 10,padx = 11,pady = 20)
r1.config(font=("Open Sans", '20'))
r2.config(font=("Open Sans", 20))
r3.config(font=("Open Sans", 20))
r4.config(font=("Open Sans", 20))
r1.place(x =155,y = 534)
r2.place(x =388,y = 534)
r3.place(x =621,y = 534)
r4.place(x =855,y = 534)

FRAME2 = Frame(root,width = 1200,height =200)
FRAME2.configure(background="#C7F0DB")

shapesl = Label(FRAME2,text = "Select Shape",bg = "#C7F0DB")
shapesl.config(font=("Open Sans", 22))
shapesl.place(x = 512,y = 10)

button1 = Button(FRAME,text = "Click to load file on canvas",command = openfilex,bg = "#464159",highlightthickness = 0, bd = 0,fg = "white",height = 1,width = 50)
button1.config(font = ("open sans",18))
button1.place(x =231,y = 428)

SHAPE = StringVar()
photo2 = PhotoImage(file = "C:/Users/Acer/Desktop/traingle copy.png")
FRAME2.photo1 = photo2
photoimaget = photo2.subsample(3,3)
r5 = Radiobutton(FRAME2,image = photoimaget,value = "triangle",variable =SHAPE,height =89,anchor = W,bg = "#C7F0DB", indicatoron=0, highlightthickness = 0, bd = 0,width = 120)

photo2 = PhotoImage(file = "C:/Users/Acer/Desktop/rectangle copy.png")
FRAME2.photo2 = photo2
photoimager = photo2.subsample(1,1)
r6 = Radiobutton(FRAME2,image = photo2,value = "rectangle",variable = SHAPE,height =100,anchor = W,bg = "#C7F0DB", indicatoron=0, highlightthickness = 0, bd = 0,width = 140)

photo3 = PhotoImage(file = "C:/Users/Acer/Desktop/circlee copy.png")
FRAME2.photo1 = photo3
r7 = Radiobutton(FRAME2,image =photo3,value = "circle",variable = SHAPE,anchor = W,bg = "#C7F0DB", indicatoron=0, highlightthickness = 0, bd = 0,width = 92)

photo4 = PhotoImage(file = "C:/Users/Acer/Desktop/pentagon copy.png")
FRAME2.photo1 = photo4
r8 = Radiobutton(FRAME2,image = photo4,value = "pentagon",variable = SHAPE,anchor = W,bg = "#C7F0DB", indicatoron=0, highlightthickness = 0, bd = 0,width = 100)

photo5 = PhotoImage(file = "C:/Users/Acer/Desktop/ellipsess copy.png")
FRAME2.photo1 = photo5
r9 = Radiobutton(FRAME2,image = photo5,value = "ellipse",variable = SHAPE,anchor = W,bg = "#C7F0DB", indicatoron=0, highlightthickness = 0, bd = 0,width = 124)

r5.place(x =130,y = 52)
r6.place(x =310,y = 50)
r7.place(x =530,y = 50)
r8.place(x =680,y = 50)
r9.place(x =870,y = 50)
FRAME2.pack()

labelt = Label(FRAME2,text = "trianagle",compound = RIGHT,bg = "#C7F0DB",highlightthickness = 0, bd = 0)
labelt.config(font=("Open Sans", 15))
labelt.place(x =140,y = 160)



labelt = Label(FRAME2,text = "Rectangle",compound = RIGHT,bg = "#C7F0DB",highlightthickness = 0, bd = 0)
labelt.config(font=("Open Sans", 15))
labelt.place(x =320,y = 160)


labelt = Label(FRAME2,text = "Circle",compound = RIGHT,bg = "#C7F0DB",highlightthickness = 0, bd = 0)
labelt.config(font=("Open Sans", 15))
labelt.place(x =550,y = 160)



labelt = Label(FRAME2,text = "Pentagon",compound = RIGHT,bg = "#C7F0DB",highlightthickness = 0, bd = 0)
labelt.config(font=("Open Sans", 15))
labelt.place(x =700,y = 160)


labelt = Label(FRAME2,text = "Ellipse ",compound = RIGHT,bg = "#C7F0DB",highlightthickness = 0, bd = 0)
labelt.place(x =900,y = 160)
labelt.config(font=("Open Sans", 15))



count  = IntVar()
photoar = PhotoImage(file = "C:/Users/Acer/Desktop/right-arrow.png")
FRAME2.photo1 = photoar

button2 = Button(FRAME2,image = photoar,compound = RIGHT,bg = "#C7F0DB",highlightthickness = 0, bd = 0,command = connectt)
button2.place(x =1050,y = 80)
photoq = PhotoImage(file = "C:/Users/Acer/Desktop/error.png")
FRAME.photoq = photoq
button1 = Button(FRAME,image = photoq,command = root.destroy,background="#464159",highlightthickness = 0, bd = 0)
button1.place(x =1120,y =14)
root.mainloop()


