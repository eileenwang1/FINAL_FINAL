"""
Created on Sun Apr  5 00:00:32 2015
@author: zhengzhang
"""
from chat_utils import *
import json
# from ui1_log_in import *
# from ui2_menu import *


## change
from texas_main_game import *


class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s  ### s stands for socket

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def gaming_to(self, peer):
        msg = json.dumps({"action":"connect_g", "target":peer})
        print("line {} is excecuted".format(1))
        mysend(self.s, msg)
        print(self.s)
        print(msg)
        print("line {} is excecuted".format(2))

        response = json.loads(myrecv(self.s))
        print("response is",response)
        if response["status"] == "success":
            print("line {} is excecuted".format(4))
            self.peer = peer
            self.out_msg += 'You are gaming with '+ self.peer + ', good luck! \n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot gaming with yourself (sick)\n'
        else:
            print("line {} is excecuted".format(5))
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    #here is the change
                    self.out_msg += json.dumps(logged_in)

                elif my_msg[0] == 'g':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == 'g_':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.gaming_to(peer) == True:
                        self.state = S_GAMING
                        self.out_msg += 'Gaming with ' + peer + '. Good Luck !\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:

                    self.out_msg += menu

            if len(peer_msg) > 0:
                try:
                    peer_msg = json.loads(peer_msg)
                except Exception as err :
                    self.out_msg += " json.loads failed " + str(err)
                    return self.out_msg

                if peer_msg["action"] == "connect":
                    # ----------your code here------#
                    print(peer_msg)
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING
                    # ----------end of your code----#

                elif peer_msg["action"] == "connect_g":
                    # ----------your code here------#
                    print(peer_msg)
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are gaming with ' + self.peer
                    self.out_msg += '. Gaming away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_GAMING
                    # ----------end of your code----#

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''

                elif my_msg == 'game':
                    self.out_msg += '[server] if you want to play game with your peer, say "bye" to return' \
                                    ' and type "g" + your peer\'s name (g ' + self.peer + ')\n'

            if len(peer_msg) > 0:  # peer's stuff, coming in
                # ----------your code here------#
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.out_msg += peer_msg["message"]
                    self.state = S_LOGGEDIN
                else:
                    self.out_msg += peer_msg["from"] + peer_msg["message"]
                # ----------end of your code----#
            if self.state == S_LOGGEDIN:
                # Display the menu again
                self.out_msg += menu


        elif self.state == S_GAMING:

            if len(my_msg) > 0:
                #this part is fine
                print("the message i intend to send is", my_msg)
                mysend(self.s, json.dumps({"action":"exchange_g", "from":"[" + self.me + "]", "message":my_msg}))
                print("the mysend line is also executed")

                if my_msg == 'good game':
                    print("my message good game is executed")
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''

            if len(peer_msg) > 0: # peer's stuff, coming in
                # ----------your code here------#
                peer_msg = json.loads(peer_msg)
                print('Congratulations, here is the message', peer_msg)
        #        if peer_msg["action"] == "connect_gaming":
         #           self.out_msg += "Sorry, currently only two people are allowed to play the game"
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.out_msg += peer_msg["message"]
                    self.state = S_LOGGEDIN
                else:
                    self.out_msg += peer_msg["from"] + peer_msg["message"]
                    print("the most essential line is good")


            if self.state == S_LOGGEDIN:
                # Display the menu again
                self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg