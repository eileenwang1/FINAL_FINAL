#source: https://www.youtube.com/watch?v=7rZ_6LFcGX8
from tkinter import *
import tkinter.messagebox
import random

class MyGUI:
    def __init__(self):
        self.name = None

        self.main_window = Tk(className = 'Welcome to the ICS chat!')
        self.frame_1 = Frame(self.main_window)
        self.frame_2 = Frame(self.main_window)

        self.label = Label(self.frame_1, text = "Please enter your name")
        self.label.pack(side = LEFT)

        self.entry = Entry(self.frame_1, width = 30)
        self.entry.pack(side = LEFT)

        self.frame_1.pack()

        self.button1 = Button(self.frame_2, text = 'Confirm', command = self.confirm)
        self.button1.pack(side = TOP)
        #self.botton1 = Botton(self.frame_2)

        self.frame_2.pack()

        self.main_window.geometry("500x100")
        self.main_window.mainloop()

  #  def delete_first(self):
   #     self.listbox.delete(END)



    def confirm(self):
        user_input = self.entry.get()
        if len(user_input) == 0:
            tkinter.messagebox.showinfo("Warning", "Name can't be empty!")
        else:
            self.name = user_input
            self.main_window.destroy()

if __name__ == '__main__':
    my_gui = MyGUI()