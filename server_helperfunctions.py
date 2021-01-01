from socket import *
import threading as thread
import re
import sys
import gzip
import time

# ========================== time class =================================
#metric used to compare results between single threaded server and multithreaded server
class Time_Track: 
    def __init__(self):
        self.start_time = time.time()
        self.time_flags = []
        self.client_history = {}
        self.extrarun = {}

    def add_history(self, action):
        if action in self.client_history.keys():
            if action in self.extrarun.keys():
                self.extrarun[action] = self.extrarun[action] =+ 1
            else:
                self.extrarun[action] = 0
            action = action + str(self.extrarun[action])

        action_time = self.time_now()
        self.client_history[action] = action_time
        return action

    def complete_action(self, action):
        self.client_history[action] = self.time_now() - self.client_history[action]

    def display_history(self):
        print('client\'s history:')
        print('--------------------------')
        for i in self.client_history.keys():
            print('{} took {} milliseconds to run!'.format(i, self.client_history[i]))
        print('--------------------------')

#setting a flag for when the operation starts running 
#to eliminate the time it takes for the user to type the input on the client side
    def set_flag(self): 
        current = len(self.time_flags)
        self.time_flags.append(time.time())
        return current
    
    def get_flag_time(self, flag_idx):
        flag_time = time.time() - self.time_flags[flag_idx]
        self.time_flags.pop(flag_idx)
        return flag_time
    
    def time_now(self):
        return time.time() - self.start_time
# ========================================================================

# ============================ compression ==============================
def compress_file(input_file, compressed_file_name):
    '''
        compress the file
    '''
    compressed_file_name = compressed_file_name + '.txt.gz'
    f = gzip.GzipFile(compressed_file_name, 'wb')
    f.write(open(input_file, "rb").read())
    f.close()
    print('file_compressed')
    return f

def uncompress_file(compressed_file_name):
    '''
        uncompress the file and return its contents
    '''
    compressed_file_name = compressed_file_name + '.txt.gz'
    return gzip.GzipFile("compressed.txt.gz", "r").read().decode("utf-8")

# ============================== helper =================================

def recieve_file(connectionSocket):
    incoming_size = int(connectionSocket.recv(1024).decode())
    file_contents = str(connectionSocket.recv(incoming_size).decode())
    return file_contents

def count_string(file, word):
    count = 0
    file_contents = str(file)
    parsed_contents = re.findall(r"[\w']+|[.,!?;]", file_contents)
    for i in parsed_contents:
        if i.lower() == word.lower():
            count += 1
    return count

def replace(file, replace, new):
    regex = r"((\s|\n|\t|n|\(|\`)"+replace+")"
    subst = " " + new
    result = re.sub(regex, subst, file, 0, re.MULTILINE | re.IGNORECASE)
    return result

# ============================== server =================================

# testing compression sending
def random(connectionSocket):
    file = connectionSocket.resc(1024).decode()

    compress_file(file+'.txt', 'compressed_version')

# search word
def search_word(connectionSocket, server_time):
    '''
        Search Word Function: 
        > finds the number of occurances of the word from the words sent from client
    '''
    action_name = server_time.add_history('search_word')

    word_to_search = connectionSocket.recv(1024).decode()

    print('recieving file...')

    incoming_file = recieve_file(connectionSocket)

    print('file-contents: \n:', incoming_file)

    count = int(count_string(incoming_file, word_to_search))

    connectionSocket.send(bytes(str(count), 'utf-8'))

    if count == 0:
        print("{} not passed".format(word_to_search))
    else:
        print('Found \"{}\" {} times'.format(word_to_search, count))

    server_time.complete_action(action_name)

    
def replace_word(connectionSocket, server_time): 
    action_name = server_time.add_history('replace_word')

    # get input from client
    word_to_replace = connectionSocket.recv(1024).decode()
    replace_to = connectionSocket.recv(1024).decode()
    print('DEBUG: ', word_to_replace, replace_to)

    incoming_file = recieve_file(connectionSocket)

    result = replace(incoming_file, word_to_replace, replace_to)

    size = str(sys.getsizeof(result))

    connectionSocket.send(bytes(size, 'utf-8'))

    connectionSocket.send(bytes(result, 'utf-8'))

    server_time.complete_action(action_name)



def reverse_word(connectionSocket, server_time): 
    action_name = server_time.add_history('reverse_word')
    
    output_file = connectionSocket.recv(1024).decode()
    
    if (output_file[-4:] != '.txt'):
        output_file = output_file + '.txt'

    created_file = open(output_file, 'w+')

    words = []
    
    word_stream = connectionSocket.recv(1024).decode()
    if (word_stream != None):
        # get words from client
        while word_stream != 'FINSH_SENDING_TO_CLIENT':
            if word_stream != 'FINSH_SENDING_TO_CLIENT':
                word_stream = word_stream + ' '
                words.append(word_stream)
            word_stream = connectionSocket.recv(1024).decode()
        word_stream = ''
    
    for i in words[::-1]:
        created_file.write(i)

    created_file.close()

    server_time.complete_action(action_name)


# ===================================================================
