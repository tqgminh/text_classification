#tính số lần xuất hiện của từ trong mỗi loại văn bản
import os

dictionary = {}

path = '../train/'
files = os.listdir(path)

#lưu các từ vào từ điển
for file in files:
    f = open(path + file, 'r', encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        words = line.split(' ')
        for i in range(1, len(words) - 1):
            if words[i] not in dictionary:
                dictionary[words[i]] = 0

#đếm số lần các từ xuất hiện trong mỗi loại văn bản
num_word_in_label = []
for i in range(0, 10):
    num_word_in_label.append({})
    for j in dictionary:
        num_word_in_label[i][j] = 0

for file in files:
    f = open(path + file, 'r', encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        words = line.split(' ')
        for i in range(1, len(words) - 1):
            num_word_in_label[int(words[0])][words[i]] += 1

#lưu kết quả ra file
f = open('num_word_in_label.txt', 'w', encoding='utf-8')
for i in dictionary:
    f.write(i + " ")
    for j in range(0, 10):
        f.write(str(num_word_in_label[j][i]))
        f.write(" ")
    f.write("\n")
