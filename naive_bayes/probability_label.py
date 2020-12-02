#tính xác suất mỗi loại văn bản
import os

path = '../train/'

files = os.listdir(path)
label = 0
sum = 0
w = open('probability_label.txt', 'w', encoding='utf-8')
for file in files:
    f = open(path+file, 'r', encoding='utf-8')
    lines = f.readlines()
    sum += len(lines)

for file in files:
    f = open(path+file, 'r', encoding='utf-8')
    lines = f.readlines()
    w.write(str(label)+" "+str(len(lines)/sum)+"\n")
    label += 1