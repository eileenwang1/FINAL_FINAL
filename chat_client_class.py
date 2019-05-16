import time
import socket
import select
import sys
import json
from chat_utils import *
import client_state_machine as csm
import threading


class Client:
    def __init__(self, args, client_ui):
        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE
        self.name = ""

        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''
        self.args = args

        ####change:
        self.ui = client_ui


    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def get_name(self):

        return self.name

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        self.sm = csm.ClientSM(self.socket)
        reading_thread = threading.Thread(target=self.read_input)
        # a threading here, read_input function gets run over and over again
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

        if len(self.console_input) > 0:
            my_msg = self.console_input.pop(0)  #a queue
        if self.socket in read:
            peer_msg = self.recv()

        return my_msg, peer_msg

    def output(self):
        if len(self.system_msg) > 0:
            try:
                self.ui.to_receive.append(self.system_msg)
                time.sleep(0.1)
                self.ui.display()
            except:
                print("output to ui failed")
            self.system_msg = ''

    def login(self):
        ### change
        my_msg, peer_msg = self.get_msgs()

        if len(my_msg) > 0:
            self.name = my_msg
            print("my name is", my_msg)
            msg = json.dumps({"action":"login", "name":self.name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.state = S_LOGGEDIN
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(self.name)
                self.print_instructions()
                return (True)
            elif response["status"] == 'duplicate':
                self.system_msg += 'Duplicate username, try again'
                return False
        else:               # fix: dup is only one of the reasons
           return(False)


    def read_input(self):
        #todo: put it in ui
        while True:
            text = self.ui.to_send
            self.ui.to_send = ""

            if len(text) > 0:
                self.console_input.append(text) # no need for lock, append is thread safe

    def print_instructions(self):
        self.system_msg += menu

    def run_chat(self):

        self.init_chat()    #create a socket for the client
                            #start the reading thread

        self.system_msg += 'Welcome to ICS chat\n'
        self.system_msg += 'Please enter your name: '

        while self.login() != True: #when no one logs in
            self.output()   #display the system_msg for once
        self.system_msg += 'Welcome, ' + self.get_name() + '!'
        self.output()

        while self.sm.get_state() != S_OFFLINE:

            self.proc()
            self.output()
            time.sleep(0.2)
        self.quit()

#==============================================================================
# main processing loop
#==============================================================================
    def proc(self):
        my_msg, peer_msg = self.get_msgs()

        self.system_msg += self.sm.proc(my_msg, peer_msg)



