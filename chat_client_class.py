import time
import socket
import select
import sys
import json
from chat_utils import *
import client_state_machine as csm
import threading
from ui1_log_in import *
from ui2_menu import *

class Client:
    def __init__(self, args):
        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE

        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''
        self.args = args

        ####change:
        self.welcome_page = None
        self.dialogue_box = None
        self.counter = 0

    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def get_name(self):

        #####change:
        return self.welcome_page.name
    #    return self.name

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        self.sm = csm.ClientSM(self.socket)
        reading_thread = threading.Thread(target=self.read_input)
        reading_thread.daemon = True
        reading_thread.start()

    def shutdown_chat(self):
        return

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def get_msgs(self):
        read, write, error = select.select([self.socket], [], [], 0)
        my_msg = ''
        peer_msg = []
        #msg_list = []
        #peer_code = M_UNDEF    for json data, peer_code is redundant
        if len(self.console_input) > 0:
            print(len(self.console_input))
            print(type(self.console_input))
            print(self.console_input)
            my_msg = self.console_input.pop(0)
        if self.socket in read:
            peer_msg = self.recv()
        #print("the origianl my_msg in get_msg is", len(my_msg), type(my_msg))
        #the original my_msg is empty string

        my_msg = str(self.dialogue_box.to_send)
        # print(type(my_msg),len(my_msg))
        # print(my_msg)
        #self.dialogue_box.to_send = ""
        '''
        #if len(msg_list) == 0:
            #msg_list.append(self.dialogue_box.to_send)
            self.dialogue_box.to_send = ""
            msg_list.append("")
            my_msg = msg_list.pop(0)
        else:
            my_msg = ""
        '''

        #at least in local line
        return my_msg, peer_msg

    def output(self):
        if len(self.system_msg) > 0:
            print(self.system_msg)
            try:
                self.dialogue_box.listbox.insert(END, self.system_msg)
                self.dialogue_box.frame.pack()
            except:
                print("Nothing happens")
            #add to list box
            self.system_msg = ''
           # print("the output function is executed")

    def login(self):
        ### change
        my_msg, peer_msg = self.get_msgs()
        my_msg = self.welcome_page.name

        if len(my_msg) > 0:
            print("my name is", my_msg)
            #self.name = my_msg
            msg = json.dumps({"action":"login", "name":self.welcome_page.name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.state = S_LOGGEDIN
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(self.welcome_page.name)
                self.print_instructions()
                return (True)
            elif response["status"] == 'duplicate':
                self.system_msg += 'Duplicate username, try again'
                return False
        else:               # fix: dup is only one of the reasons
           return(False)


    def read_input(self):
        while True:
            text = sys.stdin.readline()[:-1]
            self.console_input.append(text) # no need for lock, append is thread safe

    def print_instructions(self):
        self.system_msg += menu

    def run_chat(self):
        self.init_chat()


        self.welcome_page = GUI1()

        self.system_msg += 'Welcome to ICS chat\n'
        self.system_msg += 'Please enter your name: '

        self.output()

        self.dialogue_box = GUI2(menu)

        while self.login() != True:
            self.output()
        self.system_msg += 'Welcome, ' + self.get_name() + '!'
        self.output()
        while self.sm.get_state() != S_OFFLINE:
            self.proc()
            self.output()
            time.sleep(CHAT_WAIT)
        #self.counter = 0
        self.quit()

#==============================================================================
# main processing loop
#==============================================================================
    def proc(self):
        my_msg, peer_msg = self.get_msgs()
        #print(len(my_msg))

        #this function is inside an infinit loop, should not call ui2 function here
        self.system_msg += self.sm.proc(my_msg, peer_msg)
        self.dialogue_box.to_send = ""


