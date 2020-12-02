#tính xác suất xuất hiện của mỗi từ trong mỗi loại văn bản

file_path_num_word = "num_word_in_label.txt"
file_path_works = "sum_word_in_label.txt"

#đọc dữ liệu  từ file
read_file_num_work = open(file_path_num_word, 'r', encoding='utf-8')
num_work = read_file_num_work.read()
read_file_works = open(file_path_works, 'r', encoding='utf-8')
works = read_file_works.read()

foo = num_work.split('\n')

# work_list[i] : chứa từ thứ i
# number_work_list là ma trận 2 chiều
# number_work_list[i][j] : số từ work_list[i] xuất hiện trong văn bản loại j
work_list = []
number_work_list = []
total = 0
for x in foo:
    #bỏ dòng cuối
    if x == '':
        break

    tmp1 = x.split(" ", 1)
    work_list.append(tmp1[0])

    tmp2 = tmp1[1].split(" ")
    tmp2.remove('')  # bỏ phần tử cuối cùng
    number_work_list.append([])
    number_work_list[total] = tmp2
    total += 1

foo = works.split('\n')

# total_works[i] : tổng số từ có trong loại văn bản i
total_works = []
for x in foo:
    # bỏ đi dòng cuối cùng
    if x == '':
        break

    y = x.split(' ')
    total_works.append(y[1])

#xử lí kết quả
P = []
for i in range(0, total):
    P.append([])
    for j in range(0, 10):
        tmp = (float(number_work_list[i][j])+1)/(float(total_works[j])+total)
        P[i].append(tmp)

#in kết quả ra file text
file_name = "probability_word_in_label.txt"

write_file_result = open(file_name, 'w', encoding='utf-8')

for i in range(0, total):
    write_file_result.write(work_list[i] + " ")
    for j in range(0, 10):
        write_file_result.write(str(P[i][j]) + " ")
    write_file_result.write("\n")
