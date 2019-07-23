import trade_interface as TI


###############################################################################
_account_name = 'dev_train_interface'
_currency_balance = {'USD': 30000, 'JPY': 30000, 'GBP': 30000}
_from = "2019-01-01T00:00:00Z"
_to = "2019-01-02T00:00:00Z"
_interval = "M1"

###############################################################################
time_1 = '2019-01-01T22:30:00.000000000Z'
time_2 = '2019-01-01T22:41:00.000000000Z'
time_3 = '2019-01-01T22:55:00.000000000Z'
time_4 = '2019-01-01T22:59:00.000000000Z'
time_5 = '2019-01-01T23:02:00.000000000Z'
time_6 = '2019-01-01T23:05:00.000000000Z'
time_7 = '2019-01-01T23:55:00.000000000Z'

###############################################################################
if __name__ == "__main__":
    TI_train = TI.Trade_Interface(_account_name, _currency_balance, _from, _to, _interval)

    TI_train.execute_trade(time_1, 'USD', 'GBP', 10)
    TI_train.execute_trade(time_2, 'GBP', 'USD', 20)
    TI_train.execute_trade(time_3, 'GBP', 'JPY', 30)
    TI_train.execute_trade(time_4, 'JPY', 'GBP', 40)
    TI_train.execute_trade(time_5, 'JPY', 'USD', 50)
    TI_train.execute_trade(time_6, 'USD', 'JPY', 60)
    TI_train.execute_trade(time_7, 'USD', 'JPY', 70, False)

    TI_train.trade_log_review()
    TI_train.account_review()