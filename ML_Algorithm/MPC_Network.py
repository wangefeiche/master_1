"""
Know more, visit my Python tutorial page: https://morvanzhou.github.io/tutorials/
My Youtube Channel: https://www.youtube.com/user/MorvanZhou
Dependencies:
tensorflow: 1.1.0
matplotlib
numpy
"""
import tensorflow as tf
import numpy as np
import pandas as pd
from pandas import Series,DataFrame

tf.set_random_seed(1)
np.random.seed(1)

BATCH_SIZE = 8

df = pd.read_csv('MPC_train.csv')
data = df.iloc[:,0:8].values.tolist()
label = df.iloc[:,8].values.tolist()

memory = np.zeros((len(label),9))
for index in range(len(label)):
    memory[index, :] = np.hstack((data[index], [label[index]]))

#=======network==============================
tf_x = tf.placeholder(tf.float32, [None, len(data[0])])     # input x
tf_y = tf.placeholder(tf.float32, [None, 1])     # input y

l1 = tf.layers.dense(tf_x, 16, tf.nn.relu)          # hidden layer1
l2 = tf.layers.dense(l1, 32, tf.nn.relu)          # hidden layer
output = tf.layers.dense(l2, 1)                     # output layer

loss = tf.losses.mean_squared_error(tf_y, output)   # compute cost

train_op = tf.train.AdamOptimizer(0.001).minimize(loss)

sess = tf.Session()                                 # control training and others
sess.run(tf.global_variables_initializer())         # initialize var in graph

for step in range(int(len(label)/BATCH_SIZE-1)):
    # train and net output
    index_list = np.arange(step*BATCH_SIZE,(step+1)*BATCH_SIZE)
    batch_memory = memory[index_list,:]
    x = batch_memory[:, :8]
    y = batch_memory[:, 8].reshape(BATCH_SIZE,1)
    #y = np.array(label[step*BATCH_SIZE:(step+1)*BATCH_SIZE]).reshape(BATCH_SIZE,1)
    #print(y)
    _, l, pred = sess.run([train_op, loss, output], {tf_x: x, tf_y: y})
    print(l)
