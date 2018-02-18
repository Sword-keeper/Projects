import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data", one_hot=True)
print("Download Done!")

x = tf.placeholder(tf.float32, [None, 784])

# paras
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))

y = tf.nn.softmax(tf.matmul(x, W) + b)
y_ = tf.placeholder(tf.float32, [None, 10])

# loss func
cross_entropy = -tf.reduce_sum(y_ * tf.log(y))

train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

# init
init = tf.global_variables_initializer()

# max-accuracy
max_accuracy = 0


def get_accuracy():
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float")).eval(session=sess, feed_dict={x: mnist.test.images,
                                                                                                  y_: mnist.test.labels})
    # print("Accuarcy on Test-dataset: ", accuracy)
    return accuracy


def hot(num):
    ret = [0. for x in range(10)]
    ret[num] = 1.
    return ret


def one_hot_formed(result):
    ret = [hot(result[i]) for i in range(100)]
    return ret


# ----------------------------
sess = tf.Session()
sess.run(init)

model_path = "/tmp/model_10000.ckpt"
saver = tf.train.Saver()

total = 0
for t in range(100):
    sess.run(init)
    # saver.restore(sess, model_path)

    # train
    for i in range(200):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

    total += get_accuracy()
    print(f't:{t}')
print(total / 10)

# print(get_accuracy())
# saver.save(sess, model_path)

# for t in range(20):
#     sess.run(init)
#     saver.restore(sess, model_path)
#     print(t)
#
#     for i in range(40):
#         batch_xs, batch_ys = mnist.train.next_batch(100)
#         softmax = sess.run(y, feed_dict={x: batch_xs})
#         prediction = tf.argmax(softmax, 1).eval(session=sess)
#
#         sess.run(train_step, feed_dict={x: batch_xs, y_: one_hot_formed(prediction)})
#         accuracy = get_accuracy()
#         if max_accuracy < accuracy:
#             max_accuracy = accuracy
#             save_path = saver.save(sess, model_path)
#             print(f'max_accuracy:{max_accuracy} Model saved in file: {save_path}')
#         else:
#             saver.restore(sess, model_path)
#         # print(get_accuracy())
