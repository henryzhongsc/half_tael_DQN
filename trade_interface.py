import time
import datetime
import pandas as pd
import numpy as np

import sys
import os.path
import re
import json

import oanda_interface as OI
from decimal import *
import itertools



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
        self.currency_pairs = self.get_currency_pairs([k for k in self.currency_balance])
        self.areana = self.get_arena(self.currency_pairs)

        self.action_id_counter = 0
        self.trade_log = []


    def get_currency_pairs(self, currency_list):
        all_available_pairs = ['AUD_CAD', 'AUD_CHF', 'AUD_HKD', 'AUD_JPY', 'AUD_NZD', 'AUD_SGD', 'AUD_USD', 'CAD_CHF', 'CAD_HKD', 'CAD_JPY', 'CAD_SGD', 'CHF_HKD', 'CHF_JPY', 'CHF_ZAR', 'EUR_AUD', 'EUR_CAD', 'EUR_CHF', 'EUR_CZK', 'EUR_DKK', 'EUR_GBP', 'EUR_HKD', 'EUR_HUF', 'EUR_JPY', 'EUR_NOK', 'EUR_NZD', 'EUR_PLN', 'EUR_SEK', 'EUR_SGD', 'EUR_TRY', 'EUR_USD', 'EUR_ZAR', 'GBP_AUD', 'GBP_CAD', 'GBP_CHF', 'GBP_HKD', 'GBP_JPY', 'GBP_NZD', 'GBP_PLN', 'GBP_SGD', 'GBP_USD', 'GBP_ZAR', 'HKD_JPY', 'NZD_CAD', 'NZD_CHF', 'NZD_HKD', 'NZD_JPY', 'NZD_SGD', 'NZD_USD', 'SGD_CHF', 'SGD_HKD', 'SGD_JPY', 'TRY_JPY', 'USD_CAD', 'USD_CHF', 'USD_CNH', 'USD_CZK', 'USD_DKK', 'USD_HKD', 'USD_HUF', 'USD_JPY', 'USD_MXN', 'USD_NOK', 'USD_PLN', 'USD_SAR', 'USD_SEK', 'USD_SGD', 'USD_THB', 'USD_TRY', 'USD_ZAR', 'ZAR_JPY']

        currency_combinations = list(itertools.combinations(currency_list, 2))
        currency_pairs_list = []
        for i in currency_combinations:
            if '_'.join(i) in all_available_pairs:
                currency_pairs_list.append('_'.join(i))
            elif '_'.join(reversed(i)) in all_available_pairs:
                currency_pairs_list.append('_'.join(reversed(i)))
            else:
                #Exception2Handle: No combination between these two currency
                print("No combination between {} from Oanda".format(i))
                return 2
        return currency_pairs_list

    def get_one_currency_pair(self, currency_A, currency_B):
            if currency_A + '_' + currency_B in self.currency_pairs:
                return [currency_A + '_' + currency_B, True]
            elif currency_B + '_' + currency_A in self.currency_pairs:
                return [currency_B + '_' + currency_A, False]
            else:
                #Exception2Handle:
                print("No pair between {} and {} available in self.currency_pairs".format(currency_A, currency_B))
                return 2


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
        print("\n\n### The requested ARENA record has been successfully exported. ###")
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

    def execute_trade(self, _time, _sell_currency, _buy_currency, _trade_unit, _trade_unit_in_buy_currency = True):
        #Progess2Handle: _trade_unit_in_buy_currency = False.
        #Exception2Handle: _sell_currency, _buy_currency not in arena.

        currency_pair, pair_reverse_flag = self.get_one_currency_pair(_sell_currency, _buy_currency)

        trade_ratio = float(self.market_LUT(_time)[currency_pair+'_close'].iloc[0,])
        #Exception2Handle: market_LUT return NaN.

        if _trade_unit_in_buy_currency:
            if pair_reverse_flag:
                self.currency_balance[_sell_currency] -= _trade_unit / trade_ratio
            else:
                self.currency_balance[_sell_currency] -= _trade_unit * trade_ratio
            #Exception2Handle: no enough balance.
            self.currency_balance[_buy_currency] += _trade_unit

        elif not _trade_unit_in_buy_currency:
            self.currency_balance[_sell_currency] -= _trade_unit
            #Exception2Handle: no enough balance.
            if pair_reverse_flag:
                self.currency_balance[_buy_currency] += _trade_unit * trade_ratio
            else:
                self.currency_balance[_buy_currency] += _trade_unit / trade_ratio
        else:
            #Exception2Handle: invalid _trade_unit_in_buy_currency input
            print("Invalid _trade_unit_in_buy_currency input.")
            return 2


        trade_currency = _buy_currency if _trade_unit_in_buy_currency else _sell_currency


        val_list = [self.action_id_counter, _time, _sell_currency, _buy_currency, _trade_unit, trade_currency, trade_ratio, pair_reverse_flag, self.currency_balance[_sell_currency], self.currency_balance[_buy_currency]]
        key_list = ["action_id", "trade_time", "sell_currency", "buy_currency", "trade_unit", "trade_currency", "trade_ratio", "pair_reverse_flag", "sell_currency_balance", "buy_currency_balance"]
        new_trade_action = dict(zip(key_list, val_list))
        # print(json.dumps(new_trade_action, indent=4))
        self.trade_log.append(new_trade_action)

        #Exception2Handle: _time earlier than pervious action in log.
        self.action_id_counter += 1


        # print(json.dumps(self.currency_balance, indent=4))

    #Performance2Handle: do with decorator.
    def trade_log_review(self, raw_flag = False):
        print("#### Displaying the {} trade log of account \"{}\" ####\n".format('RAW' if raw_flag else 'READABLE', self.account_name))
        if raw_flag:
            for i in self.trade_log:
                for k, v in dict.items(i):
                    print("\t\t{:25}{}".format(k+': ', v))
                print("\n")


        else:
            for i in self.trade_log:
                for k, v in dict.items(i):
                    if k == 'action_id' or k == 'trade_time':
                        # print('\t\t-----not in {} ----'.format(k))
                        print("\t\t{:25}{}".format(k+': ', v))

                if i['trade_currency'] == i['buy_currency']:
                    sold_currency_unit = i['trade_unit'] / i['trade_ratio'] if i['pair_reverse_flag'] else i['trade_unit'] * i['trade_ratio']
                    print("\t\t{:25}Sold {} {} for {} {}".format('Trade Decision: ', sold_currency_unit, i['sell_currency'], i['trade_unit'], i['buy_currency']))
                if i['trade_currency'] == i['sell_currency']:
                    bought_currency_unit = i['trade_unit'] * i['trade_ratio'] if i['pair_reverse_flag'] else i['trade_unit'] / i['trade_ratio']
                    print("\t\t{:25}Sold {} {} for {} {}".format('Trade Decision: ', i['trade_unit'], i['sell_currency'], bought_currency_unit, i['buy_currency']))

                print("\t\t{:25}{} {}".format('Sell Currency Balance: ', i['sell_currency_balance'], i['sell_currency']))
                print("\t\t{:25}{} {}".format('Buy Currency Balance: ', i['buy_currency_balance'], i['buy_currency']))
                print("\n")

        print("#### The {} trade log of account \"{}\" has been successfully displayed ####\n".format('RAW' if raw_flag else 'READABLE', self.account_name))

    def account_review(self):
        df = self.areana.record_df
        record_from = df.iloc[0, 0]
        record_to = df.iloc[df.shape[0]-1, 0]
        record_rows = df.shape[0]
        print("\n##### Displaying information regarding account \"{}\". #####\n\n\t{:30}{}\n\t{:30}{}\n\t{:30}{}\n\t{:30}{}\n\n\t{:30}{}".format(self.account_name, 'record_from: ', record_from, 'record_to: ', record_to, 'request_interval: ', self.request_interval, 'record_rows: ', record_rows, 'trade_log_len: ', len(self.trade_log)))

        for k, v in dict.items(self.currency_balance):
            print("\t{:30}{}".format(k+': ', v))
        print("\n##### The information of account \"{}\" has been successfully displayed. #####\n".format(self.account_name))

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
# 2019-01-01T23:55:00.000000000Z,109.667,5.0,139.884,8.0,1.27540,53.0


time_1 = '2019-01-01T22:30:00.000000000Z'
time_2 = '2019-01-01T22:41:00.000000000Z'
time_3 = '2019-01-01T22:55:00.000000000Z'
time_4 = '2019-01-01T22:59:00.000000000Z'
time_5 = '2019-01-01T23:02:00.000000000Z'
time_6 = '2019-01-01T23:05:00.000000000Z'
time_7 = '2019-01-01T23:55:00.000000000Z'

TI_test.execute_trade(time_1, 'USD', 'GBP', 10)
TI_test.execute_trade(time_2, 'GBP', 'USD', 20)
TI_test.execute_trade(time_3, 'GBP', 'JPY', 30)
TI_test.execute_trade(time_4, 'JPY', 'GBP', 40)
TI_test.execute_trade(time_5, 'JPY', 'USD', 50)
TI_test.execute_trade(time_6, 'USD', 'JPY', 60)
TI_test.execute_trade(time_7, 'USD', 'JPY', 70, False)




TI_test.trade_log_review()
# TI_test.trade_log_review(True)
TI_test.account_review()


