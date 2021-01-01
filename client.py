# ECE 5650 
# Project 2 - Client Side
# Shubh Patel
# Reanna John
# 11/18/2020

from socket import *
from client_helperfunctions import *
from server_helperfunctions import compress_file, uncompress_file

SERVERNAME = 'localhost'
SERVERPORT = 12000


# dictionary to work as a switch
what_to_do = {
     "search word": search_word,
    "replace word": replace_word,
    "reverse word": reverse_word,
    "display file": display_file,
    "exit": Exit,
}

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((SERVERNAME, SERVERPORT))

while clientSocket:

    # ======= ask user which operation to do ======

    print("Valid Operations: ", 
            "\t> thread - server sends back the thread serving the current operation", 
            "\t> Search Word - counts occurances of given word in given file", 
            "\t> Replace Word - replaces a given word by another given word in a given file", 
            "\t> Reverse Word", 
            "\t> Display File", 
            "\t> Exit", sep="\n")
    userInput = input("What operation would you like to do? ").lower()

    # =============================================


    # ========= handle operation ==================

    # print('DEBUG:', userInput)
    if userInput == 'thread':
        get_thread_name(clientSocket, userInput)
    elif userInput in what_to_do.keys():
        # preps server for search word function
        clientSocket.send(bytes(userInput, 'utf-8'))
        what_to_do[userInput](clientSocket)
    else: 
        print('Command does not exist')

    # =============================================
