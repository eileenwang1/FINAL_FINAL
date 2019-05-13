#source: https://www.youtube.com/watch?v=7rZ_6LFcGX8
from tkinter import *
import tkinter.messagebox
import random
from chat_client_class import *
from chat_cmdl_client import *

class GUI2:
    def __init__(self, menu):
        self.system_msg = ''

        self.root = Tk(className='menu')
        self.frame = Frame(self.root)
        self.frame_2 = Frame(self.root)
        self.frame_3 = Frame(self.root)

        self.scroll = Scrollbar(self.frame)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.menu = menu.split("\n")
        #self.menu is a list of the string
        self.listbox = Listbox(self.frame,yscrollcommand=self.scroll.set, width=500)

        for i in self.menu:
            self.listbox.insert(END, str(i))
        self.listbox.pack(side=LEFT)

        self.scroll.config(command=self.listbox.yview)
        self.frame.pack()


        self.button1 = Button(self.frame_2, text = 'Send', command = self.send)
        self.to_send = ""

        self.button1.pack(side = LEFT)
        self.frame_2.pack()



        self.prompt_label = Label(self.frame_3, text = 'enter below')
        self.entry = Entry(self.frame_3, width = 70)

        self.prompt_label.pack(side = TOP)
        self.entry.pack(side = TOP)


        self.frame_3.pack()

        self.root.geometry("500x500")
        self.root.mainloop()

    def send(self):
        message = self.entry.get()
        if len(message) == 0:
            tkinter.messagebox.showinfo("Warning", "Can't sent empty message!")
        else:
            self.listbox.insert(END, message)   #insert into the dialogue box
                                                #how to pass it to the server?

            self.entry.delete(0, END)           #delete was sended to the message box
            self.to_send = message

        self.frame.pack()

        my_msg = self.to_send
        peer_msg = ''
        self.system_msg += self.sm.proc(my_msg, peer_msg)
        self.to_send = ''






