#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#
try:
    import Tkinter as Tk
except:
    import tkinter as Tk
 
root = Tk.Tk()
root.title('root')
 
fen1=Tk.Toplevel(root)
fen1.title('Toplevel')
 
Tk.Button(root, text='détruire le Toplevel', command=fen1.destroy).pack()
Tk.Button(root, text='Quit', command=root.destroy).pack()
root.mainloop()