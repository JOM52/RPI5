import tkinter as tk
from tkinter import *
root=tk.Tk()

def hello():
    print("hello !")

def toggle():
    if submenu.entrycget(0,"state")=="normal":
        submenu.entryconfig(0,state=DISABLED)
        submenu.entryconfig(1,label="Speak please")
    else:
        submenu.entryconfig(0,state=NORMAL)
        submenu.entryconfig(1,label="Quiet please")

menubar = Menu(root)

submenu=Menu(menubar,tearoff=0)

submenu2=Menu(submenu,tearoff=0)
submenu2.add_command(label="Hello", command=hello)

# this cascade will have index 0 in submenu
submenu.add_cascade(label="Say",menu=submenu2,state=DISABLED)
# these commands will have index 1 and 2
submenu.add_command(label="Speak please",command=toggle)
submenu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="Test",menu=submenu)

# display the menu
root.config(menu=menubar)
root.mainloop()