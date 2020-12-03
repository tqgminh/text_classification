import os

path_train = '../train/'
train_file = os.listdir(path_train)

#thống kê 40 từ xuất hiện nhiều nhất ở mỗi loại văn bản
writter = open('top_word.txt', 'w', encoding='utf-8')
top_word = {}
for file in train_file:
    dict = {}
    reader = open(path_train+file, 'r', encoding='utf-8')
    lines = reader.readlines();
    for line in lines:
        words = line.split(' ')
        for word in words[1:len(words)-1]:
            if word not in dict:
                dict[word] = 0
            else:
                dict[word] += 1
    new_dict = sorted(dict, key=dict.get, reverse=True)
    index = 0
    for word in new_dict:
        if index < 40:
            if word not in top_word:
                top_word[word] = 0
                writter.write(word+"\n")
                index += 1
