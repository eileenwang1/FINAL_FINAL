
#is there any use of this class?
#just for testing??

import tkinter

class MyGUI:
    def __init__(self):
        self.main_window = tkinter.Tk()
        self.label = tkinter.Label(self.main_window, text=" hello ")
        self.label.pack()
        #self.main_window.pack()

        tkinter.mainloop()

    def change_label(self, text):
        self.label = self.label = tkinter.Label(self.main_window, text)
        print("i am functioning")




