# 🔰 User Manual for `trade_interface.py`

> This file serves as the user manual for interacting with [`trade_interface`](https://github.com/choH/half_tael_DQN/blob/master/trade_interface.py). By convention, we name the file contains such interactions as `train_interface_SomethingReasonable.py`, e.g. [`train_interface_demo.py`](https://github.com/choH/half_tael_DQN/blob/master/demo_and_manual/train_interface_demo.py).
>
> 📌 v2.0 | 2019-09-02 | Henry Zhong

---
## 1. What does [`trade_interface`](https://github.com/choH/half_tael_DQN/blob/master/trade_interface.py) do?

It interacts with [OANDA](https://trade.oanda.com) through `oandapyV20` API (wrapped in [`oanda_interface.py`](https://github.com/choH/half_tael_DQN/blob/master/oanda_interface.py)) to get market information between two time points, and mimics trading on such interval.

To start, create a `.py` file with headers set to:
```
import trade_interface as TI
import copy
```

---
## 2. Supported Methods


### 2.1. Trade_Interface(self, _account_name, _currency_balance, _from_time, _to_time, _request_interval, _output_arena_csv = True, _output_raw_csv = False)
* **`_account_name`**:
    * `str`
    * a descriptive name of this account, should be distinguishable from other accounts.
* **`_currency_balance`**:
    * `dict`, `k = str` and `v = int/float`.
    * Forms like `{'USD': 30000, 'JPY': 30000, 'GBP': 30000}`. Where there must be `currency_pair` — checkout *Section 5.1. Supported `currenct_pair`s* —  between every two keys within dict.
* **`_from_time`**
    * `str`
    * Forms like `"YYYY-MM-DDTHH:MM:SSZ"`, setting the starting time point.
* **`_to_time`**
    * `str`
    * Forms like `"YYYY-MM-DDTHH:MM:SSZ"`, setting the ending time point.
    * Must be later than `_from` chronologically.
* **`_request_interval`**
    * `str`
    * Must be supported in *Section 5.2. Supported `request_interval`s*.
* **`_output_arena_csv`**
    * Keyword argument, default to `True`.
    * `True`: Output arena DataFrame (joint price data between all currencies) as CSV files to [./arena_data/](https://github.com/choH/half_tael_DQN/tree/master/arena_data) folder.
        * If the output directory does not exist, make such directory.
    * `False`: Do not output any arena_data CSV file.
*  **`_output_raw_csv`**
    * Keyword argument, default to `False`.
     * `True`: Output arena DataFrame (joint price data between all currencies) as CSV files to `./raw_data/` folder (ignore by [`.gitignore`](https://github.com/choH/half_tael_DQN/blob/master/.gitignore)).
        * If the output directory does not exist, make such directory.
    * `False`: Do not output any raw_data CSV file.

This class method will build a virtual account with access to trading record (defined by `_from`, `_to`, `_interval`, and `k` in `_currency_balance`) you specified. It will also register your account name and balance as stated in `_account_name` and `_currency_balance` respectively.

### 2.2. execute_trade(_time, _sell_currency, _buy_currency, _trade_unit, _trade_unit_in_buy_currency = True, review_checkout_only = False, balance_protection = True)

* **`_time`**
    * `str`
    * Forms like `"YYYY-MM-DDTHH:MM:SSZ"`, setting the execution time of this specific trade.
* **`_sell_currency`**
    * `str`
    * Set the currency you want to sell out, must be supported in *Section 5.1. Supported `currenct_pair`s* .
* **`_buy_currency`**
    * `str`
    * Set the currency you want to buy in, such currency must be included by the `k` of `_currency_balance` which perviously passed to its `Trade_Interface()` constructor.
* **`_trade_unit`**
    * `int` or `float`.
    * Set the unit of currency you want to trade.
* **`_trade_unit_in_buy_currency`**
    * Keyword argument, default to `True`.
    * `True`: buy in `_trade_unit` amount of `_buy_currency`.
    * `False`: buy in a certain amount of `_buy_currency` worth by `_trade_unit` * `_sell_currency`.

* **`review_checkout_only`**
    * Keyword argument, default to `False`.
    * `True`: If the method `execute_trade()` will be called again later, the `_time` input of the future call can be same as the `_time` input of current call.
    * `False`: Similar, but the `_time` input of the future call must be chronologically later than the `_time` input of current call.

* **`balance_protection`**
    * Keyword argument, default to `True`.
    * `True`: If the balance of sell currency is not enough to execute the requested trade, such trade will be canceled. The trade log will mark such trade as "failed."
    * `False`: If the balance of sell currency is not enough to execute the requested trade, such trade will be executed (resulted in a negative sell currency balance), and `TI_Account_Balance_Error` will be raised.

This class method will perform a virtual trade decision you made on `_time`, exchange `trade_unit` amount of currency defined by `_trade_unit_in_buy_currency`, between the two currencies you defined (`_buy_currency` and `sell_currency`). It will also accumulate the exchange record to the class's `self.currency_balance` and append this trading decision to `self.trade_log`.


### 2.3. checkout_all_in(_time, tar_currency)
* **`_time`**
    * `str`
    * Forms like `"YYYY-MM-DDTHH:MM:SSZ"`, setting the execution time of the check out.
* **`tar_currency`**
    * `str`
    * Sell out all other currency(s) other than `tar_currency`, such currency must be included by the `k` of `_currency_balance` which perviously passed to its `Trade_Interface()` constructor.


### 2.4. trade_log_review(tar_action_id = False, raw_flag = False)
* **`tar_action_id`**
    * Keyword argument default to `False`, accepts `int`.
    * `int`: retrieve a specific item from `self.trade_log` with `DictItem['action_id'] == int`.
    * `False`: print out all items in `self.trade_log`.
* **`raw_flag`**
    * Keyword argument, default to `False`.
    * `True`: Loop through `self.trade_log` and print out every items directly. e.g.

    ```
    		action_id:               6
    		trade_time:              2019-01-01T23:55:00.000000000Z
    		sell_currency:           USD
    		buy_currency:            JPY
    		trade_unit:              70
    		trade_currency:          USD
    		trade_ratio:             109.667
    		pair_reverse_flag:       True
    		sell_currency_balance:   29986.708793946465
    		buy_currency_balance:    26692.75
    		balance_protection_flag: True
    ```

    * `False`: Loop though `self.trade_log` and print out every items in a  reading-friendly way. e.g.

    ```
    		action_id:               6
    		trade_time:              2019-01-01T23:55:00.000000000Z
    		Trade Decision:          Sold 70 USD for 7676.6900000000005 JPY (succeeded)
    		Sell Currency Balance:   29986.708793946465 USD
    		Buy Currency Balance:    26692.75 JPY   
    ```

### 2.5. account_review()
This class method will print out the current status of the account — determined by its `self.` variables. e.g.

```
##### Displaying information regarding account "dev_train_interface". #####

	record_from:                  2019-01-01T22:00:00.000000000Z
	record_to:                    2019-01-01T23:59:00.000000000Z
	request_interval:             M1
	record_rows:                  118

	trade_log_len:                7
	USD:                          29986.708793946465
	JPY:                          26692.75
	GBP:                          30034.092948617737

##### The information of account "dev_train_interface" has been successfully displayed. #####
```

---

## 3. Custom Exceptions Handling (example only)

### 3.1. TI_Account_Error

```
During self.get_currency_pairs()
	<class 'trade_interface.TI_Account_Error'> is raised due to: No currency pair(s) between ('USD', 'JAY') from Oanda

During self.account_input_eval()
	<class 'trade_interface.TI_Account_Error'> is raised as: Invalid Oanda granularity input, self.request_interval: H20.

During self.account_input_eval()
	<class 'trade_interface.TI_Account_Error'> is raised as: Invalid account input, self.currency_balance['USD'] must be >= 0 (currently -10).

During self.account_input_eval()
	<class 'trade_interface.TI_Account_Error'> is raised as: self.from_time 2019-01-01T00:00:00Z is earlier than self.to_time 2018-01-02T00:00:00Z.
```

### 3.2. TI_Market_LUT_Error


```
During self.market_LUT()
	<class 'trade_interface.TI_Market_LUT_Error'> is raised due to: Invalid time input: 2019-01-01T22:30:20.000000000Z

During self.execute_trade()
	<class 'trade_interface.TI_Market_LUT_Error'> is raised as: Time input: 2019-01-01T22:03:00.000000000Z returns np.nan
```
### 3.3. TI_Execution_Error


```
During self.execute_trade()
	<class 'trade_interface.TI_Execution_Error'> is raised as: USB or GBP is(are) not in ['USD', 'JPY', 'GBP']

During self.execute_trade()
	<class 'trade_interface.TI_Execution_Error'> is raised as: _time 2019-01-01T22:29:00.000000000Z is earlier than pervious action's trade_time 2019-01-01T22:30:00.000000000Z in log.
```

### 3.4. TI_Account_Balance_Error

```
During self.execute_trade()
	<class 'trade_interface.TI_Account_Balance_Error'> is raised as: USD balance < 0 after trade action #0 (currently -127412000.00000001).
```

### 3.5. OI_Onanda_Error
```
During self.get_arena()
	<class 'trade_interface.OI_Onanda_Error'> is raised due to: {"errorMessage":"Insufficient authorization to perform request."}
```

## 4. Sample Code & Sample Output

Sample code available as [`train_interface_demo.py`](https://github.com/choH/half_tael_DQN/blob/master/demo_and_manual/train_interface_demo.py).

Sample output available in *Section Sample Output of `train_interface_demo.py`.*


---

## 5. Appendix

### 5.1. Supported `currenct_pair`s

```
'AUD_CAD', 'AUD_CHF', 'AUD_HKD', 'AUD_JPY', 'AUD_NZD', 'AUD_SGD', 'AUD_USD', 'CAD_CHF', 'CAD_HKD', 'CAD_JPY', 'CAD_SGD', 'CHF_HKD', 'CHF_JPY', 'CHF_ZAR', 'EUR_AUD', 'EUR_CAD', 'EUR_CHF', 'EUR_CZK', 'EUR_DKK', 'EUR_GBP', 'EUR_HKD', 'EUR_HUF', 'EUR_JPY', 'EUR_NOK', 'EUR_NZD', 'EUR_PLN', 'EUR_SEK', 'EUR_SGD', 'EUR_TRY', 'EUR_USD', 'EUR_ZAR', 'GBP_AUD', 'GBP_CAD', 'GBP_CHF', 'GBP_HKD', 'GBP_JPY', 'GBP_NZD', 'GBP_PLN', 'GBP_SGD', 'GBP_USD', 'GBP_ZAR', 'HKD_JPY', 'NZD_CAD', 'NZD_CHF', 'NZD_HKD', 'NZD_JPY', 'NZD_SGD', 'NZD_USD', 'SGD_CHF', 'SGD_HKD', 'SGD_JPY', 'TRY_JPY', 'USD_CAD', 'USD_CHF', 'USD_CNH', 'USD_CZK', 'USD_DKK', 'USD_HKD', 'USD_HUF', 'USD_JPY', 'USD_MXN', 'USD_NOK', 'USD_PLN', 'USD_SAR', 'USD_SEK', 'USD_SGD', 'USD_THB', 'USD_TRY', 'USD_ZAR', 'ZAR_JPY'
```

For every `k` in `_currency_balance` passed to `Trade_Interface()`, there must be a currency pair above which includes every two `k` as `k1_k2` or `k2_k1`.

e.g. `_currency_pair = {'USD': 30000, 'JPY': 30000, 'GBP': 30000}` requires `USD_JPY`, `GBP_JPY`, and `GBP_USD`.



### 5.2. Supported `request_interval`s

```
'S5', 'S10', 'S15', 'S30', 'M1', 'M2', 'M3', 'M4', 'M5', 'M10', 'M15', 'M30', 'H1', 'H2', 'H3', 'H4', 'H6', 'H8', 'H12', 'D'
```

### 5.3. Sample Output of [`train_interface_demo.py`](https://github.com/choH/half_tael_DQN/blob/master/demo_and_manual/train_interface_demo.py).

```
## The requested record has been successfully retrieved. ##
	file path:          ./raw_data/USD_JPY_2019-01-01T00:00:00_2019-01-02T00:00:00_M1.csv
	currency pair(s):   USD_JPY
	from:               2019-01-01T00:00:00Z
	to:                 2019-01-02T00:00:00Z
	interval:           M1
	total rows:         90


## The requested record has been successfully retrieved. ##
	file path:          ./raw_data/GBP_USD_2019-01-01T00:00:00_2019-01-02T00:00:00_M1.csv
	currency pair(s):   GBP_USD
	from:               2019-01-01T00:00:00Z
	to:                 2019-01-02T00:00:00Z
	interval:           M1
	total rows:         98


## The requested record has been successfully retrieved. ##
	file path:          ./raw_data/GBP_JPY_2019-01-01T00:00:00_2019-01-02T00:00:00_M1.csv
	currency pair(s):   GBP_JPY
	from:               2019-01-01T00:00:00Z
	to:                 2019-01-02T00:00:00Z
	interval:           M1
	total rows:         117


### The requested ARENA record has been successfully exported. ###
	file path:          ./arena_data/USD_JPY_GBP_2019-01-01T00:00:00_2019-01-02T00:00:00_M1.csv
	currency pair(s):   ['USD', 'JPY', 'GBP']
	from:               2019-01-01T00:00:00Z
	to:                 2019-01-02T00:00:00Z
	interval:           M1
	total rows:         118


##### Displaying information regarding account "Initial_Checkout_Review". #####

	record_from:                  2019-01-01T22:00:00.000000000Z
	record_to:                    2019-01-01T23:59:00.000000000Z
	request_interval:             M1
	record_rows:                  118

	trade_log_len:                2
	USD:                          68548.64760470846
	JPY:                          0
	GBP:                          0

##### The information of account "Initial_Checkout_Review" has been successfully displayed. #####

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#### Displaying the READABLE trade log of account "dev_train_interface" (action: ALL) ####

		action_id:               0
		trade_time:              2019-01-01T22:30:00.000000000Z
		Trade Decision:          Sold 12.744200000000001 USD for 10 GBP (succeeded)
		Sell Currency Balance:   29987.2558 USD
		Buy Currency Balance:    30010 GBP


		action_id:               1
		trade_time:              2019-01-01T22:41:00.000000000Z
		Trade Decision:          Sold 15.69242840329541 GBP for 20 USD (succeeded)
		Sell Currency Balance:   29994.307571596706 GBP
		Buy Currency Balance:    30007.2558 USD


		action_id:               2
		trade_time:              2019-01-01T22:55:00.000000000Z
		Trade Decision:          Sold 0.21462297896694807 GBP for 30 JPY (succeeded)
		Sell Currency Balance:   29994.092948617737 GBP
		Buy Currency Balance:    30030 JPY


		action_id:               3
		trade_time:              2019-01-01T22:59:00.000000000Z
		Trade Decision:          Sold 5591.040000000001 JPY for 40 GBP (succeeded)
		Sell Currency Balance:   24438.96 JPY
		Buy Currency Balance:    30034.092948617737 GBP


		action_id:               4
		trade_time:              2019-01-01T23:02:00.000000000Z
		Trade Decision:          Sold 5482.9 JPY for 50 USD (succeeded)
		Sell Currency Balance:   18956.059999999998 JPY
		Buy Currency Balance:    30057.2558 USD


		action_id:               5
		trade_time:              2019-01-01T23:05:00.000000000Z
		Trade Decision:          Sold 0.547006053533659 USD for 60 JPY (succeeded)
		Sell Currency Balance:   30056.708793946465 USD
		Buy Currency Balance:    19016.059999999998 JPY


		action_id:               6
		trade_time:              2019-01-01T23:55:00.000000000Z
		Trade Decision:          Sold 70 USD for 7676.6900000000005 JPY (succeeded)
		Sell Currency Balance:   29986.708793946465 USD
		Buy Currency Balance:    26692.75 JPY


		action_id:               7
		trade_time:              2019-01-01T23:57:00.000000000Z
		Trade Decision:          Sold 109678000.0 JPY for 1000000 USD (failed)
		Sell Balance Protection: Trade unsuccessful as 26692.75 JPY is not enough for the sell
		Sell Currency Balance:   26692.75 JPY
		Buy Currency Balance:    29986.708793946465 USD


#### The READABLE trade log of account "dev_train_interface" has been successfully displayed (action: ALL) ####


##### Displaying information regarding account "dev_train_interface". #####

	record_from:                  2019-01-01T22:00:00.000000000Z
	record_to:                    2019-01-01T23:59:00.000000000Z
	request_interval:             M1
	record_rows:                  118

	trade_log_len:                8
	USD:                          29986.708793946465
	JPY:                          26692.75
	GBP:                          30034.092948617737

##### The information of account "dev_train_interface" has been successfully displayed. #####

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

##### Displaying information regarding account "End_Checkout_Review". #####

	record_from:                  2019-01-01T22:00:00.000000000Z
	record_to:                    2019-01-01T23:59:00.000000000Z
	request_interval:             M1
	record_rows:                  118

	trade_log_len:                10
	USD:                          68536.17872218802
	JPY:                          0.0
	GBP:                          0.0

##### The information of account "End_Checkout_Review" has been successfully displayed. #####
```