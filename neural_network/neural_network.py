import numpy as np
import tensorflow as tf

#đọc các vector đầu vào, đầu ra từ văn bản đã được mã hóa
reader_train_input = open('input_train_vector.txt', 'r', encoding='utf-8')
lines = reader_train_input.readlines()
X_train = np.zeros((len(lines), 400))
index = 0
for line in lines:
    words = line.split(' ')
    for i in range(400):
        X_train[index][i] = float(words[i])
    index += 1

reader_train_output = open('output_train_vector.txt', 'r', encoding='utf-8')
lines = reader_train_output.readlines()
Y_train = np.zeros((len(lines), 10))
index = 0
for line in lines:
    words = line.split(' ')
    for i in range(10):
        Y_train[index][i] = float(words[i])
    index += 1

reader_test_input = open('input_test_vector.txt', 'r', encoding='utf-8')
lines = reader_test_input.readlines()
X_test = np.zeros((len(lines), 400))
index = 0
for line in lines:
    words = line.split(' ')
    for i in range(400):
        X_test[index][i] = float(words[i])
    index += 1

reader_test_output = open('output_test_vector.txt', 'r', encoding='utf-8')
lines = reader_test_output.readlines()
Y_test = np.zeros((len(lines), 10))
index = 0
for line in lines:
    words = line.split(' ')
    for i in range(10):
        Y_test[index][i] = float(words[i])
    index += 1

#các tham số cho mô hình
learning_rate = 0.1
num_steps = 1000
display_step = 100

n_hidden_1 = 100
n_hidden_2 = 100
input_shape = 400
num_classes = 10

#xây dựng mô hình neural network
tf.compat.v1.disable_eager_execution()
X = tf.compat.v1.placeholder("float", [None, input_shape])
Y = tf.compat.v1.placeholder("float", [None, num_classes])

#ma trận kết nối các tầng
weights = {
    'h1': tf.Variable(tf.random.normal([input_shape, n_hidden_1])),
    'h2': tf.Variable(tf.random.normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random.normal([n_hidden_2, num_classes]))
}

#tham số bias ở các tầng
biases = {
    'b1': tf.Variable(tf.random.normal([n_hidden_1])),
    'b2': tf.Variable(tf.random.normal([n_hidden_2])),
    'out': tf.Variable(tf.random.normal([num_classes]))
}

#tính toán theo mạng neural
def neural_net(x):
    # layer 1
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    # layer 2
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    # Output layer
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

logits = neural_net(X)

# Khởi tạo loss function và optimizer
loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=Y))
optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss_op)

# Đánh giá model
correct_pred = tf.equal(tf.argmax(logits, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# ops khởi tạo các biến của graph
init = tf.compat.v1.global_variables_initializer()

with tf.compat.v1.Session() as sess:
    sess.run(init)
    for step in range(1,num_steps+1):
        sess.run(train_op, feed_dict={X: X_train, Y: Y_train})
        if step%display_step == 0 or step == 1:
            loss, acc = sess.run([loss_op, accuracy], feed_dict={X: X_train, Y: Y_train})
            print("Step " + str(step) + ", Minibatch Loss= " + \
                  "{:f}".format(loss) + ", Training Accuracy= " + \
                  "{:f}".format(acc))
    print("Optimization Finished!")
    print("Testing Accuracy:", \
          sess.run(accuracy, feed_dict={X: X_test, Y: Y_test}))
    #lấy kết quả đã training
    weights_h1, weights_h2, weights_out, biases_b1, biases_b2, biases_out = sess.run([weights['h1'], weights['h2'], weights['out'], biases['b1'], biases['b2'], biases['out']])

#ghi kết quả các tham số weight và bias ra console
for i in range(input_shape):
    for j in range(n_hidden_1):
        print(str(weights_h1[i][j]), end=' ')
    print('')
print("\n")

for i in range(n_hidden_1):
    for j in range(n_hidden_2):
        print(str(weights_h2[i][j]), end=' ')
    print('')
print("\n")


for i in range(n_hidden_2):
    for j in range(num_classes):
        print(str(weights_out[i][j]), end=' ')
    print('')
print("\n")

for i in range(n_hidden_1):
    print(str(biases_b1[i]), end=' ')
print("\n")


for i in range(n_hidden_2):
    print(str(biases_b2[i]), end=' ')
print("\n")

for i in range(num_classes):
    print(str(biases_out[i]), end=' ')

