from socket import *
from sys import getsizeof
import time
import gzip


# ============================== helper =================================

def send_file(clientSocket, fileName):
    file = open(fileName, 'rb')
    file_contents = file.read()
    file.close()

    size = str(getsizeof(file_contents))
    
    # sending file size
    clientSocket.send(bytes(size, 'utf-8'))

    # sending file
    clientSocket.send(file_contents)


# ============================== client =================================

#search word function
def search_word(clientSocket): 
    '''
    search word function (client):
    > reads file and sends the client each word, then upon recieving the count, displays it
    '''

    filename, word = input('input the file to search through and word to search (space-separated): ').split()
    
    # sending word to search
    clientSocket.send(bytes(word, 'utf-8'))

    # checks if filename has .txt at the end
    if (filename[-4:] != '.txt'):
        filename = filename + '.txt'
    
    if (filename):
        send_file(clientSocket, filename)
        count = int(clientSocket.recv(1024).decode())
        print('\nFound {} {} times in {}\n'.format(word, count, filename))
    else: 
        print('No file given')



#replace word function 
def replace_word(clientSocket):
    '''
    replace word function (client):
    > reads file and sends the client each word, then upon recieving the count, displays it
    '''
    word_to_replace, replace_to = input("Please enter the word you'd like to replace, then the word you want to replace to (space-separated): ").split()
    input_file, output_file = input('Input the file to search through and file name to save to (space-separated): ').split()
    words_to_send = [word_to_replace, replace_to]
    print('DEBUG: ', words_to_send)
    # sending word to replace, replace to to server
    for i in words_to_send:
        clientSocket.send(bytes(i, 'utf-8'))

    if (input_file[-4:] != '.txt'):
        input_file = input_file + '.txt'

    send_file(clientSocket, input_file)

    size = int(clientSocket.recv(1024).decode())

    new_file_content = str(clientSocket.recv(size).decode())


    new = open(output_file, 'w+')
    new.write(new_file_content)
    new.close()

    print('file created')

#display file function
def display_file(clientSocket):
    filename = input('Input the file to display: ')

    if (filename[-4:] != '.txt'):
        filename = filename + '.txt'
    
    display = ''

    with open(filename, "r") as file:
        for line in file:
            for each_word in line.split():
                display += ' '
                display += each_word

    print('File Contents:', '\n', display, '\n')
                
#reverse word function 
def reverse_word(clientSocket): 
    input_file, output_file = input('Input the file to search through and file name to save to (space-separated): ').split()
    clientSocket.send(bytes(output_file, 'utf-8'))

    with open(input_file, "r") as file:
        for line in file:
            for each_word in line.split():
                clientSocket.send(bytes(each_word, 'utf-8'))
    clientSocket.send(bytes('FINSH_SENDING_TO_CLIENT', 'utf-8'))
    print(output_file, 'has been created')
    
#exit function
def Exit(clientSocket):
    clientSocket.send(bytes('Exit', 'utf-8'))
    clientSocket.shutdown(SHUT_RDWR)
    clientSocket.close()
    exit()
        
#displaying the thread active when the client connects to the server
def get_thread_name(clientSocket, userInput):
    clientSocket.send(bytes(userInput, 'utf-8'))
    thread_connected = clientSocket.recv(1024).decode()

    print('Client connected to thread:', thread_connected)
    