import os
import numpy as np

#lấy dữ liệu cho các tham số
reader_weight_h1 = open('weight_h1.txt', 'r', encoding='utf-8')
reader_weight_h2 = open('weight_h2.txt', 'r', encoding='utf-8')
reader_weight_out = open('weight_out.txt', 'r', encoding='utf-8')
reader_bias_b1 = open('bias_b1.txt', 'r', encoding='utf-8')
reader_bias_b2 = open('bias_b2.txt', 'r', encoding='utf-8')
reader_bias_out = open('bias_out.txt', 'r', encoding='utf-8')

h_1 = np.zeros((400, 100))
h_2 = np.zeros((100, 100))
h_out = np.zeros((100, 10))
b_1 = np.zeros(100)
b_2 = np.zeros(100)
b_out = np.zeros(10)

weight_h1 = reader_weight_h1.readlines()
for i in range(len(weight_h1)):
    words = weight_h1[i].split(' ')
    for j in range(len(words)-1):
        h_1[i][j] = float(words[j])

weight_h2 = reader_weight_h2.readlines()
for i in range(len(weight_h2)):
    words = weight_h2[i].split(' ')
    for j in range(len(words)-1):
        h_2[i][j] = float(words[j])

weight_out = reader_weight_out.readlines()
for i in range(len(weight_out)):
    words = weight_out[i].split(' ')
    for j in range(len(words)):
        h_out[i][j] = float(words[j])

bias_b1 = reader_bias_b1.read()
words = bias_b1.split(' ')
for i in range(len(words)):
    b_1[i] = float(words[i])

bias_b2 = reader_bias_b2.read()
words = bias_b2.split(' ')
for i in range(len(words)):
    b_2[i] = float(words[i])

bias_out = reader_bias_out.read()
words = bias_out.split(' ')
for i in range(len(words)):
    b_out[i] = float(words[i])

#hàm tính toán theo neural network
def neural_network(x):
    #Hidden layer 1
    layer_1 = x.dot(h_1) +b_1
    #Hidden layer 2
    layer_2 = layer_1.dot(h_2) + b_2
    # Output layer
    out_layer = layer_2.dot(h_out) + b_out
    return out_layer

def text_vectorize(document):
    reader_dict = open('top_word.txt', 'r', encoding='utf-8')
    words = reader_dict.read()
    words = words.split('\n')
    x = np.zeros((1, 400))
    word = document.split(' ')
    for w in word:
        for i in range(400):
            if w == words[i]:
                x[0][i] += 1
    return x

#hàm dự đoán kết quả
def predict(document):
    x = text_vectorize(document)
    y = neural_network(x)
    pr = 0
    for i in range(10):
        if y[0][i] > y[0][pr]:
            pr = i
    return pr

#lưu kết quả ra các file recall, precision, result
writter_recall = open('recall.txt', 'w', encoding='utf-8')
writter_precision = open('precision.txt', 'w', encoding='utf-8')
writter_result = open('result.txt', 'w', encoding='utf-8')

path = '../test/'
test_file = os.listdir(path)

overall = 0
predi = np.zeros((10, 10))

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

