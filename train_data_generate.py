import trade_interface as TI
import copy


# _account_name = 'train_data' # 74277 rows.
# _currency_balance = {'USD': 30000, 'JPY': 30000, 'GBP': 30000}
# _from = "2017-01-01T00:00:00Z"
# _to = "2018-01-01T00:00:00Z"
# _interval = "M5"

# _account_name = 'test_data' # 74590 rows.
# _currency_balance = {'USD': 30000, 'JPY': 30000, 'GBP': 30000}
# _from = "2018-01-01T00:00:00Z"
# _to = "2019-01-01T00:00:00Z"
# _interval = "M5"

# _account_name = 'lightweight_trial_data' # 6358 rows.
# _currency_balance = {'USD': 30000, 'JPY': 30000, 'GBP': 30000}
# _from = "2019-01-01T00:00:00Z"
# _to = "2019-02-01T00:00:00Z"
# _interval = "M5"


# _account_name = 'DQN_v1.0_trial_data_remix' # 4999 rows.
# _currency_balance = {'EUR': 30000, 'GBP': 30000}
# _from = "2018-04-13T18:30:00Z"
# _to = "2018-04-19T14:58:00Z"
# _interval = "M1"

# _account_name = 'DQN_v1.0_trial_data_remix_with_USD' # 5488 rows.
# _currency_balance = {'USD': 30000, 'EUR': 30000, 'GBP': 30000}
# _from = "2018-04-13T18:30:00Z"
# _to = "2018-04-19T14:58:00Z"
# _interval = "M1"

_account_name = 'DQN_v1.0_trial_data_4800_line' # 4800 rows.
_currency_balance = {'USD': 0, 'EUR': 100000, 'GBP': 0}
_from = "2018-04-13T18:30:00Z"
_to = "2018-04-19T03:27:00Z"
_interval = "M1"

if __name__ == "__main__":
    TI_data_generate = TI.Trade_Interface(_account_name, _currency_balance, _from, _to, _interval)