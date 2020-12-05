from flask import Flask, render_template, request
from pyvi import ViTokenizer
import unicodedata
import math
import regex as re
import numpy as np

#các hàm tiền xử lý dữ liệu
def convert_unicode(document):
    document = unicodedata.normalize('NFC', document)
    return document

def remove_stop_word(document):
    document_final = ""
    file_stop_word = open("../stopword.txt", "r", encoding="utf8")
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

#lấy tham số từ probability_label.txt

pro_label = open('probability_label.txt', 'r', encoding='utf-8')
pro_label_txt = pro_label.readlines()
pi = []
index = 0
for line in pro_label_txt:
    if(line != "\n"):
        words = line.split(' ')
        pi.append(float(words[1]))
pro_label.close()

def decode_label(label):
    if label == 0:
        return "Chính trị xã hội"
    if label == 1:
        return "Công nghệ"
    if label == 2:
        return "Đời sống"
    if label == 3:
        return "Khoa học"
    if label == 4:
        return "Kinh doanh"
    if label == 5:
        return "Pháp luật"
    if label == 6:
        return "Sức khỏe"
    if label == 7:
        return "Thế giới"
    if label == 8:
        return "Thể thao"
    if label == 9:
        return "Văn hóa"

# lấy thám số từ file probability_word_in_label.txt
pro_i_in_label_j = open('probability_word_in_label.txt', 'r', encoding='utf-8')
pro_i_in_label_j_txt = pro_i_in_label_j.readlines()
P = {}
for line in pro_i_in_label_j_txt:
    if(line != "\n"):
        words = line.split(' ')
        if words[0] not in P:
            P[words[0]] = []
            for i in range(1, 11):
                P[words[0]].append(float(words[i]))

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

def neural_network(x):
    # Layer 1
    layer_1 = x.dot(h_1) +b_1
    # Layer 2
    layer_2 = layer_1.dot(h_2) + b_2
    # Output layer
    out_layer = layer_2.dot(h_out) + b_out
    return out_layer

def text_vectorize(document):
    reader_dict = open('top_word.txt', 'r', encoding='utf-8')
    words = reader_dict.read()
    words = words.split('\n')
    x = np.zeros((1,400))
    word = document.split(' ')
    for w in word:
        for i in range(400):
            if w == words[i]:
                x[0][i] += 1
    return x

#hàm phân loại
def predict_naive_bayes(document):
    pr = 0
    pre = []
    document = text_preprocess(document)
    words = document.split(' ')
    for i in range(0, 10):
        value = math.log10(pi[i])
        for j in range(0, len(words)):
            if words[j] in P:
                value += math.log10(P[words[j]][i])
        pre.append(value)
        if(pre[pr] < pre[i]):
            pr = i
    return decode_label(pr)

def predict_neural_network(document):
    document = text_preprocess(document)
    x = text_vectorize(document)
    y = neural_network(x)
    pr = 0
    for i in range(10):
        if y[0][i] > y[0][pr]:
            pr = i
    return decode_label(pr)
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

# english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
# trainer = ChatterBotCorpusTrainer(english_bot)
# trainer.train("chatterbot.corpus.english")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    answer = "Theo giải thuật Naive Bayes: "+predict_naive_bayes(userText)+\
             ". Theo neural network: "+predict_neural_network(userText)
    return answer
"""
    if "full name of Han" in userText:
    	return "Nguyen Nam Han"
    elif "university" and "han" in userText:
    	return "HUST"
    # else:
    # 	return str(english_bot.get_response(userText))
    else:
    	return "khong hieu"
"""
if __name__ == "__main__":
    app.run(debug = True) 


