import os
import numpy as np

train_path = '../train/'
test_path = '../test/'
train_file = os.listdir(train_path)
test_file = os.listdir(train_path)

writter_input_train = open('input_train_vector.txt', 'w', encoding='utf-8')
writter_input_test = open('input_test_vector.txt', 'w', encoding='utf-8')
writter_output_train = open('output_train_vector.txt', 'w', encoding='utf-8')
writter_output_test = open('output_test_vector.txt', 'w', encoding='utf-8')

#mã hóa các văn bản train và test, nhãn thành các vector
#văn bản là vector 400 chiều
#nhãn là vector 10 chiều
dict = {}
reader_dict = open('top_word.txt', 'r', encoding='utf-8')
words = reader_dict.read()
words = words.split('\n')

for file in train_file:
    reader = open(train_path+file, 'r', encoding='utf-8')
    lines = reader.readlines()
    for line in lines:
        x = np.zeros(400)
        word_line = line.split(' ')
        for w in word_line[1:len(word_line)-1]:
            for i in range(400):
                if w == words[i]:
                    x[i] += 1
        for i in range(400):
            writter_input_train.write(str(x[i])+" ")
        writter_input_train.write("\n")
        for i in range(10):
            if int(word_line[0]) == i:
                writter_output_train.write("1 ")
            else:
                writter_output_train.write("0 ")
        writter_output_train.write("\n")

for file in test_file:
    reader = open(test_path+file, 'r', encoding='utf-8')
    lines = reader.readlines()
    for line in lines:
        x = np.zeros(400)
        word_line = line.split(' ')
        for w in word_line[1:len(word_line)-1]:
            for i in range(400):
                if w == words[i]:
                    x[i] += 1
        for i in range(400):
            writter_input_test.write(str(x[i])+" ")
        writter_input_test.write("\n")
        for i in range(10):
            if int(word_line[0]) == i:
                writter_output_test.write("1 ")
            else:
                writter_output_test.write("0 ")
        writter_output_test.write("\n")
