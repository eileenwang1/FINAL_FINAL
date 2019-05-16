# FINAL_FINAL
ics final

Authors:
Zixiao Yang: Texas Poker (server side)
Eileen Wang: GUI (client side)

Texax:





GUI:
passage:
cd FINAL_FINAL
server: chat_server.py 
create client: chat_cmdl_client.py

In file ui3.py, we use the tkinter module to create the GUI interface.
We modify the the file chat_cmdl_client.py to create an instance of our GUI class for each instance of the Client class.
In chat_cmdl_client.py, we use threading to enable the chat system and the GUI interface to run together.

An optimization we did for the orinigal chat system is at chat_client_class.py
     def read_input(self):
        #todo: put it in ui
        while True:
            text = self.ui.to_send
            self.ui.to_send = ""
            if len(text) > 0:
                self.console_input.append(text) # no need for lock, append is thread safe
                #self.console_input is used as a queue, the original code enqueue each time the infinite loop runs.
                #optimization for space complexity: only enqueue message that is not empty
