# ECE 5650 
# Project 2 - Client Side
# Shubh Patel
# Reanna John
# 11/18/2020

from socket import *
import threading as thread

from server_helperfunctions import *


# dictionary to work as a switch
what_to_do = {
     "search word": search_word,
    "replace word": replace_word,
    "reverse word": reverse_word,
    "random": random,
    # "display file": ,
    # "exit": Exit
}

# =============== socket thread functions =================

def send_thread_name(thread_name):
    connectionSocket.send(bytes(str(thread_name), 'utf-8'))


def acceptClient(thread_name, connectionSocket, addr, server_time):
    print("Server {} connected to: {}:{}".format(thread_name, addr[0], addr[1]))

    client_flag = server_time.set_flag()

    while True:
        command = str(connectionSocket.recv(1024).decode()).lower()
        print(command)
        if command == 'thread':
            send_thread_name(thread_name)
        elif command in what_to_do.keys():
            what_to_do[command](connectionSocket, server_time)
        elif command == 'exit':
            break
        else:
            print('Command does not exist')

    print('\n{} has closed connection with {}:{}'.format(thread_name, addr[0], addr[1]))
    print('\n\nMetrics:\n')
    print('The client has been handled for {} milliseconds'.format(server_time.get_flag_time(client_flag)))
    server_time.display_history()
    connectionSocket.shutdown(SHUT_WR)
    connectionSocket.close()


# ================================================


SERVERPORT = 12000

threads_handled = 0

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('localhost', SERVERPORT))
serverSocket.listen(3)

# start counting server
sever_time = Time_Track()

print('The server is ready to recieve')


while True:
    connectionSocket, addr = serverSocket.accept()
    thread._start_new_thread(acceptClient, ('thread'+str(threads_handled), connectionSocket, addr, sever_time))
    threads_handled += 1        



