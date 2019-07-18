import time
import datetime
import pandas as pd
import numpy as np

import os.path
import re
import json

class Trade_Action:
    def __init__(self, _time, _currency_pair, _volume):
        self.time = _time
        self.currency_pair = _currency_pair
        self.volume = _volume


class Trade_Interface:
    def __init__(self, _account_name, _record, _currency_pair, _currency_A_balance, _currency_B_balance):
        self.account_name = _account_name

        self.currency_A_balance = _currency_A_balance
        self.currency_B_balance = _currency_B_balance

        if isinstance(_record, str) and os.path.isfile(_record):
            df = pd.read_csv(_record)
        elif isinstance(_record, pd.DataFrame):
            df = _record
        else:
            print("Invalid _record input: must be DataFrame or csv file path.")
            return 1
        self.record = df

        currency_pair = _currency_pair.split('_')
        self.currency_A, self.currency_B = currency_pair
        self.action_id_counter = 0
        self.trade_log = []


    def market_LUT(self, _time):
        df = self.record
        target_df = df.loc[df['time'] == _time]
        if target_df.empty:
            print("no target found")
            return 2
        else:
            # print(target_df.head())
            return target_df

    def execute_long(self, _time, _trade_unit):
        price = self.market_LUT(_time).iloc[0, 4]
        # print("price is {}.".format(price))
        self.currency_A_balance += _trade_unit
        self.currency_B_balance -= _trade_unit * price
        val_list = [self.action_id_counter, _time, 'long', price, self.currency_A, _trade_unit, self.currency_A_balance, self.currency_B_balance]
        key_list = ["action_id", "trade_time", "trade_type", "trade_price", "trade_currency", "trade_unit", "currency_A_balance", "currency_B_balance"]
        new_trade_action = dict(zip(key_list, val_list))
        # print(json.dumps(new_trade_action, indent=4))
        self.trade_log.append(new_trade_action)
        self.action_id_counter += 1

    def execute_short(self, _time, _trade_unit):
        # price = pd.to_numeric(self.market_LUT(_time)['close_price'])
        price = self.market_LUT(_time).iloc[0, 4]
        # print("price is {}.".format(price))
        self.currency_A_balance -= _trade_unit / price
        self.currency_B_balance += _trade_unit
        val_list = [self.action_id_counter, _time, 'short', price, self.currency_B, _trade_unit, self.currency_A_balance, self.currency_B_balance]
        key_list = ["action_id", "trade_time", "trade_type", "trade_price", "trade_currency", "trade_unit", "currency_A_balance", "currency_B_balance"]
        new_trade_action = dict(zip(key_list, val_list))
        # print(json.dumps(new_trade_action, indent=4))
        self.trade_log.append(new_trade_action)
        self.action_id_counter += 1

    def account_review(self):
        df = self.record
        record_from = df.iloc[0, 0]
        record_to = df.iloc[df.shape[0]-1, 0]
        print("\nAccount {} is built.\n\t{:30}{}\n\t{:30}{}\n\t{:30}{}\n\t{:30}{}\n\t{:30}{}\n\t{:30}{}\n\t{:30}{}\n\n".format(self.account_name, 'currency_A: ', self.currency_A, 'currency_B: ', self.currency_B, 'record_from: ', record_from, 'record_to: ', record_to, 'currency_A_balance: ', self.currency_A_balance, 'currency_B_balance: ', self.currency_B_balance, 'trade_log_len: ', len(self.trade_log)))

    def trade_log_review(self):
        # print(json.dumps(self.trade_log, indent=4))
        for i in self.trade_log:
            for k, v in dict.items(i):
                print("\t\t\t{:25}{}".format(k+':', v))
            print("\n")

_account_name = 'dev_test'
_record = 'dummy_data/USD_JPY_2018-01-01T00:00:00_2018-06-30T23:59:59_M1.csv'
_currency_pair = 'USD_JPY'
_currency_A_balance = 10000
_currency_B_balance = 10000

_time_1 = '2018-01-01T22:02:00.000000000Z'
#2018-01-01T22:02:00.000000000Z,112.676,112.676,112.676,112.676,True,2
_time_2 = '2018-01-01T22:21:00.000000000Z'
#2018-01-01T22:21:00.000000000Z,112.641,112.641,112.636,112.636,True,2
_time_3 = '2018-01-01T23:05:00.000000000Z'
#2018-01-01T23:05:00.000000000Z,112.674,112.677,112.657,112.672,True,47
_time_4 = '2018-01-02T00:16:00.000000000Z'
#2018-01-02T00:16:00.000000000Z,112.742,112.742,112.742,112.742,True,1

TI = Trade_Interface(_account_name, _record, _currency_pair, _currency_A_balance, _currency_B_balance)
TI.account_review()

TI.execute_short(_time_1, 2000)
TI.execute_short(_time_2, 5000)
TI.execute_long(_time_3, 20)
TI.execute_long(_time_4, 30)
TI.trade_log_review()
TI.account_review()

