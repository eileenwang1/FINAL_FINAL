
from chat_client_class import *
import ui3


def main():
    import argparse
    parser = argparse.ArgumentParser(description='chat client argument')
    parser.add_argument('-d', type=str, default=None, help='server IP addr')
    args = parser.parse_args()
    #create an instance of ui3
    client_ui = ui3.main1()
    #how to put this function (the init function of ui3) in threading?
    #if called in threading, how can i use a variable to store the instance of ui3 i,
    #so that the instance can be a parameter in the client class?
    print("the line after ui3")
    client = Client(args,client_ui)

    '''
    def fun():
        client.ui = GUI3(client)
    '''

    x1 = threading.Thread(target=client.run_chat)
    #x1.daemon = True
    x1.start()



if __name__ == '__main__':

    main()
