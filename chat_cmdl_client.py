
from chat_client_class import *
import ui3
import threading

def main():
    import argparse
    parser = argparse.ArgumentParser(description='chat client argument')
    parser.add_argument('-d', type=str, default=None, help='server IP addr')
    args = parser.parse_args()

    client_ui = ui3.main1() #create an instance of the ui class
    client = Client(args, client_ui)    #create an instance of the client class
    x1 = threading.Thread(target=client.run_chat)   #put run_chat into threading
    #x1.daemon = True
    x1.start()
    #client_ui.update()
    client_ui.display()
    client_ui.mainloop()

if __name__ == '__main__':

    main()
