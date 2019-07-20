import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.instruments as instruments
from oandapyV20.exceptions import V20Error, StreamTerminated

from oandapyV20.contrib.factories import InstrumentsCandlesFactory

import time
import datetime
import pandas as pd
import numpy as np

csv_export_dir = './test_data/'
my_account_id = '101-001-11707432-001'
my_access_token = 'a10a1538b3fdaf3a8a2f3b9a496a3aeb-00a7b8f54791fb3132b22ca77419cc58'

class Onada_Record:
    def __init__(self, _record, _record_path, _from, _to, _interval, _currency_pair):
        self.record_df = _record
        self.record_path = _record_path
        self.currency_pair = _currency_pair
        self.from_time = _from
        self.to_time = _to
        self.request_interval = _interval
        self.rows = _record.shape[0]

    def record_review(self):
        print("\n\t{:20}{}\n\t{:20}{}\n\t{:20}{}\n\t{:20}{}\n\t{:20}{}\n\t{:20}{}\n".format('file path:', self.record_path, 'currency pair(s): ', self.currency_pair, 'from: ', self.from_time, 'to: ', self.to_time, 'interval: ', self.request_interval, 'total rows:', self.rows))


class Oanda_Interface:
    def __init__(self, _account_id, _access_token):
        self.account_id = _account_id
        self.access_token = _access_token
        self.nationality = "USA"
        self.client = oandapyV20.API(access_token=self.access_token)

    def get_history_price(self, _from, _to, _interval, _currency_pair, close_price_only = False):
        _params = {
            "from": _from,
            "to": _to,
            "granularity": _interval
        }

        existed_df = pd.DataFrame()
        for new_df in self.get_history_price_segment(_currency_pair, _params):
            existed_df = pd.concat([existed_df, new_df]).reset_index(drop=True)
        df = existed_df.rename(index=str, columns={"mid.o": "open_price", "mid.h": "high_price", "mid.l": "low_price", "mid.c": "close_price"})
        df = df.reindex(columns=['time', 'open_price', 'high_price', 'low_price', 'close_price', 'complete', 'volume'])

        csv_filename = csv_export_dir + _currency_pair + '_' + _from[0:19] + '_' + _to[0:19] + '_' + _interval + '.csv'
        if close_price_only:
            df = df.drop(['open_price', 'high_price', 'low_price', 'complete'], axis =1)
            df = df.rename(index=str, columns={'close_price': _currency_pair + '_close', 'volume': _currency_pair + '_volume'})
            # print(df)
        df.to_csv(csv_filename, index = None, header = True)


        temp_OR = Onada_Record(df, csv_filename, _from, _to, _interval, _currency_pair)
        print("\n\nThe requested record has been successfully exported.")
        temp_OR.record_review()
        return temp_OR

    def get_history_price_segment(self, _currency_pair, _params):
        for r in InstrumentsCandlesFactory(instrument = _currency_pair, params = _params):
            # print("REQUEST: {} {} {}".format(r, r.__class__.__name__, r.params))
            record_json = self.client.request(r)
            new_df = pd.io.json.json_normalize(record_json['candles'])
            yield new_df



# OI = Oanda_Interface(my_account_id, my_access_token)

# _from = "2019-01-01T00:00:00Z"
# _to = "2019-01-02T00:00:00Z"
# _interval = "M1"
# USD_JPY_currency_pair = "USD_JPY"
# GBP_JPY_currency_pair = "GBP_JPY"
# GBP_USD_currency_pair = "GBP_USD"

# OR_test = OI.get_history_price(_from, _to, _interval, USD_JPY_currency_pair)
