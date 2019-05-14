
from chat_client_class import *
import ui3


def main():
    import argparse
    parser = argparse.ArgumentParser(description='chat client argument')
    parser.add_argument('-d', type=str, default=None, help='server IP addr')
    args = parser.parse_args()

    client_ui = ui3.main1()
    #how to put tihs function in threading?
    print("the line after ui3")
    client = Client(args,client_ui)
    '''
    def fun():
        client.ui = GUI3(client)
    '''

    x1 = threading.Thread(target=client.run_chat)
    #x1.daemon = True
    x1.start()




    '''
    x1 = threading.Thread(target=ui3.main, args=(client,))
    x1.start()
    client.run_chat()
    '''
    '''
    x2 = threading.Thread(target=ui3.main)
    x2.daemon = True
    x2.start()
    '''



if __name__ == '__main__':

    main()
