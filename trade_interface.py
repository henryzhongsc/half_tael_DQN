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

from oanda_config import *



###############################################################################
arena_csv_export_dir = './arena_data/'
###############################################################################



class TI_Account_Error(Exception):
    pass

class TI_Market_LUT_Error(Exception):
    pass

class TI_Execution_Error(Exception):
    pass

class TI_Accunt_Balance_Error(Exception):
    pass

class OI_Onanda_Error(Exception):
    pass





def account_input_report(decorated):
    def inner(*args):
        try:
            decorated(*args)
        except TI_Account_Error as e:
            sys.exit("During self.account_input_eval()\n\t{} is raised as: {}".format(type(e), e))
    return inner

def execution_report(decorated):
    def inner(*args, **kwargs):
        try:
            decorated(*args, **kwargs)
        except TI_Market_LUT_Error as e:
            sys.exit("During self.execute_trade()\n\t{} is raised as: {}".format(type(e), e))
        except TI_Execution_Error as e:
            sys.exit("During self.execute_trade()\n\t{} is raised as: {}".format(type(e), e))
        except TI_Accunt_Balance_Error as e:
            sys.exit("During self.execute_trade()\n\t{} is raised as: {}".format(type(e), e))
    return inner


class Trade_Interface:
    @account_input_report
    def __init__(self, _account_name, _currency_balance, _from_time, _to_time, _request_interval, _output_arena_csv = True, _output_raw_csv = False):
        self.account_name = _account_name
        self.currency_balance = _currency_balance
        self.from_time = _from_time
        self.to_time = _to_time
        self.request_interval = _request_interval
        self.all_currency_list = [k for k in self.currency_balance]

        self.output_arena_csv = _output_arena_csv
        self.output_raw_csv = _output_raw_csv

        self.account_input_eval()

        try:
            self.currency_pairs = self.get_currency_pairs(self.all_currency_list)
        except TI_Account_Error as e:
            sys.exit("During self.get_currency_pairs()\n\t{} is raised due to: {}".format(type(e), e))
        try:
            self.arena = self.get_arena(self.currency_pairs)
        except OI_Onanda_Error as e:
            sys.exit("During self.get_arena()\n\t{} is raised due to: {}".format(type(e), e))
        except TI_Account_Error as e:
            sys.exit("During self.get_arena()\n\t{} is raised due to: {}".format(type(e), e))

        self.action_id_counter = 0
        self.trade_log = []

    def account_input_eval(self):
        for k, v in dict.items(self.currency_balance):
            if v < 0:
                raise TI_Account_Error('Invalid account input, self.currency_balance[\'{}\'] must be >= 0 (currently {}).'.format(k, v))

        oanda_granularity = ['S5', 'S10', 'S15', 'S30', 'M1', 'M2', 'M3', 'M4', 'M5', 'M10', 'M15', 'M30', 'H1', 'H2', 'H3', 'H4', 'H6', 'H8', 'H12', 'D']
        if self.request_interval not in oanda_granularity:
            raise TI_Account_Error('Invalid Oanda granularity input, self.request_interval: {}.'.format(self.request_interval))

        if not self.time_is_later(self.from_time, self.to_time, equal_time_acceptable = False):
            raise TI_Account_Error("self.from_time {} is earlier than self.to_time {}.".format(self.from_time, self.to_time))


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
                raise TI_Account_Error("No currency pair(s) between {} from Oanda".format(i))
        return currency_pairs_list

    def get_one_currency_pair(self, currency_A, currency_B):
            if currency_A + '_' + currency_B in self.currency_pairs:
                return [currency_A + '_' + currency_B, True]
            elif currency_B + '_' + currency_A in self.currency_pairs:
                return [currency_B + '_' + currency_A, False]
            else:
                raise TI_Execution_Error("No currency pair between {} and {} available in {}".format(currency_A, currency_B, self.currency_pairs))



    def get_arena(self, currency_pairs):
        close_price_only_flag = True
        currency_ORs = []
        for i in currency_pairs:
            OI_temp = OI.Oanda_Interface(my_account_id, my_access_token)
            try:
                OR_temp = OI_temp.get_history_price(self.from_time, self.to_time, self.request_interval, i, close_price_only_flag, _output_raw_csv = self.output_raw_csv)
            except OI.oandapyV20.exceptions.V20Error as e:
                raise OI_Onanda_Error(e)
            except ValueError as e:
                raise TI_Account_Error(e)

            currency_ORs.append(OR_temp)

        # for i in currency_ORs:
        #     print('{} has unique index: {}'.format(i.currency_pair, i.record_df.set_index('time').index.is_unique))
        #     print(i.record_df.set_index('time')[i.record_df.set_index('time').index.duplicated()])

        currency_ORs_dfs = [i.record_df.set_index('time') for i in currency_ORs]
        currency_ORs_dfs = [i.loc[~i.index.duplicated(keep='first')] for i in currency_ORs_dfs]


        arena_df = pd.concat([i for i in currency_ORs_dfs], axis=1, join='outer', sort=True).reset_index()
        arena_df = arena_df.rename(index=str, columns={'index': 'time'})
        arena_df = arena_df.fillna(method='ffill')
        # print("NaN value within arena_df: {}".format(arena_df.isnull().sum().sum()))


        arena_filename = arena_csv_export_dir + '_'.join(self.all_currency_list) + '_' + self.from_time[0:19] + '_' + self.to_time[0:19] + '_' + self.request_interval + '.csv'
        if self.output_arena_csv:
            if not os.path.exists(arena_csv_export_dir):
                os.makedirs(arena_csv_export_dir)
            arena_df.to_csv(arena_filename, index = None, header = True)


        OR_arena = OI.Onada_Record(arena_df, arena_filename, self.from_time, self.to_time, self.request_interval, self.all_currency_list)
        print("\n\n### The requested ARENA record has been successfully exported. ###")
        OR_arena.record_review()
        return OR_arena


    def market_LUT(self, _time):
        df = self.arena.record_df
        target_df = df.loc[df['time'] == _time]
        if target_df.empty:
            raise TI_Market_LUT_Error('Invalid time input: {}'.format(_time))
        else:
            # print(target_df.head())
            return target_df

    @execution_report
    def execute_trade(self, _time, _sell_currency, _buy_currency, _trade_unit, _trade_unit_in_buy_currency = True, review_checkout_only = False, balance_protection = True):
        temp_currency_list = self.all_currency_list
        if _sell_currency not in temp_currency_list or _buy_currency not in temp_currency_list:
            raise TI_Execution_Error('{} or {} is(are) not in {}'.format(_sell_currency, _buy_currency, temp_currency_list))

        try:
            currency_pair, pair_reverse_flag = self.get_one_currency_pair(_sell_currency, _buy_currency)
        except TI_Execution_Error as e:
            sys.exit("During self.get_one_currency_pair()\n\t{} is raised due to: {}".format(type(e), e))

        try:
            trade_ratio = float(self.market_LUT(_time)[currency_pair+'_close'].iloc[0,])
        except TI_Market_LUT_Error as e:
            sys.exit("During self.market_LUT()\n\t{} is raised due to: {}".format(type(e), e))

        if pd.isna(trade_ratio):
            raise TI_Market_LUT_Error('Time input: {} returns np.nan'.format(_time))


        sell_currency_balance_before_trade = self.currency_balance[_sell_currency]
        buy_currency_balance_before_trade = self.currency_balance[_buy_currency]



        if _trade_unit_in_buy_currency:
            if pair_reverse_flag:
                self.currency_balance[_sell_currency] -= _trade_unit / trade_ratio
            else:
                self.currency_balance[_sell_currency] -= _trade_unit * trade_ratio
            self.currency_balance[_buy_currency] += _trade_unit

        elif not _trade_unit_in_buy_currency:
            self.currency_balance[_sell_currency] -= _trade_unit
            if pair_reverse_flag:
                self.currency_balance[_buy_currency] += _trade_unit * trade_ratio
            else:
                self.currency_balance[_buy_currency] += _trade_unit / trade_ratio
        else:
            raise TI_Execution_Error('Invalid _trade_unit_in_buy_currency input: {}'.format(_trade_unit_in_buy_currency))

        balance_protection_flag = False
        if self.currency_balance[_sell_currency] < 0:
            if balance_protection:
                self.currency_balance[_sell_currency] = sell_currency_balance_before_trade
                self.currency_balance[_buy_currency] = buy_currency_balance_before_trade
                balance_protection_flag = True
            else:
                raise TI_Accunt_Balance_Error('{} balance < 0 after trade action #{} (currently {}).'.format(_sell_currency, self.action_id_counter,  self.currency_balance[_sell_currency]))

        trade_currency = _buy_currency if _trade_unit_in_buy_currency else _sell_currency

        if not review_checkout_only:
            if self.action_id_counter != 0:
                pervious_log = self.trade_log[-1]
                if not self.time_is_later(pervious_log['trade_time'], _time, equal_time_acceptable = False):
                    raise TI_Execution_Error("_time {} is earlier than pervious action's trade_time {} in log.".format(_time, pervious_log['trade_time']))
        else:
            if self.action_id_counter != 0:
                pervious_log = self.trade_log[-1]
                if not self.time_is_later(pervious_log['trade_time'], _time, equal_time_acceptable = True):
                    raise TI_Execution_Error("_time {} is earlier than pervious action's trade_time {} in log.".format(_time, pervious_log['trade_time']))


        val_list = [self.action_id_counter, _time, _sell_currency, _buy_currency, _trade_unit, trade_currency, trade_ratio, pair_reverse_flag, self.currency_balance[_sell_currency], self.currency_balance[_buy_currency], balance_protection_flag]
        key_list = ["action_id", "trade_time", "sell_currency", "buy_currency", "trade_unit", "trade_currency", "trade_ratio", "pair_reverse_flag", "sell_currency_balance", "buy_currency_balance", "balance_protection_flag"]
        new_trade_action = dict(zip(key_list, val_list))
        # print(json.dumps(new_trade_action, indent=4))
        self.trade_log.append(new_trade_action)




        self.action_id_counter += 1


        # print(json.dumps(self.currency_balance, indent=4))

    def checkout_all_in(self, _time, tar_currency):
        for k, v in dict.items(self.currency_balance):
            if k != tar_currency:
                self.execute_trade(_time, k, tar_currency, v, _trade_unit_in_buy_currency = False, review_checkout_only = True)

    def time_is_later(self, time_A, time_B, equal_time_acceptable = False):
        time_A_strip = re.split('-|:|\.|T|Z', time_A)
        del time_A_strip[-1]
        time_B_strip = re.split('-|:|\.|T|Z', time_B)
        del time_B_strip[-1]

        time_B_is_later_flag = equal_time_acceptable
        for a, b in zip(time_A_strip, time_B_strip):
            if int(a) < int(b):
                time_B_is_later_flag = True
                break
            elif int(a) > int(b):
                time_B_is_later_flag = False
                break
            else:
                continue
        return time_B_is_later_flag


    def trade_log_review(self, tar_action_id = False, raw_flag = False):
        print("#### Displaying the {} trade log of account \"{}\" (action: {}) ####\n".format('RAW' if raw_flag else 'READABLE', self.account_name, 'ALL' if tar_action_id is False else tar_action_id))

        if tar_action_id is False:
            log_to_display = self.trade_log
        else:
            if tar_action_id == 'LAST':
                all_action_ids = [i['action_id'] for i in self.trade_log]
                tar_action_id = max(all_action_ids)

            log_to_display = []
            for i in self.trade_log:
                if i['action_id']  == tar_action_id:
                    log_to_display.append(i)
                    break

        if raw_flag:
            for i in log_to_display:
                for k, v in dict.items(i):
                    print("\t\t{:25}{}".format(k+': ', v))
                print("\n")


        else:
            for i in log_to_display:
                for k, v in dict.items(i):
                    if k == 'action_id' or k == 'trade_time':
                        # print('\t\t-----not in {} ----'.format(k))
                        print("\t\t{:25}{}".format(k+': ', v))


                if i['trade_currency'] == i['buy_currency']:
                    sold_currency_unit = i['trade_unit'] / i['trade_ratio'] if i['pair_reverse_flag'] else i['trade_unit'] * i['trade_ratio']
                    print("\t\t{:25}Sold {} {} for {} {} ({})".format('Trade Decision: ', sold_currency_unit, i['sell_currency'], i['trade_unit'], i['buy_currency'], 'failed' if i["balance_protection_flag"] else 'succeeded'))
                if i['trade_currency'] == i['sell_currency']:
                    bought_currency_unit = i['trade_unit'] * i['trade_ratio'] if i['pair_reverse_flag'] else i['trade_unit'] / i['trade_ratio']
                    print("\t\t{:25}Sold {} {} for {} {} ({})".format('Trade Decision: ', i['trade_unit'], i['sell_currency'], bought_currency_unit, i['buy_currency'], 'failed' if i["balance_protection_flag"] else 'succeeded'))

                if i["balance_protection_flag"]:
                    print("\t\t{:25}Trade unsuccessful as {} {} is not enough for the sell".format('Sell Balance Protection: ', i['sell_currency_balance'], i['sell_currency']))

                print("\t\t{:25}{} {}".format('Sell Currency Balance: ', i['sell_currency_balance'], i['sell_currency']))
                print("\t\t{:25}{} {}".format('Buy Currency Balance: ', i['buy_currency_balance'], i['buy_currency']))
                print("\n")

        print("#### The {} trade log of account \"{}\" has been successfully displayed (action: {}) ####\n".format('RAW' if raw_flag else 'READABLE', self.account_name,  'ALL' if tar_action_id is False else tar_action_id))

    def account_review(self):
        df = self.arena.record_df
        record_from = df.iloc[0, 0]
        record_to = df.iloc[df.shape[0]-1, 0]
        record_rows = df.shape[0]
        print("\n##### Displaying information regarding account \"{}\". #####\n\n\t{:30}{}\n\t{:30}{}\n\t{:30}{}\n\t{:30}{}\n\n\t{:30}{}".format(self.account_name, 'record_from: ', record_from, 'record_to: ', record_to, 'request_interval: ', self.request_interval, 'record_rows: ', record_rows, 'trade_log_len: ', len(self.trade_log)))

        for k, v in dict.items(self.currency_balance):
            print("\t{:30}{}".format(k+': ', v))
        print("\n##### The information of account \"{}\" has been successfully displayed. #####\n".format(self.account_name))


###############################################################################



