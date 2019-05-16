# FINAL_FINAL
ics final

Authors:
Zixiao Yang: Texas Poker (server side)
Eileen Wang: GUI (client side)

------------------------------------------------------------------------------------------------------------------------------

Texas:
To run the program:
     cd final_final
     cd texas (important)
     server: python chat_server.py
     create players: python chat_cmdl_client.py (suppose names as Alice and Bob)
     start game: type ‘g Bob’ for Alice, or type ‘g Alice’ for Bob

We coded the main gaming system from scratch. The system shuffles, gives out cards, chooses five cards for best combination and shows the results automatically. In order to running the game while keep receiving and sending messages, we uses a threading process to run the main_game in the background. In the gaming status, the user_input sent to server would be sent to the gaming system, and the output processed by the system would be sent back to the server (and then the socket and clients).In order to do this, we set up a Player class to track with the betting status and chip status, and set the Players an attribute of the server. 

----------------------------------------------------------------------------------------------------------------------------

GUI:
To run the program:
     cd FINAL_FINAL
     server: chat_server.py 
     create clients: chat_cmdl_client.py

In file ui3.py, we use the tkinter module to create the GUI interface.
We modify the the file chat_cmdl_client.py to create an instance of our GUI class for each instance of the Client class.
In chat_cmdl_client.py, we use threading to enable the chat system and the GUI interface to run together.

An optimization we did for the original chat system is at chat_client_class.py:
     def read_input(self):
        while True:
            text = self.ui.to_send
            self.ui.to_send = ""
            if len(text) > 0:
                self.console_input.append(text) # no need for lock, append is thread safe
                #self.console_input is used as a queue, the original code enqueue each time the infinite loop runs.
                #optimization for space complexity: only enqueue message that is not empty
                #and there is no trade-off for time-complexity, the runtime for the extra if-statement is O(1)

A problem we run into:
Some transmission of message in gui is not successful. I suspect that there is some time gap between threadings. If a message is (unfortunately) sent within the time gap, the transmission is not successful. t o fix the problem requires more knowledge of threading.

