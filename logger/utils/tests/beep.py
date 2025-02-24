from tkinter import Tk, Label, Button
import os

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("Random Tone Generator")

        self.label = Label(master, text="Press Generate and enjoy")
        self.label.pack()

        self.generate_button = Button(master, text="Generate", command=self.generate)
        self.generate_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def generate(self):
#         os.system('play -n -c1 synth 3 sine 500')
        os.system("speaker-test -c1 -t sine -f 800 -P 2 -p 0.4 -l 1")
root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()