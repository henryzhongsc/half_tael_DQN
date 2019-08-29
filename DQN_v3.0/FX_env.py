import pandas as pd
import numpy as np
import time
import sys
import copy

# from os.path import dirname, abspath
# file_parent_dir = dirname(dirname(abspath(__file__)))

sys.path.append('.')
import trade_interface as TI
from anita.anita_interface import *
from anita.anita_interface import Anita_Trait as AT
from anita.anita_interface import Anita_Persona as AP



class FX:

    def __init__(self, _TI_account, _base_currency = 'USD', _n_features = 300, _anita_switch = False):
        self.anita_switch = _anita_switch

        self.action_space = ['hold','buy_100_A','sell_100_A','buy_100_B','sell_100_B','buy_100_C','sell_100_C']
        self.n_actions = len(self.action_space)
        self.n_features = _n_features
        self.step_count = 0
        self.base_currency = _base_currency

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
            # pass
            self.TI_train.execute_trade(current_time, c_list[0], c_list[1], 0)
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


        reward, done = self.eval_reward(current_time)

        s_ = np.asarray(self.obs)
        return s_, reward, done, self.TI_train, self.data_time[-1]


    def eval_reward(self, _current_time):
        initial_checkout_balance = self.TI_initial.currency_balance[self.base_currency]
        TI_checkout = copy.deepcopy(self.TI_train)
        TI_checkout.checkout_all_in(_current_time, self.base_currency)
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

        final_reward = reward
        if self.anita_switch == True and reward != 0:
            TI_AT = copy.deepcopy(self.TI_train)
            AT_reward = AT(TI_AT, self.n_features, self.n_actions)
            AP_reward = AP('Anita_placeholder_avatar', AT_reward)
            final_reward = reward + AP_reward.anita_reward
            print('$$ Final reward ({}) = DQN reward ({}) + Anita reward ({}) $$'.format(final_reward, reward, AP_reward.anita_reward))

        return final_reward, done



