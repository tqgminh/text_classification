#tính tổng số từ trong một loại văn bản
import os

path = '../train/'

files = os.listdir(path)

writer = open('sum_word_in_label.txt', 'w', encoding='utf-8')
index = 0
for file in files:
    sum = 0
    reader = open(path+file, 'r', encoding='utf-8')
    lines = reader.readlines()
    for line in lines:
        words = line.split(' ')
        sum += len(words)-2
    writer.write(str(index)+" "+str(sum)+"\n")
    index +=1