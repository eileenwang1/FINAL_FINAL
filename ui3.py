from tkinter import *
import tkinter.messagebox


Root = Tk(className='Welcome to ICS chat')
def get_root():
    return Root


def main1():
    x = GUI3(Root)
    return x


class GUI3(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.geometry("500x500")

        self.to_send = ""
        self.to_receive = []
        while len(self.to_receive) != 0:
            self.listbox.insert(END, self.to_receive.pop(0))

        self.frame_1 = Frame(master)
        self.frame_2 = Frame(master)
        self.frame_3 = Frame(master)

        self.scroll = Scrollbar(self.frame_1)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self.frame_1, yscrollcommand=self.scroll.set, width=500)


        self.listbox.pack(side=LEFT)

        self.scroll.config(command=self.listbox.yview)
        self.frame_1.pack()

        self.button1 = Button(self.frame_2, text='Send', command=self.send)

        self.button1.pack(side=LEFT)
        self.frame_2.pack()

        self.prompt_label = Label(self.frame_3, text='enter below')
        self.entry = Entry(self.frame_3, width=70)

        self.prompt_label.pack(side=TOP)
        self.entry.pack(side=TOP)

        self.frame_3.pack()
        self.pack()


    def display(self):
        while len(self.to_receive) != 0:
            target = self.to_receive.pop(0)
            l = target.split('\n')
            for item in l:
                self.listbox.insert(END, item)



    def send(self):
        message = self.entry.get()
        if len(message) == 0:
            tkinter.messagebox.showinfo("Warning", "Can't sent empty message!")
        else:
            self.listbox.insert(END, message)   #insert into the dialogue box
                                                #how to pass it to the server?

            self.entry.delete(0, END)           #delete was sended to the message box
            self.to_send = message

