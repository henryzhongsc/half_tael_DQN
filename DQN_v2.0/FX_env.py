import pandas as pd
import numpy as np
import time
import sys
import copy

from os.path import dirname, abspath
file_parent_dir = dirname(dirname(abspath(__file__)))

sys.path.append('.')
import trade_interface as TI


class FX:
    def __init__(self, TI_account, trade_on, base_currency = 'USD', n_features = 300):
        #super(Maze, self).__init__()
        self.action_space = ['hold','buy_100','sell_100','buy_200','sell_200','buy_300','sell_300']
        self.n_actions = len(self.action_space)
        self.n_features = n_features # each time, we consider 300 days historical records
        self.step_count = 0
        self.base_currency = base_currency


        self.obs = []
        self.data_env = []

        # 零假空 初始化 环境变量
        self.TI_train = copy.deepcopy(TI_account)
        self.TI_initial = copy.deepcopy(TI_account)

        df = self.TI_initial.arena.record_df
        left_over_row = df.shape[0] % self.n_features
        self.max_usable_row = df.shape[0] - left_over_row
        print("__init__ max_usable_row: {}".format(self.max_usable_row))
        self.data_env = list(df[trade_on].iloc[0 : (self.max_usable_row)])
        self.data_time = list(df['time'].iloc[0 : (self.max_usable_row)])
        self.obs_time = []

        print("__init__ len(data_env): {}, len(data_time): {}".format(len(self.data_env), len(self.data_time)))
        self.reset()
        print("__init__ reset len(data_env): {}, len(data_time): {}".format(len(self.data_env), len(self.data_time)))



    def reset(self):
            time.sleep(0.1)

            self.start_day = self.n_features # each time we  trade, our state is 300 historical price
            self.obs = self.data_env[0 : self.start_day]
            self.obs_time = self.data_time[0 : self.start_day]
            self.step_count = 0

            del self.TI_train
            self.TI_train = copy.deepcopy(self.TI_initial)

            return np.asarray(self.obs), self.TI_train, self.data_time[0] #输出是一个 1D array

    def step(self, action):
        current_time = self.obs_time[-1]

        c_1 = self.base_currency
        c_2 = 'GBP'


        if action == 0:
            pass
        elif action == 1:
            self.TI_train.execute_trade(current_time, c_1, c_2, 100, _trade_unit_in_buy_currency = False)
        elif action == 2:
            self.TI_train.execute_trade(current_time, c_2, c_1, 100)
        elif action == 3:
            self.TI_train.execute_trade(current_time, c_1, c_2, 100, _trade_unit_in_buy_currency = False)
        elif action == 4:
            self.TI_train.execute_trade(current_time, c_2, c_1, 200)
        elif action == 5:
            self.TI_train.execute_trade(current_time, c_1, c_2, 300, _trade_unit_in_buy_currency = False)
        elif action == 6:
            self.TI_train.execute_trade(current_time, c_2, c_1, 200)
        else:
            print("Invalid action input = {}".format(action))
            return -1
        self.step_count += 1




        # 更新 observation 的状态
        if self.step_count < self.max_usable_row - self.n_features:
            self.obs = self.data_env[self.step_count : (self.start_day + self.step_count)]
            self.obs_time = self.data_time[self.step_count : (self.start_day + self.step_count)]
        elif self.step_count == self.max_usable_row - self.n_features:

            # print("step_count: {}, start_date: {}, data_env[-1]: {}, data_time[-1]: {}, max_usable_row: {}".format(self.step_count, self.start_day, self.data_env[-1], self.data_time[-1], self.max_usable_row))

            self.obs = self.data_env[(self.max_usable_row - self.n_features) : ]
            self.obs_time = self.data_time[(self.max_usable_row - self.n_features) : ]

            # print("len(obs): {}, len(obs_time): {}".format(len(self.obs), len(self.obs_time)))
            # print("len(obs_fix): {}, len(obs_time_fix): {}".format(len(self.data_env[self.max_usable_row : ]), len(self.data_time[self.max_usable_row :])))
            # print("len(data_env): {}, len(data_time): {}".format(len(self.data_env), len(self.data_time)))


        # reward function
        initial_checkout_balance = self.TI_initial.currency_balance[c_1]
        TI_checkout = copy.deepcopy(self.TI_train)
        TI_checkout.checkout_all_in(current_time, c_1)
        # TI_checkout.account_review()
        current_checkout_balance = TI_checkout.currency_balance[c_1]



        if (current_checkout_balance > initial_checkout_balance) & (self.step_count == self.max_usable_row - self.n_features):
            reward = 1
            done = True
        elif (current_checkout_balance <= initial_checkout_balance)  & (self.step_count == self.max_usable_row - self.n_features):
            reward = -1
            done = True
        else:
            reward = 0
            done = False



        # print("Done = {}, {} = {}, {} = {}, step_count = {}".format(done, c_1, self.TI_train.currency_balance[c_1], c_2, self.TI_train.currency_balance[c_2], self.step_count))

        s_ = np.asarray(self.obs)
        return s_, reward, done, self.TI_train, self.data_time[-1]

