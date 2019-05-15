
from chat_client_class import *
import ui3
from tkinter import *
import threading


def main():
    import argparse
    parser = argparse.ArgumentParser(description='chat client argument')
    parser.add_argument('-d', type=str, default=None, help='server IP addr')
    args = parser.parse_args()


    #print("the line before creating a root")
    #root = Tk(className='Welcome to ICS chat')
    #root = Tk()
    #print("creating a root line gets run")

    client_ui = ui3.main1() #create an instance of ui3
    Root = ui3.get_root()
    client = Client(args, client_ui)
    x2 = threading.Thread(target=Root.mainloop)
    x2.daemon = True
    x2.start()
    #how to put this function (the init function of ui3) in threading?
    #if called in threading, how can i use a variable to store the instance of ui3 i,
    #so that the instance can be a parameter in the client class?
    print("the line after ui3")


    '''
    def fun():
        client.ui = GUI3(client)
    '''

    x1 = threading.Thread(target=client.run_chat)
    #x1.daemon = True
    x1.start()



if __name__ == '__main__':

    main()
