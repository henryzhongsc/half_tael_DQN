import sys
sys.path.append('.')
import trade_interface as TI
import copy

###############################################################################
_account_name = 'dev_train_interface'
_currency_balance = {'USD': 30000, 'JPY': 30000, 'GBP': 30000}
_from = "2019-01-01T00:00:00Z"
_to = "2019-01-02T00:00:00Z"
_interval = "M1"

# _to = "2018-01-02T00:00:00Z"
# Test case for <class 'trade_interface.TI_Account_Error'> is raised as: self.from_time 2019-01-01T00:00:00Z is earlier than self.to_time 2018-01-02T00:00:00Z.

###############################################################################

# time_0 = '2019-01-01T22:03:00.000000000Z'
# Test case for During self.execute_trade()
# 	<class 'trade_interface.TI_Market_LUT_Error'> is raised as: Time input: 2019-01-01T22:03:00.000000000Z returns np.nan

# time_2 = '2019-01-01T22:29:00.000000000Z'
# Test case for During self.execute_trade()
# 	<class 'trade_interface.TI_Execution_Error'> is raised as: _time 2019-01-01T22:29:00.000000000Z is earlier than pervious action's trade_time 2019-01-01T22:30:00.000000000Z in log.

###############################################################################

# Several _time input for execute_trade() method.
time_1 = '2019-01-01T22:30:00.000000000Z'
time_2 = '2019-01-01T22:41:00.000000000Z'
time_3 = '2019-01-01T22:55:00.000000000Z'
time_4 = '2019-01-01T22:59:00.000000000Z'
time_5 = '2019-01-01T23:02:00.000000000Z'
time_6 = '2019-01-01T23:05:00.000000000Z'
time_7 = '2019-01-01T23:55:00.000000000Z'
time_8 = '2019-01-01T23:57:00.000000000Z'

time_initial = '2019-01-01T22:00:00.000000000Z' # Initial time to checkout all currency in USD, in other to compare with time_end after experimenting the trade strategy.
time_end = '2019-01-01T23:59:00.000000000Z' # End time to checkout profit in USD.

###############################################################################
if __name__ == "__main__":
    TI_train = TI.Trade_Interface(_account_name, _currency_balance, _from, _to, _interval) # Build trading account.

    # Review the initial worth of account in USD before any trade was made.
    TI_initial = copy.deepcopy(TI_train) # Copy the account status before all trades to prepare for checkout review.
    TI_initial.account_name = 'Initial_Checkout_Review'
    TI_initial.checkout_all_in(time_initial, 'USD')
    TI_initial.account_review()

    print("!"*50)

    # TI_train.execute_trade(time_0, 'USD', 'JPY', 100)
    # Test case for During self.execute_trade()
    # 	<class 'trade_interface.TI_Market_LUT_Error'> is raised as: Time input: 2019-01-01T22:03:00.000000000Z returns np.nan

    # Several trade actions.
    TI_train.execute_trade(time_1, 'USD', 'GBP', 10)
    TI_train.execute_trade(time_2, 'GBP', 'USD', 20)
    TI_train.execute_trade(time_3, 'GBP', 'JPY', 30)
    TI_train.execute_trade(time_4, 'JPY', 'GBP', 40)
    TI_train.execute_trade(time_5, 'JPY', 'USD', 50)
    TI_train.execute_trade(time_6, 'USD', 'JPY', 60)
    TI_train.execute_trade(time_7, 'USD', 'JPY', 70, _trade_unit_in_buy_currency = False)
    TI_train.execute_trade(time_8, 'JPY', 'USD', 1000000)


    TI_train.trade_log_review() # Review trade log.
    TI_train.account_review() # Review account balance after all trades, with decriptive info of this account.


    print("@"*50)

    # Review the final worth of account in USD after all trades were made.
    TI_end = copy.deepcopy(TI_train) # Copy the account status after all trades to prepare for checkout review.
    TI_end.account_name = 'End_Checkout_Review' # Rename the account with a descriptive name to be distinguishable from other account.
    TI_end.checkout_all_in(time_end, 'USD')
    TI_end.account_review()
