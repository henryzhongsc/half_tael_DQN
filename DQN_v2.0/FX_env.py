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
    def __init__(self, TI_account, n_features = 300):
        #super(Maze, self).__init__()
        self.action_space = ['hold','buy_100','sell_100','buy_200','sell_200','buy_300','sell_300']
        self.n_actions = len(self.action_space)
        self.n_features = n_features # each time, we consider 300 days historical records
        self.step_count = 0


        self.obs = []
        self.data_env = []

        # 零假空 初始化 环境变量
        self.TI_train = TI_account
        self.TI_initial = copy.deepcopy(TI_account)

        df = self.TI_initial.arena.record_df
        left_over_row = df.shape[0] % self.n_features
        self.max_usable_row = df.shape[0] - left_over_row
        self.data_env = list(df['EUR_GBP_close'].iloc[0 : (self.max_usable_row - 1)])
        self.data_time = list(df['time'].iloc[0 : (self.max_usable_row - 1)])
        self.obs_time = []

        self.reset()


    def reset(self):
            time.sleep(0.1)

            self.start_day = self.n_features # each time we  trade, our state is 300 historical price
            self.obs = self.data_env[0 : self.start_day]
            self.obs_time = self.data_time[0 : self.start_day]
            self.step_count = 0

            self.TI_train = copy.deepcopy(self.TI_initial)

            return np.asarray(self.obs) #输出是一个 1D array

    def step(self, action):
        current_time = self.obs_time[-1]

        c_1 = 'EUR'
        c_2 = 'GBP'

        # Exception2Handle: BALANCE NOT ENOUGH handle, may consider remove the catch phrase code of TI_Execution_Error and let it pass to this script to handle.
        try:
            self.execute_action(action)
        except balance_not_enough_error as e:
            sys.exit("During execute_action()\n\t{} is raised due to: {}".format(type(e), e))
        finally:
            self.execute_action(0)




        # 更新 observation 的状态
        if self.step_count < self.max_usable_row - self.n_features:
            self.obs = self.data_env[self.step_count : (self.start_day + self.step_count)]
            self.obs_time = self.data_time[self.step_count : (self.start_day + self.step_count)]
        elif self.step_count == self.max_usable_row - self.n_features:
            self.obs = self.data_env[self.step_count : ]
            self.obs_time = self.data_time[self.step_count : ]

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

        print("Done = {}, {} = {}, {} = {}, step_count = {}".format(done, c_1, self.TI_train.currency_balance[c_1], c_2, self.TI_train.currency_balance[c_2], self.step_count))

        s_ = np.asarray(self.obs)
        return s_, reward, done

    def execute_action(self, action):
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