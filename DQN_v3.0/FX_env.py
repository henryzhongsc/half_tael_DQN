import pandas as pd
import numpy as np
import time
import sys
import copy

# from os.path import dirname, abspath
# file_parent_dir = dirname(dirname(abspath(__file__)))

sys.path.append('.')
import trade_interface as TI


class FX:

    def __init__(self, _TI_account, _base_currency = 'USD', _n_features = 300):
        #super(Maze, self).__init__()
        self.action_space = ['hold','buy_100_A','sell_100_A','buy_100_B','sell_100_B','buy_100_C','sell_100_C']
        # self.action_space = ['hold','buy_100','sell_100','buy_200','sell_200','buy_300','sell_300']
        self.n_actions = len(self.action_space)
        self.n_features = _n_features # each time, we consider 300 days historical records
        self.step_count = 0
        self.base_currency = _base_currency


        # self.start_day = 300

        self.obs = []
        self.data_env = []

        self.TI_train = copy.deepcopy(_TI_account)
        self.TI_initial = copy.deepcopy(_TI_account)


        df = self.TI_initial.arena.record_df
        left_over_row = df.shape[0] % self.n_features
        self.max_usable_row = df.shape[0] - left_over_row


        # self.data_env = list(df[trade_on].iloc[0 : (self.max_usable_row - 1)])



        # for i, j in zip(self.TI_initial.currency_pairs, [i for i in range(len(self.TI_initial.currency_pairs) + 1)]:
        #     df_one_pair = list(df[i+'_close'].iloc[0: (self.max_usable_row - 1)])
        #     df_one_pair = np.asarray(df_one_pair[0 : (self.max_usable_row - 1)]).reshape((j, (self.max_usable_row - 1)))

        self.data_env = np.empty((0, self.max_usable_row))
        for i in self.TI_initial.currency_pairs:
            price_list_one_pair = list(df[i+'_close'].iloc[0: self.max_usable_row])
            temp_array = np.asarray(price_list_one_pair).reshape(1, len(price_list_one_pair))
            self.data_env = np.vstack((self.data_env, temp_array))

        self.data_time = list(df['time'].iloc[0 : (self.max_usable_row)])
        self.obs_time = []

        self.reset()



    def reset(self): #GRAPHEN

        self.step_count = 0
        self.start_day = self.n_features
        self.obs = self.data_env[:, 0 : self.start_day].reshape((len(self.TI_train.currency_pairs) * self.start_day,))
        self.obs_time = self.data_time[0 : self.start_day]

        del self.TI_train
        self.TI_train = copy.deepcopy(self.TI_initial)

        return np.asarray(self.obs), self.TI_train, self.data_time[0] #输出是一个 1D array



    def step(self, action, print_step = False):
        current_time = self.obs_time[-1]

        c_list = self.TI_train.all_currency_list
        c_list.remove(self.base_currency)
        c_list.insert(0, self.base_currency)

        # ['hold','buy_100_A','sell_100_A','buy_100_B','sell_100_B','buy_100_C','sell_100_C']
        if action == 0:
            pass
        elif action == 1:
            self.TI_train.execute_trade(current_time, c_list[0], c_list[1], 100, _trade_unit_in_buy_currency = False)
        elif action == 2:
            self.TI_train.execute_trade(current_time, c_list[1], c_list[0], 100)
        elif action == 3:
            self.TI_train.execute_trade(current_time, c_list[0], c_list[2], 100, _trade_unit_in_buy_currency = False)
        elif action == 4:
            self.TI_train.execute_trade(current_time, c_list[2], c_list[0], 100)
        elif action == 5:
            self.TI_train.execute_trade(current_time, c_list[1], c_list[2], 100, _trade_unit_in_buy_currency = False)
        elif action == 6:
            self.TI_train.execute_trade(current_time, c_list[2], c_list[1], 100)
        else:
            print("Invalid action input = {}".format(action))
            return -1
        self.step_count += 1


        if self.step_count < self.max_usable_row - self.n_features:
            if print_step == True:
                print('Step: {}'.format(self.step_count))

            self.obs = self.data_env[:, self.step_count : (self.start_day + self.step_count)].reshape((len(self.TI_train.currency_pairs) * self.start_day,))
            self.obs_time = self.data_time[self.step_count : (self.start_day + self.step_count)]

        elif self.step_count == self.max_usable_row - self.n_features:
            self.obs = self.data_env[:, (self.max_usable_row - self.n_features) : ].reshape((len(self.TI_train.currency_pairs) * self.start_day,))
            self.obs_time = self.data_time[(self.max_usable_row - self.n_features) : ]


        # # 更新 observation 的状态
        # if self.step_count < 4500:
        #     #self.obs = self.data_env[(0 + self.step_count):(self.start_day + self.step_count)]
        #
        #     self.obs = self.data_env[:,(0+self.step_count):(self.start_day + self.step_count)].reshape((600,))
        #     #self.obs =np.concatenate(np.asarray(self.data_env[(0+self.step_count):(self.start_day + self.step_count)]),
        #     #                         np.asarray(self.data_env[(0+self.step_count):(self.start_day + self.step_count)]))
        #     #print(self.obs.shape)
        # elif self.step_count == 4500:
        #
        #
        #     temp_obs = self.data_env[:,(0+self.step_count):(self.start_day + self.step_count)]
        #     #self.obs = self.obs =np.concatenate(np.asarray(self.data_env[(0+self.step_count):(self.start_day + self.step_count)]),
        #     #                                    np.asarray(self.data_env[(0+self.step_count):(self.start_day + self.step_count)]))
        #     print('^')
        #     print(temp_obs.shape)
        #     print(self.data_env[:, -1])
        #     print(self.data_env[: , -1].shape)
        #     temp_obs = np.append(temp_obs, self.data_env[:, -1])
        #     # temp_obs = np.append(temp_obs, self.data_env[-1])
        #     print('*')
        #     print(len(temp_obs))
        #     print(temp_obs.shape)
        #     temp_obs.reshape((600,))
        #     self.obs = temp_obs
            #print
            #print(self.obs)

        # reward function
        initial_checkout_balance = self.TI_initial.currency_balance[self.base_currency]
        TI_checkout = copy.deepcopy(self.TI_train)
        TI_checkout.checkout_all_in(current_time, self.base_currency)
        current_checkout_balance = TI_checkout.currency_balance[self.base_currency]

        if (current_checkout_balance > initial_checkout_balance) & (self.step_count == self.max_usable_row - self.n_features):
            reward = 1
            done = True
        elif (current_checkout_balance <= initial_checkout_balance)  & (self.step_count == self.max_usable_row - self.n_features):
            reward = -1
            done = True
        else:
            reward = 0
            done = False


        s_ = np.asarray(self.obs)

        return s_, reward, done, self.TI_train, self.data_time[-1]

