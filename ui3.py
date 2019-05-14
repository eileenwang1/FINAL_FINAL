from tkinter import *
import tkinter.messagebox
class GUI3:
    def __init__(self):
        self.root = Tk(className='Welcome to ICS chat')
        self.frame1 = Frame(self.root)
        self.label = Label(self.frame_1, text="Please enter your name")
        self.label.pack(side=LEFT)
        self.entry = Entry(self.frame_1, width=30)
        self.entry.pack(side=LEFT)

        self.frame_1.pack()
        self.button1 = Button(self.frame_2, text='Confirm', command=self.send)
        self.button1.pack(side=TOP)
        self.frame_2.pack()

        self.main_window.geometry("500x100")
        self.main_window.mainloop()
        #please enter your name
#new ui, all in one

#copy the chat_client_class

#the magical send button

#log_in, display name

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


#determine state (time, who, connect, gameing)