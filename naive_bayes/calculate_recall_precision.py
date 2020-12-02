import math
import os
import numpy as np

# lấy dữ liệu cho mảng pi: xác suất là một loại văn bản
pro_label = open('probability_label.txt', 'r', encoding='utf-8')
pro_label_txt = pro_label.readlines()
pi = []
index = 0
for line in pro_label_txt:
    if(line != "\n"):
        words = line.split(' ')
        pi.append(float(words[1]))
pro_label.close()

# lấy dữ liệu mảng p: xác suất từ i xuất hiện trong văn bản loại j
probability_word_in_label = open('probability_word_in_label.txt', 'r', encoding='utf-8')
probability_word_in_label_txt = probability_word_in_label.readlines()

P = {}

for line in probability_word_in_label_txt:
    if(line != ""):
        words = line.split(' ')
        if words[0] not in P:
            P[words[0]] = []
            for i in range(1, 11):
                P[words[0]].append(float(words[i]))

#hàm dự đoán theo công thức
def predict(document):
    pr = 0
    pre = []
    words = document.split(' ')
    for i in range(0, 10):
        value = math.log10(pi[i])
        for word in words:
            if word in P:
                value += math.log10(P[word][i])
        pre.append(value)
        if(pre[pr] < pre[i]):
            pr = i
    return pr

writter_recall = open('recall.txt', 'w', encoding='utf-8')
writter_precision = open('precision.txt', 'w', encoding='utf-8')
writter_result = open('result.txt', 'w', encoding='utf-8')

path = '../test/'
test_file = os.listdir(path)

overall = 0
predi = np.zeros((10, 10))

#ghi kết quả ra các file recall, precision, result
i = 0
for file in test_file:
    f = open(path+file, 'r', encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        predi[i][predict(line[2:])] += 1
    i += 1
right = 0
for i in range(10):
    right += predi[i][i]
    writter_recall.write(str(i)+" "+str(predi[i][i]/np.sum(predi[i, :]))+"\n")
    writter_precision.write(str(i)+" "+str(predi[i][i]/np.sum(predi[:, i]))+"\n")
writter_recall.write("Overall: "+str(right/np.sum(predi)))
writter_precision.write("Overall: "+str(right/np.sum(predi)))

for i in range(10):
    for j in range(10):
        writter_result.write(str(int(predi[i][j]))+" ")
    writter_result.write("\n")

