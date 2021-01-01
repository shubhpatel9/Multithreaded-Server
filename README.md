# Multithreaded-Server
Develop a Cloud File Processor in Python using low-level socket programming. Develop a client and a corresponding cloud-computing server that handles one client at a time. The client asks the user for the specific file processing operation to be performed and then sends the input text file and other necessary information to the server, which in turn performs the desired operation on the received file and returns the output or the modified file content to the client. The following operations must be supported: • (25 Points) SearchWord – This operation asks the server to determine the number of  3 occurrences of a specified word in a specified text file. The client must prompt the user to enter the name of a text file and the word to search for in the file. The client then transfers the file content and the word to the server, which in turn calculates the number of occurrences of the specified word in the received text file and then returns the result to the client. Finally, the client must display the output in a well-formatted message. • (25 Points) ReplaceWord – This operation asks the server to replace a specified word by another specified word in a specified input text file. The client must prompt the user to enter two words, the name of an input text file, and the name of the output file. The client then transfers the input file content and the two words to the server, which in turn produces a modified file content with every occurrence of the first word being replaced by the second word. Finally, the client must store the received modified file content as a file with the specified output file name. • (25 Points) ReverseWords – This operation asks the server to reverse the order of words in a specified text file. The client must prompt the user to enter the names of the input and output files. The client then transfers the input file content to the server, which in turn reverses the order of words and returns the modified file content to the client. Finally, the client must store the received modified content as a file with the specified output file name. • (10 Points) DisplayFile – This operation asks the client to display the content of the specified local filename. This is a local operation, which does not interact with the server. • (15 Points) Exit – When the server receives this command from the client, it must close the connection with the client and wait for a new client connection. The client program then terminates.  Next, Support multithreading and file compression  
