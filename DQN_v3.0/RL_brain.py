# Refenced [MorvanZhou/Reinforcement-learning-with-tensorflow/contents/5_Deep_Q_Network/](https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/tree/master/contents/5_Deep_Q_Network)

import numpy as np
import pandas as pd
import tensorflow as tf


tf.logging.set_verbosity(tf.logging.ERROR)
np.random.seed(1)
tf.set_random_seed(1)

# Deep Q Network off-policy
class DQN:
    def __init__(
            self,
            n_currency_pairs,
            n_actions,
            n_features,
            learning_rate=0.01,
            reward_decay=0.9,
            e_greedy=0.9,
            replace_target_iter=300,
            memory_size=500,
            batch_size=32,
            e_greedy_increment=None,
            output_graph=False,
    ):
        self.n_currency_pairs = n_currency_pairs
        self.n_actions = n_actions
        self.n_features = n_features
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon_max = e_greedy
        self.replace_target_iter = replace_target_iter
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.epsilon_increment = e_greedy_increment
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max


        self.learn_step_counter = 0
        self.memory = np.zeros((self.memory_size, self.n_features * self.n_currency_pairs * 2 + 2))
        self._build_net()
        t_params = tf.get_collection('target_net_params')
        e_params = tf.get_collection('eval_net_params')
        self.replace_target_op = [tf.assign(t, e) for t, e in zip(t_params, e_params)]
        self.sess = tf.Session()

        if output_graph:
            tf.summary.FileWriter("logs/tensorboard_logs", self.sess.graph)

        self.sess.run(tf.global_variables_initializer())
        self.cost_his = []

    def weight_variable(self, shape):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)

    def bias_variable(self,shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    def conv2d(self,x, W):
        temp = tf.nn.conv2d(x, filter=W, strides=[1, 1, 1, 1], padding='SAME')
        # print('CONV2D'*5)
        # print("\n\n x: {} \n W: {} \n temp: {} ".format(x, W, temp))
        return temp

    def max_pool_pairs_x_timestamps(self, input, n_pairs, n_timestamps):
        return tf.nn.max_pool(input, ksize=[1, 2, 2, 1], strides=[1, n_pairs, n_timestamps, 1], padding='SAME')


    def _build_net(self):
        # ------------------ build evaluate_net ------------------
        self.x = tf.placeholder(tf.float32, [None, self.n_features * self.n_currency_pairs], name = 's')
        self.s = tf.reshape(self.x, [-1, self.n_currency_pairs, self.n_features, 1])


        W = tf.Variable(tf.zeros([self.n_features * self.n_currency_pairs, self.n_actions]))
        b = tf.Variable(tf.zeros([self.n_actions]))

        self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name='Q_target')  # for calculating loss

        #########################################################
        with tf.variable_scope('eval_net'):
            # c_names(collections_names) are the collections to store variables
            c_names = ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES]
            # first layer. collections is used later when assign to target net
            with tf.variable_scope('l1'):
                W_conv1 = self.weight_variable([3, 3, 1, 32])
                b_conv1 = self.bias_variable([32])

                # DQN_v2.5 setting:
                    # self.s = [-1,3,300,1]
                    # strides = [1, 2, 25, 1]
                    # filter = [6, 6, 1, 32]
                h_conv1 = tf.nn.relu(self.conv2d(self.s, W_conv1) + b_conv1)
                # print('@3'*10 + " before h_conv1_relu shape " + '@3'*10)
                # print(self.conv2d(self.s, W_conv1) + b_conv1)

                # print('@3'*10 + " before h_conv1_relu shape " + '@3.1'*10)
                # print(h_conv1)


                h_pool1 = self.max_pool_pairs_x_timestamps(h_conv1, 2, 2)
                # print('@4'*10 + " h_pool1 shape after max_pool " + '@4'*10)
                # print(h_pool1)


                n_rows_temp = np.prod(h_pool1.shape.as_list()[1: ]) # 9600 for 3 currencies.
                # print(tf.size(h_pool1), type(tf.size(h_pool1)))
                # print(n_rows_temp, type(n_rows_temp))
                # W_fc1 = self.weight_variable([3 * 3200, 100])
                # W_fc1 = self.weight_variable([self.n_currency_pairs * 3200, 100])

                W_fc1 = self.weight_variable([n_rows_temp, 100])
                # print('@5'*10 + " W_fc1 shape " + '@5'*10)
                # print(W_fc1)

                b_fc1 = self.bias_variable([100])
                # print('@6'*10 + " b_fc1 shape " + '@6'*10)
                # print(b_fc1)


                # h_pool1_flat = tf.reshape(h_pool1, [-1, 3 * 3200])
                # h_pool1_flat = tf.reshape(h_pool1, [-1, self.n_currency_pairs * 3200])
                h_pool1_flat = tf.reshape(h_pool1, [-1, n_rows_temp])
                # print('@7'*10 + " h_pool1_flat shape " + '@7'*10)
                # print(h_pool1_flat)

                h_fc1 = tf.nn.relu(tf.matmul(h_pool1_flat, W_fc1) + b_fc1)
                # print('@8'*10 + " h_fc1 shape " + '@8'*10)
                # print(h_fc1)


                # self.keep_prob = tf.placeholder(tf.float32)
                # h_fc1_drop = tf.nn.dropout(h_fc1, self.keep_prob)
            with tf.variable_scope('l2'):
                W_fc2 = self.weight_variable([100, self.n_actions])
                b_fc2 = self.bias_variable([self.n_actions])

                self.q_eval=tf.nn.softmax(tf.matmul(h_fc1, W_fc2) + b_fc2)

        with tf.variable_scope('loss'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))
        with tf.variable_scope('train'):
            self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)


        # ------------------ build target_net ------------------
        self.x_ = tf.placeholder(tf.float32, [None, self.n_features * self.n_currency_pairs], name = 's_' )
        self.s_ = tf.reshape(self.x_, [-1, self.n_currency_pairs, self.n_features, 1])

        with tf.variable_scope('target_net'):
            c_names = ['target_net_params', tf.GraphKeys.GLOBAL_VARIABLES]
            with tf.variable_scope('l1'):

                W_conv1 = self.weight_variable([3, 3, 1, 32])
                b_conv1 = self.bias_variable([32])

                h_conv1 = tf.nn.relu(self.conv2d(self.s, W_conv1) + b_conv1)
                h_pool1 = self.max_pool_pairs_x_timestamps(h_conv1, 2, 2)
                n_rows_temp = np.prod(h_pool1.shape.as_list()[1: ])
                W_fc1 = self.weight_variable([n_rows_temp, 100])
                b_fc1 = self.bias_variable([100])
                h_pool1_flat = tf.reshape(h_pool1, [-1, n_rows_temp])
                h_fc1 = tf.nn.relu(tf.matmul(h_pool1_flat, W_fc1) + b_fc1)

            with tf.variable_scope('l2'):
                W_fc2 = self.weight_variable([100, self.n_actions])
                b_fc2 = self.bias_variable([self.n_actions])

                self.q_next=tf.nn.softmax(tf.matmul(h_fc1, W_fc2) + b_fc2)

    def store_transition(self, s, a, r, s_):
        if not hasattr(self, 'memory_counter'):
            self.memory_counter = 0

        transition = np.hstack((s, [a, r], s_))

        index = self.memory_counter % self.memory_size
        self.memory[index, :] = transition
        self.memory_counter += 1

    def choose_action(self, observation):
        observation = observation[np.newaxis, :]
        if np.random.uniform() < self.epsilon:
            # forward feed the observation and get q value for every actions
            actions_value = self.sess.run(self.q_eval, feed_dict={self.x: observation})
            action = np.argmax(actions_value)
        else:
            action = np.random.randint(0, self.n_actions)
        return action

    def learn(self):
        # check to replace target parameters
        if self.learn_step_counter % self.replace_target_iter == 0:
            self.sess.run(self.replace_target_op)
            print('\ntarget_params_replaced\n')

        # sample batch memory from all memory
        if self.memory_counter > self.memory_size:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_counter, size=self.batch_size)
        batch_memory = self.memory[sample_index, :]

        temp_s_ = batch_memory[: , -self.n_features * self.n_currency_pairs :]
        feed_s_ = np.array(temp_s_).reshape(-1, self.n_currency_pairs, self.n_features, 1)
        temp_s = batch_memory[: , : self.n_features * self.n_currency_pairs]
        feed_s = np.array(temp_s).reshape(-1, self.n_currency_pairs, self.n_features, 1)

        q_next, q_eval = self.sess.run([self.q_next, self.q_eval], feed_dict={
                self.s_: feed_s_,  # fixed params
                self.s: feed_s,  # newest params
            })

        q_target = q_eval.copy()
        batch_index = np.arange(self.batch_size, dtype=np.int32)
        eval_act_index = batch_memory[:, self.n_features * self.n_currency_pairs].astype(int)
        reward = batch_memory[: , self.n_features * self.n_currency_pairs + 1]
        q_target[batch_index, eval_act_index] = reward + self.gamma * np.max(q_next, axis=1)

        # print('batch_memory.shape {}'.format(batch_memory.shape))
        #ValueError: operands could not be broadcast together with shapes (32,) (3200,)
        # q_target.shape: (32, 7)
        # batch_memory.shape: (32, 3602) four currencies. (32, 1802) three currencies.

        _, self.cost = self.sess.run([self._train_op, self.loss], feed_dict={self.s: feed_s, self.q_target: q_target})
        self.cost_his.append(self.cost)

        self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
        self.learn_step_counter += 1

    def plot_cost(self):
        import matplotlib.pyplot as plt
        # print('COST LOG: ')
        # print(self.cost_his)
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()
