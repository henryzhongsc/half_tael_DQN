# CHANGELOG

> This file serves as the journal for the [half_tael_DQN](https://github.com/choH/half_tael_DQN) project.

---
## Broadcast

### Tentative Goals for Scrum Meeting 2019-07-19
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

### 2019-07-19 | Scrum | Henry, Jian, Steven
* Placeholder



### 2019-07-11 | Kick-off briefing | Anul Sinha, Henry, Jian, Steven
* Anul gave a presentation of his `forex` side-project, mainly regarding the method of interaction with OANDA, his model try-out, and why he abandoned this project.
* Due to the lacks of documentation of Anul's work, we decided to not to take over his project (also because he has moved on to a more combined design base on his `forex`), but to build our own bot. However, we will take his code as an important reference, especially regarding the OANDA API part and model environment setup.

---
## Development Journal

### 2019-7-17 | Developed wrapper functions output pricing record | Henry
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

### 2019-07-11 | Finished Q-learning courses | Henry
* Finished the *Q-learning* section of the [Morvan](https://morvanzhou.github.io/tutorials/machine-learning/reinforcement-learning/) course.
* Started the DQN section.
* Hand over the pervious project to be fully committed on this one.