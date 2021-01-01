from socket import *

# ============================== client =================================

def search_word(clientSocket): 
    '''
    search word function (client):
    > reads file and sends the client each word, then upon recieving the count, displays it
    '''

    filename, word = input('input the file to search through and word to search (space-separated): ').split()
    
    # checks if filename has .txt at the end
    if (filename[-4:] != '.txt'):
        filename = filename + '.txt'
    
    if (filename):
        file = open(filename, 'rb')
        file_contents = file.read(1024)
        while file_contents:
            for i in file_contents:
                print('yolo', i)
            # clientSocket.send(file_contents)
            # print('sending: {}'.format(str(file_contents)))
            file_contents = file.read(1024)
        file.close()
        # clientSocket.send(bytes(word, 'utf-8'))
        # with open(filename, "r") as file:
        #     for line in file:
        #         for each_word in line.split():
        #             print(each_word)
        #             clientSocket.send(bytes(each_word, 'utf-8'))
        # clientSocket.send(bytes('FINSH_SENDING_TO_CLIENT', 'utf-8'))
        count = clientSocket.recv(1024).decode()
        print('Found {} {} times in {}'.format(word, count, filename))
    else: 
        print('No file given')


def replace_word(clientSocket):
    '''
    replace word function (client):
    > reads file and sends the client each word, then upon recieving the count, displays it
    '''
    word_to_replace, replace_to = input("Please enter the word you'd like to replace, then the word you want to replace to (space-separated): ").split()
    input_file, output_file = input('Input the file to search through and file name to save to (space-separated): ').split()
    words_to_send = [word_to_replace, replace_to, output_file]
    print('DEBUG: ', words_to_send)
    for i in words_to_send:
        clientSocket.send(bytes(i, 'utf-8'))

    with open(input_file, "r") as file:
        for line in file:
            for each_word in line.split():
                print(each_word)
                clientSocket.send(bytes(each_word, 'utf-8'))
    clientSocket.send(bytes('FINSH_SENDING_TO_CLIENT', 'utf-8'))
    print(output_file, 'has been created')


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
                

def reverse_word(clientSocket): 
    input_file, output_file = input('Input the file to search through and file name to save to (space-separated): ').split()
    clientSocket.send(bytes(output_file, 'utf-8'))

    with open(input_file, "r") as file:
        for line in file:
            for each_word in line.split():
                clientSocket.send(bytes(each_word, 'utf-8'))
    clientSocket.send(bytes('FINSH_SENDING_TO_CLIENT', 'utf-8'))
    print(output_file, 'has been created')
    

def Exit(clientSocket):
    clientSocket.send(bytes('Exit', 'utf-8'))
    clientSocket.shutdown(SHUT_RDWR)
    clientSocket.close()
    exit()
        

def get_thread_name(clientSocket, userInput):
    clientSocket.send(bytes(userInput, 'utf-8'))
    thread_connected = clientSocket.recv(1024).decode()

    print(thread_connected)
    