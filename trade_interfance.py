import time
import datetime
import pandas as pd
import numpy as np

import sys
import os.path
import re
import json

import oanda_interface as OI



###############################################################################


my_account_id = '101-001-11707432-001'
my_access_token = 'a10a1538b3fdaf3a8a2f3b9a496a3aeb-00a7b8f54791fb3132b22ca77419cc58'
csv_dir = './test_data/'


###############################################################################



class TI_Account_Exception(Exception):
    pass

class TI_Market_LUT_Exception(Exception):
    pass

class TI_Execution_Exception(Exception):
    pass


class Trade_Interface:
    def __init__(self, _account_name, _currency_balance, _from_time, _to_time, _request_interval, _arena_folder = None):
        self.account_name = _account_name
        self.currency_balance = _currency_balance
        self.from_time = _from_time
        self.to_time = _to_time
        self.request_interval = _request_interval
        currency_pairs = ['USD_JPY', 'GBP_JPY', 'GBP_USD']
        self.areana = self.get_arena(currency_pairs)

        self.action_id_counter = 0
        self.trade_log = []

    # def get_currency_pairs(self, mode=None, currency_A=None, currency_B=None):
    def get_currency_pairs(self, currency_A, currency_B):
        all_pairs = ['USD_JPY', 'GBP_JPY', 'GBP_USD']
        # if mode == 'ALL':
        #     print('there')
        #     return all_pairs
        #Exception2Handle: do not have C(len(currency_balance), 2) sets of data.
        #Progess2Handle: return currency_pairs from `k in self.currenct_balance`.
        # if currency_A != None and currency_B != None:
        #     print("here")

        if currency_A + '_' + currency_B in all_pairs:
            return [currency_A + '_' + currency_B, True]
        else:
            return [currency_B + '_' + currency_A, False]

    def get_arena(self, currency_pairs):
        close_price_only_flag = True

        currency_ORs = []
        for i in currency_pairs:
            OI_temp = OI.Oanda_Interface(my_account_id, my_access_token)
            OR_temp = OI_temp.get_history_price(self.from_time, self.to_time, self.request_interval, i, close_price_only_flag)
            currency_ORs.append(OR_temp)

        arena_df = pd.concat((i.record_df.set_index('time') for i in currency_ORs), axis=1, join='outer', sort=True).reset_index()
        arena_df = arena_df.rename(index=str, columns={'index': 'time'})

        currency_list = [k for k in self.currency_balance]
        arena_filename = './arena_data/' + '_'.join(currency_list) + '_' + _from[0:19] + '_' + _to[0:19] + '_' + self.request_interval + '.csv'
        arena_df.to_csv(arena_filename, index = None, header = True)


        OR_arena = OI.Onada_Record(arena_df, arena_filename, self.from_time, self.to_time, self.request_interval, currency_list)
        print("\n\nThe requested ARENA record has been successfully exported.")
        return OR_arena


    def market_LUT(self, _time):
        df = self.areana.record_df
        target_df = df.loc[df['time'] == _time]
        if target_df.empty:
            #Exception2Handle: invalid timeframe.
            print("no target found")
            return 2
        else:
            # print(target_df.head())
            return target_df

    def execute_trade(self, _time, _sell_currency, _buy_currency, _trade_unit, _trade_unit_in_buy_currenct = True):
        #Progess2Handle: _trade_unit_in_buy_currenct = False.
        #Exception2Handle: _sell_currency, _buy_currency not in arena.

        currency_pair, pair_flag = self.get_currency_pairs(_sell_currency, _buy_currency)

##########################BUG###################################################
        col = currency_pair+'_close'
        print(self.market_LUT(_time))
        print(type(self.market_LUT(_time)))
        print(currency_pair)
        print(col)

        price = self.market_LUT(_time).loc(axis=0)[:, col]
        # print("price is {}.".format(price))
        #Exception2Handle: market_LUT return NaN.

##########################BUG###################################################

        if pair_flag == True:
            self.currency_balance['_sell_currency'] -= _trade_unit / price
            self.currency_balance['_buy_currency'] += _trade_unit
        else:
            self.currency_balance['_sell_currency'] -= _trade_unit * price
            self.currency_balance['_buy_currency'] += _trade_unit





        val_list = [self.action_id_counter, _time, _sell_currency, _buy_currency, _trade_unit, price, pair_flag, self.self.currency_balance['_sell_currency'], self.currency_balance['_buy_currency']]
        key_list = ["action_id", "trade_time", "sell_currency", "buy_currency", "trade_unit", "trade_price", "pair_flag", "sell_currency_balance", "buy_currency_balance"]
        new_trade_action = dict(zip(key_list, val_list))
        # print(json.dumps(new_trade_action, indent=4))
        self.trade_log.append(new_trade_action)

        #Exception2Handle: _time earlier than pervious action in log.
        self.action_id_counter += 1

    #Performance2Handle: do with decorator.
    def trade_log_review(self):
        # print(json.dumps(self.trade_log, indent=4))
        for i in self.trade_log:
            for k, v in dict.items(i):
                print("\t\t\t{:25}{}".format(k+':', v))
            print("\n")

    def account_review(self):
        df = self.areana.record_df
        record_from = df.iloc[0, 0]
        record_to = df.iloc[df.shape[0]-1, 0]
        print("\nCurrenct acount is {}.\n\t{:30}{}\n\t{:30}{}\n\t{:30}{}\n\n".format(self.account_name, 'record_from: ', record_from, 'record_to: ', record_to, 'trade_log_len: ', len(self.trade_log)))
        print(json.dumps(self.currency_balance, indent=4))

###############################################################################





_account_name = 'dev_arena_test'
_currency_balance = {'USD': 50000, 'JPY': 50000, 'GBP': 50000}
_from = "2019-01-01T00:00:00Z"
_to = "2019-01-02T00:00:00Z"
_interval = "M1"

TI_test = Trade_Interface(_account_name, _currency_balance, _from, _to, _interval)
# TI_test.areana.record_df
TI_test.areana.record_review()


# 2019-01-01T22:30:00.000000000Z,109.646,14.0,139.736,145.0,1.27442,21.0
# 2019-01-01T22:41:00.000000000Z,109.668,4.0,139.776,20.0,1.27450,12.0
# 2019-01-01T22:55:00.000000000Z,109.684,1.0,139.780,202.0,1.27416,2.0
# 2019-01-01T22:59:00.000000000Z,109.684,5.0,139.776,38.0,1.27398,15.0
# 2019-01-01T23:02:00.000000000Z,109.658,7.0,139.859,7.0,1.27513,3.0
# 2019-01-01T23:05:00.000000000Z,109.688,10.0,139.863,19.0,1.27509,2.0

time_1 = '2019-01-01T22:30:00.000000000Z'
time_2 = '2019-01-01T22:41:00.000000000Z'
time_3 = '2019-01-01T22:55:00.000000000Z'
time_4 = '2019-01-01T22:59:00.000000000Z'
time_5 = '2019-01-01T23:02:00.000000000Z'
time_6 = '2019-01-01T23:05:00.000000000Z'

TI_test.execute_trade(time_1, 'USD', 'GBP', 10)
TI_test.execute_trade(time_2, 'GBP', 'USD', 20)
TI_test.execute_trade(time_3, 'GBP', 'JPY', 30)
TI_test.execute_trade(time_4, 'JPY', 'GBP', 40)
TI_test.execute_trade(time_5, 'JPY', 'USD', 50)
TI_test.execute_trade(time_5, 'USD', 'JPY', 60)


TI_test.trade_log_review()
TI_test.account_review()


