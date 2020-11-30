from pyvi import ViTokenizer
import unicodedata
import sys
import regex as re

#hàm chuẩn hóa unicode
def convert_unicode(document):
    document = unicodedata.normalize('NFC', document)
    return document

#hàm xóa các stop word
def remove_stop_word(document):
    document_final = ""
    file_stop_word = open("stopword.txt", "r", encoding="utf8")
    stop_word_list = file_stop_word.read()
    stop_word = stop_word_list.split('\n')
    document_list = document.split()
    for word in document_list:
        if(word not in stop_word_list):
            document_final = document_final+word+" "
    return document_final

bang_nguyen_am = [['a', 'à', 'á', 'ả', 'ã', 'ạ', 'a'],
                  ['ă', 'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ', 'aw'],
                  ['â', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ', 'aa'],
                  ['e', 'è', 'é', 'ẻ', 'ẽ', 'ẹ', 'e'],
                  ['ê', 'ề', 'ế', 'ể', 'ễ', 'ệ', 'ee'],
                  ['i', 'ì', 'í', 'ỉ', 'ĩ', 'ị', 'i'],
                  ['o', 'ò', 'ó', 'ỏ', 'õ', 'ọ', 'o'],
                  ['ô', 'ồ', 'ố', 'ổ', 'ỗ', 'ộ', 'oo'],
                  ['ơ', 'ờ', 'ớ', 'ở', 'ỡ', 'ợ', 'ow'],
                  ['u', 'ù', 'ú', 'ủ', 'ũ', 'ụ', 'u'],
                  ['ư', 'ừ', 'ứ', 'ử', 'ữ', 'ự', 'uw'],
                  ['y', 'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ', 'y']]
bang_ky_tu_dau = ['', 'f', 's', 'r', 'x', 'j']

nguyen_am_to_ids = {}

for i in range(len(bang_nguyen_am)):
    for j in range(len(bang_nguyen_am[i]) - 1):
        nguyen_am_to_ids[bang_nguyen_am[i][j]] = (i, j)

def chuan_hoa_dau_tu_tieng_viet(word):
    if not is_valid_vietnam_word(word):
        return word

    chars = list(word)
    dau_cau = 0
    nguyen_am_index = []
    qu_or_gi = False
    for index, char in enumerate(chars):
        x, y = nguyen_am_to_ids.get(char, (-1, -1))
        if x == -1:
            continue
        elif x == 9:  # check qu
            if index != 0 and chars[index - 1] == 'q':
                chars[index] = 'u'
                qu_or_gi = True
        elif x == 5:  # check gi
            if index != 0 and chars[index - 1] == 'g':
                chars[index] = 'i'
                qu_or_gi = True
        if y != 0:
            dau_cau = y
            chars[index] = bang_nguyen_am[x][0]
        if not qu_or_gi or index != 1:
            nguyen_am_index.append(index)
    if len(nguyen_am_index) < 2:
        if qu_or_gi:
            if len(chars) == 2:
                x, y = nguyen_am_to_ids.get(chars[1])
                chars[1] = bang_nguyen_am[x][dau_cau]
            else:
                x, y = nguyen_am_to_ids.get(chars[2], (-1, -1))
                if x != -1:
                    chars[2] = bang_nguyen_am[x][dau_cau]
                else:
                    chars[1] = bang_nguyen_am[5][dau_cau] if chars[1] == 'i' else bang_nguyen_am[9][dau_cau]
            return ''.join(chars)
        return word

    for index in nguyen_am_index:
        x, y = nguyen_am_to_ids[chars[index]]
        if x == 4 or x == 8:  # ê, ơ
            chars[index] = bang_nguyen_am[x][dau_cau]
            # for index2 in nguyen_am_index:
            #     if index2 != index:
            #         x, y = nguyen_am_to_ids[chars[index]]
            #         chars[index2] = bang_nguyen_am[x][0]
            return ''.join(chars)

    if len(nguyen_am_index) == 2:
        if nguyen_am_index[-1] == len(chars) - 1:
            x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
            chars[nguyen_am_index[0]] = bang_nguyen_am[x][dau_cau]
            # x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
            # chars[nguyen_am_index[1]] = bang_nguyen_am[x][0]
        else:
            # x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
            # chars[nguyen_am_index[0]] = bang_nguyen_am[x][0]
            x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
            chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
    else:
        # x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
        # chars[nguyen_am_index[0]] = bang_nguyen_am[x][0]
        x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
        chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
        # x, y = nguyen_am_to_ids[chars[nguyen_am_index[2]]]
        # chars[nguyen_am_index[2]] = bang_nguyen_am[x][0]
    return ''.join(chars)


def is_valid_vietnam_word(word):
    chars = list(word)
    nguyen_am_index = -1
    for index, char in enumerate(chars):
        x, y = nguyen_am_to_ids.get(char, (-1, -1))
        if x != -1:
            if nguyen_am_index == -1:
                nguyen_am_index = index
            else:
                if index - nguyen_am_index != 1:
                    return False
                nguyen_am_index = index
    return True


def chuan_hoa_dau_cau_tieng_viet(sentence):
    """
        Chuyển câu tiếng việt về chuẩn gõ dấu kiểu cũ.
        :param sentence:
        :return:
        """
    sentence = sentence.lower()
    words = sentence.split()
    for index, word in enumerate(words):
        cw = re.sub(r'(^\p{P}*)([p{L}.]*\p{L}+)(\p{P}*$)', r'\1/\2/\3', word).split('/')
        # print(cw)
        if len(cw) == 3:
            cw[1] = chuan_hoa_dau_tu_tieng_viet(cw[1])
        words[index] = ''.join(cw)
    return ' '.join(words)
#u=chuan_hoa_dau_cau_tieng_viet('ghế nghìên hơn vựơn hoà thuỷ uỷ quỳnh gỉa hòan khuỷu gìa thuỳên đang làm gì')
#print(u)

def text_preprocess(document):
    # chuẩn hóa unicode
    document = convert_unicode(document)
    # chuẩn hóa cách gõ dấu tiếng Việt
    document = chuan_hoa_dau_cau_tieng_viet(document)
    # tách từ
    document = ViTokenizer.tokenize(document)
    # đưa về lower
    document = document.lower()
    # xóa các ký tự không cần thiết
    document = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_]',' ',document)
    # xóa khoảng trắng thừa
    document = re.sub(r'\s+', ' ', document).strip()
    # xóa stop word
    document = remove_stop_word(document)
    return document

