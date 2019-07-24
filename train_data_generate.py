import trade_interface as TI
import copy

_account_name = 'dev_train_interface'
_currency_balance = {'USD': 30000, 'JPY': 30000, 'GBP': 30000}
_from = "2018-01-01T00:00:00Z"
# _to = "2018-01-02T00:00:00Z"
_to = "2019-01-01T00:00:00Z"
_interval = "M5"


# if __name__ == "__main__":
#     TI_common_data = TI.Trade_Interface(_account_name, _currency_balance, _from, _to, _interval)