#chia dữ liệu train-test theo tỉ lệ 3:1
import os

path_train = 'train/'
path_test = 'test/'
path_dataset = 'dataset/'

list_dataset = os.listdir(path_dataset)

for file in list_dataset:
    reader = open(path_dataset+file, 'r', encoding='utf-8')
    lines = reader.readlines()
    limit = 0.75*(len(lines))
    index = 1
    writter_train = open(path_train+file, 'w', encoding='utf-8')
    writter_test = open(path_test+file, 'w', encoding='utf-8')
    for line in lines:
        if index <= limit:
            writter_train.write(line)
        else:
            writter_test.write(line)
        index += 1

reader.close()
writter_train.close()
writter_test.close()