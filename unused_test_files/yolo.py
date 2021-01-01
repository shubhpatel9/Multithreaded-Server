import gzip
import re
import sys

def compress_file(input_file, compressed_file_name):
    if compressed_file_name[-7::] != '.txt.gz':
        compressed_file_name = compressed_file_name + '.txt.gz'
    f = gzip.GzipFile(compressed_file_name, 'wb')
    f.write(open(input_file, "rb").read())
    f.close()
    print('file_compressed')
    return f

def uncompress_file(compressed_file_name):
    if compressed_file_name[-7::] != '.txt.gz':
        compressed_file_name = compressed_file_name + '.txt.gz'
    return gzip.GzipFile(compressed_file_name, "r").read().decode("utf-8")

def uncompress_file_from_GZIP(compressed_file_name):
    return gzip.decompress(compressed_file_name)

def send_file(clientSocket, fileName):
    file = open(fileName, 'rb')
    file_contents = file.read()
    size = sys.getsizeof(file_contents)
    file.close()

    print(type(file_contents), type(str(file_contents)))
    print('size of file: {}, file:'.format(size))
    # print(file_contents)

def count_string(fileName, word):
    count = 0
    file = open(fileName, 'rb')
    file_contents = file.read()
    file_contents = str(file_contents)
    parsed_contents = re.findall(r"[\w']+|[.,!?;]", file_contents)
    for i in parsed_contents:
        if i == 'word':
            count += 1
    return count


# def replace_word(fileName, word, replace):
#     file = open(fileName, 'rb')
#     file_contents = file.read()
#     file_contents = str(file_contents)
#     parsed_contents = re.findall(r"[\w']+|[.,!?;]", file_contents)

def replace(output, fileName, replace, new):
  file = open(fileName, 'rb')
  file_contents = file.read()
  file_contents = str(file_contents)
  regex = r"((\s|\n|\t|n|\(|\`)"+replace+")"
  subst = " " + new
  result = re.sub(regex, subst, file_contents, 0, re.MULTILINE | re.IGNORECASE)
  new = open(output, 'w+')
  new.write(result)
  new.close()





testing_compression = 2


if testing_compression == 1:
    yolo = compress_file('input.txt', 'compressed_out')
    print(type(yolo), yolo)
    print(uncompress_file_from_GZIP(yolo))
    print(uncompress_file('compressed_out'))
elif testing_compression == 0:
    send_file(0, 'alice.txt')
    print('counts: ', count_string('alice.txt', 'alice'))
elif testing_compression == 2:
    replace('test1.txt','alice.txt', 'Alice', 'shubh')

