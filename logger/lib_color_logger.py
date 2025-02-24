#!/usr/bin/env python3
# -*-
"""
    class Colors to generate s aet of colors
"""

import random
import math
import tkinter as tk
from tkinter import *

MAX_ROWS = 35
FONT_SIZE = 18 # (pixels)

class Colors:
    
    """ cette classe sert à générer un set de couleurs dans une liste
        Procédures :
        _init ()
    """

    def __init__(self, nbre_of_colors):
        
        # version infos
        VERSION_NO = "0.01.01" 
        VERSION_DATE = "27.04.2020"
        VERSION_DESCRIPTION = "tout au début"
        VERSION_STATUS = "en développement "
        VERSION_AUTEUR = "josmet"

        random.seed(math.sin(math.log(math.pi)))
        
        self.color_list = []
        for i in range (nbre_of_colors):
            color_val_rouge = random.randrange(255)
            color_val_vert = random.randrange(255)
            color_val_bleu = random.randrange(255)
            color_tupple = (color_val_rouge, color_val_vert, color_val_bleu)
            self.color_list.append(color_tupple)

    def color_from_rgb(self, rgb):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        return "#%02x%02x%02x" % rgb   

if __name__ == '__main__':

    root = Tk()
    root.title("Named colour chart")
    
    colors = Colors(255)
    
    row = 0
    col = 0
    for ind, color in enumerate(colors.color_list):
      e = Label(root, text = "".join([str(ind), " -> ", str(color), "   "]), background = colors.color_from_rgb(color), 
            font = (None, -FONT_SIZE))
      e.grid(row = row, column = col, sticky = W)
      row += 1
      if (row > MAX_ROWS):
        row = 0
        col += 1
    
#       print("".join([str(ind), " -> ", str(color), "   "]))
    root.mainloop()
        
