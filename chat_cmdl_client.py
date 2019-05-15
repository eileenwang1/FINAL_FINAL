
from chat_client_class import *
import ui3
from tkinter import *
import threading
from multiprocessing.pool import ThreadPool

pool = ThreadPool(processes=1)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='chat client argument')
    parser.add_argument('-d', type=str, default=None, help='server IP addr')
    args = parser.parse_args()

    client_ui = ui3.main1()

    client = Client(args, client_ui)

    x1 = threading.Thread(target=client.run_chat)
    x1.start()
    client_ui.mainloop()

if __name__ == '__main__':

    main()
