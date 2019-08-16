"""
This part of code is the DQN brain, which is a brain of the agent.
All decisions are made in here.
Using Tensorflow to build the neural network.
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
Using:
Tensorflow: 1.0
gym: 0.7.3
"""

import numpy as np
import pandas as pd
import tensorflow as tf

np.random.seed(1)
tf.set_random_seed(1)


# Deep Q Network off-policy
class DeepQNetwork:
    def __init__(
            self,
            n_actions,
            n_features,
            learning_rate=0.01,
            reward_decay=0.9,
            e_greedy=0.9,
            replace_target_iter=300,
            memory_size=800,
            batch_size=32,
            e_greedy_increment=None,
            output_graph=False,
    ):
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

        # total learning step
        self.learn_step_counter = 0

        # initialize zero memory [s, a, r, s_]
        self.memory = np.zeros((self.memory_size, n_features * 4 + 2))
        # print("@"*30)
        # print(len(self.memory))
        # print("@"*30)
        # consist of [target_net, evaluate_net]
        print('before build net')
        self._build_net()
        print('after build net')
        t_params = tf.get_collection('target_net_params')
        e_params = tf.get_collection('eval_net_params')
        self.replace_target_op = [tf.assign(t, e) for t, e in zip(t_params, e_params)]

        self.sess = tf.Session()

        if output_graph:
            # $ tensorboard --logdir=logs
            # tf.train.SummaryWriter soon be deprecated, use following
            tf.summary.FileWriter("logs/", self.sess.graph)

        self.sess.run(tf.global_variables_initializer())
        self.cost_his = []

    # we will define functions for tensorflow use # ######################################################
    # these are private methods                   # ######################################################
    ######################################################################################################

    def weight_variable(self, shape):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)

    def bias_variable(self,shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    def conv2d(self,x, W):

        temp = tf.nn.conv2d(x, W, strides=[1, 2, 25, 1], padding='SAME')

        print('CONV2d !#!'*20)
        print(x, W, temp)
        print('CONV2d !#!'*20)

        return temp

    def max_pool_2x2(self,x):
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],     # 纵2 横25
                              strides=[1, 2, 2, 1], padding='SAME')





    def _build_net(self):

        print('in build net')
        # ------------------ build evaluate_net ------------------
        #self.s = tf.placeholder(tf.float32, [None, self.n_features], name='s')  # input
        #tf.placeholder(tf.float32, [None, 784]) # [-1,2,self.n_features,1]
        self.x = tf.placeholder(tf.float32, [None, 600])
        self.s = tf.reshape(self.x, [-1,2,300,1])
        W = tf.Variable(tf.zeros([self.n_features*2,7]))
        b = tf.Variable(tf.zeros([7]))

        self.q_target = tf.placeholder(tf.float32, [None, 7], name='Q_target')  # for calculating loss

        #########################################################
        with tf.variable_scope('eval_net'):
            c_names = ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES]

            with tf.variable_scope('l1'):
                W_conv1 = self.weight_variable([6, 6, 1, 32])
                b_conv1 = self.bias_variable([32])

                h_conv1 = tf.nn.relu(self.conv2d(self.s, W_conv1) + b_conv1)
                h_pool1 = self.max_pool_2x2(h_conv1)

                W_fc1 = self.weight_variable([6 * 32, 100])  # 这一行要改，用colab 打印 输入 来协助完成
                b_fc1 = self.bias_variable([100])                # 这一行要改，用colab 打印 输入 来协助完成

                h_pool1_flat = tf.reshape(h_pool1, [-1, 6*32])
                h_fc1 = tf.nn.relu(tf.matmul(h_pool1_flat, W_fc1) + b_fc1)


                # self.keep_prob = tf.placeholder(tf.float32)
                # h_fc1_drop = tf.nn.dropout(h_fc1, self.keep_prob)
            with tf.variable_scope('l2'):
                W_fc2 = self.weight_variable([100, 7]) # 可以把10 改成 7，也就是 action_space
                b_fc2 = self.bias_variable([7])         # 可以把10 改成 7，也就是 action_space

                self.q_eval=tf.nn.softmax(tf.matmul(h_fc1, W_fc2) + b_fc2)
                # print("### q_eval shape: {} ###".format(self.q_eval))

        with tf.variable_scope('loss'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))
        with tf.variable_scope('train'):
            self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)


        # ------------------ build target_net ------------------

        self.x_ = tf.placeholder(tf.float32, [None, 600],name = 's_' )
        self.s_ = tf.reshape(self.x_, [-1,2,300,1])

        #self.s_ = tf.placeholder(tf.float32, [-1,2,self.n_features,1],name = 's_' )    # input
        with tf.variable_scope('target_net'):
            # c_names(collections_names) are the collections to store variables
            c_names = ['target_net_params', tf.GraphKeys.GLOBAL_VARIABLES]
            # first layer. collections is used later when assign to target net
            with tf.variable_scope('l1'):
                W_conv1 = self.weight_variable([6, 6, 1, 32])
                b_conv1 = self.bias_variable([32])

                h_conv1 = tf.nn.relu(self.conv2d(self.s_, W_conv1) + b_conv1)
                h_pool1 = self.max_pool_2x2(h_conv1)

                W_fc1 = self.weight_variable([ 6 * 32, 100])  # 这一行要改，用colab 打印 输入 来协助完成
                b_fc1 = self.bias_variable([100])                # 这一行要改，用colab 打印 输入 来协助完成

                h_pool1_flat = tf.reshape(h_pool1, [-1, 6*32])
                h_fc1 = tf.nn.relu(tf.matmul(h_pool1_flat, W_fc1) + b_fc1)


                # self.keep_prob = tf.placeholder(tf.float32)
                # h_fc1_drop = tf.nn.dropout(h_fc1, self.keep_prob)
            with tf.variable_scope('l2'):
                W_fc2 = self.weight_variable([100, 7]) # 可以把10 改成 7，也就是 action_space
                b_fc2 = self.bias_variable([7])         # 可以把10 改成 7，也就是 action_space

                self.q_next=tf.nn.softmax(tf.matmul(h_fc1, W_fc2) + b_fc2)

            print('out build net')


    def store_transition(self, s, a, r, s_):
        if not hasattr(self, 'memory_counter'):
            self.memory_counter = 0

        transition = np.hstack((s, [a, r], s_))
        print('TRANS $'*20)
        print(transition[0:10])
        print(transition[-10:])
        print('TRANS $'*20)
        # print("#"*20)
        # print(len(s))
        # print(len([a,r]))
        # print(len(s_))
        # print(transition)
        # print(type(transition))
        # print(len(transition))

        # replace the old memory with new memory
        index = self.memory_counter % self.memory_size

        # print(self.memory_counter, self.memory_size, index)
        # print(len(self.memory[index, :]))
        #
        # print("#"*21)
        # print(self.memory)
        # print(len(self.memory))
        # print(index)

        self.memory[index, :] = transition


        self.memory_counter += 1

    def choose_action(self, observation):
        # to have batch dimension when feed into tf placeholder

        #print("###############################################")
        #print(type(observation))
        #print("###############################################")
        #print(observation.shape)
        #print(observation)
        observation = observation[np.newaxis, :]

        #print('after: ','observation = observation[np.newaxis, :]')
        #print(observation.shape)
        #print(observation)
        #此处新增修改
        #observation = np.array([observation])

        #print(observation)
        #print(observation.shape)

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

        print('SELF.S &'*20)
        print(self.s)
        # print(self.s.shape)
        # print(batch_memory[:, :self.n_features*2])
        # print(batch_memory[:, :self.n_features*2].shape)


        temp_s_ = batch_memory[:, -self.n_features*2:]
        # temp_s_ = batch_memory[:, -self.n_features:]
        feed_s_ = np.array(temp_s_).reshape(-1,2,300,1)

        temp_s = batch_memory[:, :self.n_features*2]
        # temp_s = batch_memory[:, :self.n_features]
        feed_s = np.array(temp_s).reshape(-1,2,300,1)


        q_next = self.sess.run(self.q_next, feed_dict={
                self.s_: feed_s_,  # fixed params
                self.s: feed_s,  # newest params
            })

        # print('@'*30)

        q_eval = self.sess.run(self.q_eval, feed_dict={
                self.s_: feed_s_,  # fixed params
                self.s: feed_s,  # newest params
            })
        print("self.s_: ",self.s_)
        print("self.s: ",self.s)

        print('SELF.S &'*20)

        # change q_target w.r.t q_eval's action
        q_target = q_eval.copy()

        batch_index = np.arange(self.batch_size, dtype=np.int32)
        eval_act_index = batch_memory[:, self.n_features].astype(int)
        reward = batch_memory[:, self.n_features + 1]

        print("TEMP^FEED "*20)

        print("\n\n\n temp_s_: {}\n temp_s_.shape: {}".format(temp_s_, temp_s_.shape))
        print("\n\n\n feed_s_: {}\n feed_s_.shape: {}".format(feed_s_, feed_s_.shape))
        print("\n\n\n temp_s: {}\n temp_s.shape: {}".format(temp_s, temp_s.shape))
        print("\n\n\n feed_s: {}\n feed_s.shape: {}".format(feed_s, feed_s.shape))

        print("TEMP^FEED "*20)

        print("REWARD^ "*20)
        print("batch_index: {} ({})\neval_act_index: {} ({})\n\n\nq_target[batch_index, eval_act_index]: {}\nq_target[b, e].shape: {}\n\n\nq_target: {}\nq_target.shape: {}".format(batch_index, len(batch_index), eval_act_index, len(eval_act_index), q_target[batch_index, eval_act_index], q_target[batch_index, eval_act_index].shape, q_target, q_target.shape))



        print("\n\n\nreward: {}\nreward.shape: {}".format(reward, reward.shape))
        print("\n\n\nnp.max(q_next): {}\nnp.max(q_next).shape: {}".format(np.max(q_next, axis=1), (np.max(q_next, axis=1).shape)))
        print("\n\n\nq_target: {}\nq_target.shape: {}".format(q_target, q_target.shape))
        print("\n\n\nq_next: {}\nq_next.shape: {}".format(q_next, q_next.shape))

        q_target[batch_index, eval_act_index] = reward + self.gamma * np.max(q_next, axis=1)

        # print(q_target[batch_index, eval_act_index])

        print("REWARD^ "*20)

        # train eval network
        _, self.cost = self.sess.run([self._train_op, self.loss],
                                     feed_dict={self.s: feed_s,
                                                self.q_target: q_target})
        self.cost_his.append(self.cost)

        # increasing epsilon
        self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
        self.learn_step_counter += 1

    def plot_cost(self):
        import matplotlib.pyplot as plt
        print("COST^!^ "*20)
        print(self.cost_his)
        print("COST^!^ "*20)
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()
