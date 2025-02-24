#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import *
import time

def disp_choice():
    for i in range(nbre):
        if menu_list[i].get():
            print(menu_label[i])


nbre = 10
tk_root = tk.Tk()
screen_width = tk_root.winfo_screenwidth()  
screen_height = tk_root.winfo_screenheight()
tk_root.geometry("%dx%d+%d+%d" % (screen_width/2, screen_height/4, screen_width/4, screen_height*3/8))


# menu_val = [False if x % 2 else True for x in range(nbre)]
menu_val = [False for x in range(nbre)]
menu_list = [IntVar(tk_root) for i in range(len(menu_val))]
menu_label =['menu 0','menu 1','menu 2','menu 3','menu 4','menu 5','menu 6','menu 7','menu 8','menu 9']
menu_color = ['black','brown','red','orange','yellow','green','blue','violet','grey','white']
menu_separator =[3, 5, 8]


for i in range(nbre):
    print(i)
for i in range(nbre):
    menu_list[i].set(menu_val[i])
    
menubar = Menu(tk_root)
testmenu = Menu(menubar, tearoff=0)
for i in range(nbre):
    testmenu.add_checkbutton(label=menu_label[i], variable=menu_list[i], foreground=menu_color[i], command = disp_choice)
    if i in menu_separator:
        testmenu.add_separator()

menubar.add_cascade(label="Essai", menu=testmenu)
tk_root.config(menu=menubar)
 
