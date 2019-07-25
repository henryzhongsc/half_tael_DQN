# half_tael_DQN
> A foreign exchange trading bot with quite some personalities, utilizing DQN+RNN with persona-driven adjustments.

---
A proper [`README.md`](https://github.com/choH/half_tael_DQN/blob/master/README.md) file will be written once the project is fully developed (or once reached a certain milestone). During the developing stage, records will be update on [`CHANGELOG.md`](https://github.com/choH/half_tael_DQN/blob/master/CHANGELOG.md).

To get involved, you are expected to uphold [`CONTRIBUTING.md`](https://github.com/choH/half_tael_DQN/blob/master/CONTRIBUTING.md).

---
# Tentative Goals for Scrum Meeting #3 on 2019-08-02.
* **Henry**
    1. Draft version control standard and contribution guideline (2019-07-26).
    * Finish basic DQN learning.
* **Steven**
    1. Document the two-currency DQN model (2019-07-26).
* **Jian**
    1. Develop a set of evaluation functions to evaluate the status (weight) of certain metrics introduced in [Anita folder](https://github.com/choH/half_tael_DQN/tree/master/legacy_ref/anita).
        * Such functions should take `_time`, `_currency_pair`, `_volume`, `trade_action` (long, short, hold) and any other necessary parameters (e.g. historical `trade_log`) as inputs and return a `float` number between `-1` to `1` as a reflection of the status of such metrics at this particular position.

        * Sample data as:
            * [USD_JPY_GBP_2017-01-01T00:00:00_2018-01-01T00:00:00_M5.csv](https://github.com/choH/half_tael_DQN/blob/master/arena_data/USD_JPY_GBP_2017-01-01T00:00:00_2018-01-01T00:00:00_M5.csv) (74,277 rows).
            * If the above data is too huge , you may always refer to [USD_JPY_GBP_2019-01-01T00:00:00_2019-02-01T00:00:00_M5.csv](https://github.com/choH/half_tael_DQN/blob/master/arena_data/USD_JPY_GBP_2019-01-01T00:00:00_2019-02-01T00:00:00_M5.csv) as a lightweight alternative (6,358 rows).

# Tentative Goals for Scrum Meeting #4 on 2019-07-30.
* **Henry**
    1. Integrate Steven's trial DQN model (two-currency) with Henry's custom virtual trading platform.
* **Steven**
    1. Refactor his trial DQN model as DQN+RNN, present a runnable demo.
        1. Support trading among multiple (>2) currencies.
        * Implement RNN design with DQN..
        * Research about the possibility of using `vector` as first layer nodes in RNN design.

    * Sample data as:
        * Train: [USD_JPY_GBP_2017-01-01T00:00:00_2018-01-01T00:00:00_M5.csv](https://github.com/choH/half_tael_DQN/blob/master/arena_data/USD_JPY_GBP_2017-01-01T00:00:00_2018-01-01T00:00:00_M5.csv) (74,277 rows).
        * Test: [USD_JPY_GBP_2018-01-01T00:00:00_2019-01-01T00:00:00_M5.csv](https://github.com/choH/half_tael_DQN/blob/master/arena_data/USD_JPY_GBP_2018-01-01T00:00:00_2019-01-01T00:00:00_M5.csv) (74,590 rows).
        * Lightweight trial data for development: [USD_JPY_GBP_2019-01-01T00:00:00_2019-02-01T00:00:00_M5.csv](https://github.com/choH/half_tael_DQN/blob/master/arena_data/USD_JPY_GBP_2019-01-01T00:00:00_2019-02-01T00:00:00_M5.csv) (6,358 rows).




---
## Purpose of this Project.

## UI Showcase & Demo.

## User Manuel.

## Vision for Future.

## Acknowledgements.

