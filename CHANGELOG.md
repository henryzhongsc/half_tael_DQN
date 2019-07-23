# CHANGELOG

> This file serves as the journal for the [half_tael_DQN](https://github.com/choH/half_tael_DQN) project.

---
## Broadcast

### Tentative Goals for Scrum Meeting #2 on 2019-07-24
* **Goals**:
    * **Henry**
        * Implement trading interface.
        * Write user manual on such trading interface.
        * Draft version control standard and contribution guideline.
    * **Steven**
        * Run a trial DQN model on any `USD_JPY` file in [./dummy_data](https://github.com/choH/half_tael_DQN/tree/master/arena_data).
    * **Jian**
        * Help Steven on building the basic DQN model.
        * Quantified Anita's personality on trading behavior.
        * Research some high-end DQN structure and make a presentation.



### Upcoming Meetings:
* **2019-07-19 | Scrum | Henry, Jian, Steven** — Checkout **Meeting** section for details.


### 2019-07-10 | A short style guide for updating this `CHANGELOG.md`.
* The `CHANGELOG.md` has three sections.
    * **Broadcast**: Briefing of upcoming events or reminders (like this one).
    * **Meeting**: Summaries for meetings.
    * **Development Journal**: Records for development updates.
* For the sake of consistency, I suggest we update this `CHANGELOG.md` in a date descending order (new-to-old) with a headline format of `YYYY-MM-DD | Highlight | Name`. Note the `Highlight` and `Name` parts can be omitted if not applicable, e.g.
    * This broadcast headline, which omits `Name`.
    * Under **Development Journal** as `2019-04-10 | Henry Zhong`, which omits `Highlight`.

---
## Meeting

### 2019-07-26 | Scrum #3 | Henry, Jian, Steven
* **Goals**:
    * **Henry & Steve**
        * Integrate the trial DQN model with custom backend.
    * **Henry**
        * Finish basic DQN learning.

### 2019-07-24 | Scrum #2 | Henry, Jian, Steven


### 2019-07-19 | Scrum #1 | Henry, Steven
* **Goals**
    * **ALL**:
        * Get familiar with basic Q-learning and DQN concept in general.
    * **Henry**:
        * Build a basic wrapper to communicate with [OANDA](https://www.oanda.com/us-en/) API as the backend of the project. Anul's code [`Oanda_Trader.py`](placeholder) can be use as reference.
    * **Steven**:
        * Run a trial DQN model on ~~SP 500~~ [`USD_JPY_0.csv`](https://github.com/choH/half_tael_DQN/blob/master/dummy_data/USD_JPY_0.csv).
            * Task change due to CSV file of foreign exchange between USD and JPY is easily obtainable -- Henry.
    * **Jian**:
        * ~~Research and present some insight regarding the possible designs of DQN model.~~
        * Understand the concept of [Anita](https://www.graphen.ai/dev/anita/), and define a quantified standard for "trading personality" according to [Mapping Personality Traits to Investment Behavior (Revised)](https://github.com/choH/half_tael_DQN/blob/master/legacy_ref/anita/Mapping%20Personality%20Traits%20to%20Investment%20Behavior%20(Revised).pptx) and [Strategies and Metrics.xlsx](https://github.com/choH/half_tael_DQN/blob/master/legacy_ref/anita/Strategies%20and%20Metrics.xlsx)
            * Task change due to update form Dr. Lin regarding [Anita](https://www.graphen.ai/dev/anita/). As "trading bot with personalities" is the unique selling point of this project, we should only research in designs which are compatible with such idea. Thus we should quantify the concept of "trading personality" first -- Henry.


* **Review**
    * **Henry**
        * ✅ Delivered by [commit `ac4d217`](https://github.com/choH/half_tael_DQN/commit/ac4d21741ae3a7c45a16025de1a4b93b42891e39).
        * ❌ 🚧 Work-in-progress on DQN (**ALL**).
    * **Steven**
        * ❌ 🚧 Work-in-progress, will delivery by on 2019-07-24.
        * ✅ Basic DQN learned (**ALL**)
    * **Jian**
        * ~~❓ Absent for the day, will catch up on 2019-07-22 -- Henry.~~
        * ❌ 🚧 Work-in-progress, will delivery by on 2019-07-24.
        * ✅ Basic DQN learned (**ALL**)


### 2019-07-11 | Kick-off briefing | Anul Sinha, Henry, Jian, Steven
* Anul gave a presentation of his `forex` side-project, mainly regarding the method of interaction with OANDA, his model try-out, and why he abandoned this project.
* Due to the lacks of documentation of Anul's work, we decided to not to take over his project (also because he has moved on to a more combined design base on his `forex`), but to build our own bot. However, we will take his code as an important reference, especially regarding the OANDA API part and model environment setup.

---
## Development Journal

### 2019-07-23 | Implemented custom exceptions handling, and stand alone training input portal | Henry
* Now all input should goes to — or in a form which is similar to — `train_interface.py` with the login info saved in `config.py`
* Custom exceptions handling implemented, e.g.

```
During self.get_arena()
	<class 'trade_interface.OI_Onanda_Error'> is raised due to: {"errorMessage":"Insufficient authorization to perform request."}

During self.get_currency_pairs()
	<class 'trade_interface.TI_Account_Error'> is raised due to: No currency pair(s) between ('USD', 'JAY') from Oanda

During self.account_input_eval()
	<class 'trade_interface.TI_Account_Error'> is raised as: Invalid Oanda granularity input, self.request_interval: H20.

During self.account_input_eval()
	<class 'trade_interface.TI_Account_Error'> is raised as: Invalid account input, self.currency_balance['USD'] must be >= 0 (currently -10).

During self.market_LUT()
	<class 'trade_interface.TI_Market_LUT_Error'> is raised due to: Invalid time input: 2019-01-01T22:30:20.000000000Z

During self.execute_trade()
	<class 'trade_interface.TI_Market_LUT_Error'> is raised as: Time input: 2019-01-01T22:03:00.000000000Z returns np.nan

During self.execute_trade()
	<class 'trade_interface.TI_Execution_Error'> is raised as: USB or GBP is(are) not in ['USD', 'JPY', 'GBP']

During self.execute_trade()
	<class 'trade_interface.TI_Execution_Error'> is raised as: USD balance < 0 after trade action #0 (currently -127412000.00000001).

During self.execute_trade()
	<class 'trade_interface.TI_Execution_Error'> is raised as: _time 2019-01-01T22:29:00.000000000Z is earlier than pervious action's trade_time 2019-01-01T22:30:00.000000000Z in log.

During self.account_input_eval()
	<class 'trade_interface.TI_Account_Error'> is raised as: self.from_time 2019-01-01T00:00:00Z is earlier than self.to_time 2018-01-02T00:00:00Z.
```
* Add feature to retrieve one trade action by `action_id` from `trade_log`.


### 2019-07-22 | Fully supports trading among multiple currency | Henry
* Bug fixed for perviously mentioned [commit `#8248b6f`](https://github.com/choH/half_tael_DQN/commit/8248b6ff8fbd73be7c2fc52935574d90ea422b9f), trading among multiple currency is now fully supported ([commit `#443e4d1`](https://github.com/choH/half_tael_DQN/commit/443e4d16b9baf9f1c0d23cf85e7aaa3376fec320)).

```
##### Displaying information regarding account "dev_arena_test". #####

	record_from:                  2019-01-01T22:00:00.000000000Z
	record_to:                    2019-01-01T23:59:00.000000000Z
	request_interval:             M1
	record_rows:                  118

	trade_log_len:                7
	USD:                          49986.70879394646
	JPY:                          46692.75
	GBP:                          50034.09294861774

##### The information of account "dev_arena_test" has been successfully displayed. #####
```
* Support for `trade_unit_in_buy_currency` is implemented ([commit `#49e1f01`](https://github.com/choH/half_tael_DQN/commit/49e1f01f4834493fd37ac228fca689c67db7d6d9)).
* Readable `trade_log_review()` is implemented, now each trade action is expressed in natural language rather than pure JSON.

```
#### Displaying the READABLE trade log of account "dev_arena_test" ####
        ......
		action_id:               5
		trade_time:              2019-01-01T23:05:00.000000000Z
		Trade Decision:          Sold 0.547006053533659 USD for 60 JPY
		Sell Currency Balance:   50056.70879394646 USD
		Buy Currency Balance:    39016.06 JPY


		action_id:               6
		trade_time:              2019-01-01T23:55:00.000000000Z
		Trade Decision:          Sold 70 USD for 7676.6900000000005 JPY
		Sell Currency Balance:   49986.70879394646 USD
		Buy Currency Balance:    46692.75 JPY

#### The READABLE trade log of account "dev_arena_test" has been successfully displayed ####
```



### 2019-07-19 | Refactored trading interface to handle trading among multiple currency (Bug-fixing in progress) | Henry

* Refactored the `trade_interface.py` to handle multiple currency.
    * Bug on `market_LUT()` price retrive, see [commit `#8248b6f`](https://github.com/choH/half_tael_DQN/commit/8248b6ff8fbd73be7c2fc52935574d90ea422b9f).

```
The requested ARENA record has been successfully exported.

	file path:      ./arena_data/USD_JPY_GBP_2019-01-01T00:00:00_2019-01-02T00:00:00_M1.csv
	currency pair:  ['USD', 'JPY', 'GBP']
	from:           2019-01-01T00:00:00Z
	to:             2019-01-02T00:00:00Z
	interval:       M1
	total rows:     118
```
* Updated `oanda_interface.py` to wrap `DataFrame` return into a custom class `Oanda_Record`, so that when passed to other method info regarding such record shall preserve.
* Setting goals and time for next two scrum meetings.

### 2019-07-18 | Developed internal trading interface for model testing | Henry
* Developed a `Trade_Interface` class to regulate allowed trading behavior and review portal:
    * Behaviors: short, long.
    * Review: account, trade log.

```
Account dev_test is built.
	currency_A:                   USD
	currency_B:                   JPY
	record_from:                  2018-01-01T22:00:00.000000000Z
	record_to:                    2018-06-29T20:59:00.000000000Z
	currency_A_balance:           9987.859210202378
	currency_B_balance:           11364.3
	trade_log_len:                4
```
```
action_id:               0
			trade_time:              2018-01-01T22:02:00.000000000Z
			trade_type:              short
			trade_price:             112.676
			trade_currency:          JPY
			trade_unit:              2000
			currency_A_balance:      9982.249991124996
			currency_B_balance:      12000
```
* Marked places which can be improved in future (exception-handling, decorator log generation).

### 2019-07-17 | Developed wrapper functions output pricing record | Henry
* Developed a set of wrapper functions in `oanda_interface.py`, which can interact with `oandapyV20` API and output pricing record according to user requested currency pair, start time, end time, interval.
* Output is available in both `DataFrame` and CSV file with command line confirmation on both request and export stage:

```
REQUEST: v3/instruments/USD_JPY/candles InstrumentsCandles {'granularity': 'H1', 'includeFirst': True, 'from': '2018-01-01T00:00:00Z', 'to': '2018-01-21T20:00:00Z'}
REQUEST: v3/instruments/USD_JPY/candles InstrumentsCandles {'granularity': 'H1', 'includeFirst': True, 'from': '2018-01-21T20:00:00Z', 'to': '2018-02-11T16:00:00Z'}
...
REQUEST: v3/instruments/USD_JPY/candles InstrumentsCandles {'granularity': 'H1', 'includeFirst': True, 'from': '2018-12-21T04:00:00Z', 'to': '2018-12-31T23:59:59Z'}
```
```
The requested record has been successfully exported.
	file path:      ./dummy_data/USD_JPY_2018-01-01T00:00:00_2018-12-31T23:59:59_H1.csv
	currency pair:  USD_JPY
	from:           2018-01-01T00:00:00Z
	to:             2018-12-31T23:59:59Z
	interval:       H1
	total rows:     6217
```


* Experienced with [commit-message-emoji](https://github.com/dannyfritz/commit-message-emoji).

### 2019-07-11 | Finished Q-learning courses | Henry
* Finished the *Q-learning* section of the [Morvan](https://morvanzhou.github.io/tutorials/machine-learning/reinforcement-learning/) course.
* Started the DQN section.
* Hand over the pervious project to be fully committed on this one.