import os

path_train = 'Train_Full/Chinh tri Xa hoi/'
path_test = 'Test_Full/Chinh tri Xa hoi/'
writer = open('dataset/chinh_tri_xa_hoi.txt', 'w', encoding='utf-8')
files_train = os.listdir(path_train)
files_test = os.listdir(path_test)
for file in files_train:
    reader = open(path_train+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("0 "+text+"\n")
for file in files_test:
    reader = open(path_test+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("0 "+text+"\n")

path_train = 'Train_Full/Cong nghe/'
path_test = 'Test_Full/Cong nghe/'
writer = open('dataset/cong_nghe.txt', 'w', encoding='utf-8')
files_train = os.listdir(path_train)
files_test = os.listdir(path_test)
for file in files_train:
    reader = open(path_train+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("1 "+text+"\n")
for file in files_test:
    reader = open(path_test+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("1 "+text+"\n")

path_train = 'Train_Full/Doi song/'
path_test = 'Test_Full/Doi song/'
writer = open('dataset/doi_song.txt', 'w', encoding='utf-8')
files_train = os.listdir(path_train)
files_test = os.listdir(path_test)
for file in files_train:
    reader = open(path_train+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("2 "+text+"\n")
for file in files_test:
    reader = open(path_test+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("2 "+text+"\n")

path_train = 'Train_Full/Khoa hoc/'
path_test = 'Test_Full/Khoa hoc/'
writer = open('dataset/khoa_hoc.txt', 'w', encoding='utf-8')
files_train = os.listdir(path_train)
files_test = os.listdir(path_test)
for file in files_train:
    reader = open(path_train+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("3 "+text+"\n")
for file in files_test:
    reader = open(path_test+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("3 "+text+"\n")

path_train = 'Train_Full/Kinh doanh/'
path_test = 'Test_Full/Kinh doanh/'
writer = open('dataset/kinh_doanh.txt', 'w', encoding='utf-8')
files_train = os.listdir(path_train)
files_test = os.listdir(path_test)
for file in files_train:
    reader = open(path_train+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("4 "+text+"\n")
for file in files_test:
    reader = open(path_test+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("4 "+text+"\n")

path_train = 'Train_Full/Phap luat/'
path_test = 'Test_Full/Phap luat/'
writer = open('dataset/phap_luat.txt', 'w', encoding='utf-8')
files_train = os.listdir(path_train)
files_test = os.listdir(path_test)
for file in files_train:
    reader = open(path_train+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("5 "+text+"\n")
for file in files_test:
    reader = open(path_test+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("5 "+text+"\n")

path_train = 'Train_Full/Suc khoe/'
path_test = 'Test_Full/Suc khoe/'
writer = open('dataset/suc_khoe.txt', 'w', encoding='utf-8')
files_train = os.listdir(path_train)
files_test = os.listdir(path_test)
for file in files_train:
    reader = open(path_train+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("6 "+text+"\n")
for file in files_test:
    reader = open(path_test+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("6 "+text+"\n")

path_train = 'Train_Full/The gioi/'
path_test = 'Test_Full/The gioi/'
writer = open('dataset/the_gioi.txt', 'w', encoding='utf-8')
files_train = os.listdir(path_train)
files_test = os.listdir(path_test)
for file in files_train:
    reader = open(path_train+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("7 "+text+"\n")
for file in files_test:
    reader = open(path_test+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("7 "+text+"\n")

path_train = 'Train_Full/The thao/'
path_test = 'Test_Full/The thao/'
writer = open('dataset/the_thao.txt', 'w', encoding='utf-8')
files_train = os.listdir(path_train)
files_test = os.listdir(path_test)
for file in files_train:
    reader = open(path_train+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("8 "+text+"\n")
for file in files_test:
    reader = open(path_test+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("8 "+text+"\n")

path_train = 'Train_Full/Van hoa/'
path_test = 'Test_Full/Van hoa/'
writer = open('dataset/van_hoa.txt', 'w', encoding='utf-8')
files_train = os.listdir(path_train)
files_test = os.listdir(path_test)
for file in files_train:
    reader = open(path_train+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("9 "+text+"\n")
for file in files_test:
    reader = open(path_test+file, 'r', encoding='utf-16')
    text = reader.read()
    text = text_preprocess(text)
    writer.write("9 "+text+"\n")

