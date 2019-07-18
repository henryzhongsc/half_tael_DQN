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




class Oanda_Interface:
    def __init__(self, _account_id, _access_token):
        self.account_id = _account_id
        self.access_token = _access_token
        self.nationality = "USA"
        self.client = oandapyV20.API(access_token=self.access_token)
        self.action = []
        self.trade_history = []

    def get_history_price(self, _from, _to, _interval, _currency_pair):
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

        csv_filename = './dummy_data/' + _currency_pair + '_' + _from[0:19] + '_' + _to[0:19] + '_' + _interval + '.csv'
        df.to_csv(csv_filename, index = None, header = True)
        print("\n\nThe requested record has been successfully exported.\n\t{:16}{}\n\t{:16}{}\n\t{:16}{}\n\t{:16}{}\n\t{:16}{}\n\t{:16}{}\n".format('file path:', csv_filename, 'currency pair: ', _currency_pair, 'from: ', _from, 'to: ', _to, 'interval: ', _interval, 'total rows:', df.shape[0]))
        return df

    def get_history_price_segment(self, _currency_pair, _params):
        for r in InstrumentsCandlesFactory(instrument = _currency_pair, params = _params):
            print("REQUEST: {} {} {}".format(r, r.__class__.__name__, r.params))
            record_json = self.client.request(r)
            new_df = pd.io.json.json_normalize(record_json['candles'])
            yield new_df


my_account_id = '101-001-11707432-001'
my_access_token = 'a10a1538b3fdaf3a8a2f3b9a496a3aeb-00a7b8f54791fb3132b22ca77419cc58'
OI = Oanda_Interface(my_account_id, my_access_token)

# _from = "2017-01-01T00:00:00Z"
# _to = "2017-12-31T23:59:59Z"
# _interval = "H1"
# _currency_pair = "USD_JPY"

_from = "2018-01-01T00:00:00Z"
_to = "2018-12-31T23:59:59Z"
_interval = "H1"
_currency_pair = "USD_JPY"

df = OI.get_history_price(_from, _to, _interval, _currency_pair)
df
