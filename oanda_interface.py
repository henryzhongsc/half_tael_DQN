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
import os
import pandas as pd
import numpy as np

from oanda_config import *

###############################################################################
two_currency_csv_export_dir = './raw_data/'
###############################################################################


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
        print("\t{:20}{}\n\t{:20}{}\n\t{:20}{}\n\t{:20}{}\n\t{:20}{}\n\t{:20}{}\n".format('file path:', self.record_path, 'currency pair(s): ', self.currency_pair, 'from: ', self.from_time, 'to: ', self.to_time, 'interval: ', self.request_interval, 'total rows:', self.rows))


class Oanda_Interface:
    def __init__(self, _account_id, _access_token):
        self.account_id = _account_id
        self.access_token = _access_token
        self.nationality = "USA"
        self.client = oandapyV20.API(access_token=self.access_token)

    def get_history_price(self, _from, _to, _interval, _currency_pair, close_price_only = False, nan_fill = True, _output_raw_csv = False):
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

        if not os.path.exists(two_currency_csv_export_dir):
            os.makedirs(two_currency_csv_export_dir)
        csv_filename = two_currency_csv_export_dir + _currency_pair + '_' + _from[0:19] + '_' + _to[0:19] + '_' + _interval + '.csv'
        if close_price_only:
            df = df.drop(['open_price', 'high_price', 'low_price', 'complete'], axis =1)
            df = df.rename(index=str, columns={'close_price': _currency_pair + '_close', 'volume': _currency_pair + '_volume'})
            # print(df)
            df = df.fillna(method='ffill')

        if _output_raw_csv:
            df.to_csv(csv_filename, index = None, header = True)
            print("\n\n## The requested record has been successfully exported. ##")


        temp_OR = Onada_Record(df, csv_filename, _from, _to, _interval, _currency_pair)
        print("\n\n## The requested record has been successfully retrieved. ##")
        temp_OR.record_review()
        return temp_OR

    def get_history_price_segment(self, _currency_pair, _params):
        for r in InstrumentsCandlesFactory(instrument = _currency_pair, params = _params):
            # print("REQUEST: {} {} {}".format(r, r.__class__.__name__, r.params))
            record_json = self.client.request(r)
            new_df = pd.io.json.json_normalize(record_json['candles'])
            yield new_df
