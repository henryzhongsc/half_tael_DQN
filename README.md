# half_tael_DQN
> A foreign exchange trading bot with quite some personalities, utilizing DQN with persona-driven adjustments.
>
> 📌 v1.0 | 2019-07-26 | Trading platform and trial DQN (two currencies) done.

---
A proper [`README.md`](https://github.com/choH/half_tael_DQN/blob/master/README.md) file will be written once the project is fully developed (or once reached a certain milestone). During the developing stage, records will be update on [`CHANGELOG.md`](https://github.com/choH/half_tael_DQN/blob/master/CHANGELOG.md).

To get involved, you are expected to uphold [`CONTRIBUTING.md`](https://github.com/choH/half_tael_DQN/blob/master/CONTRIBUTING.md).

---

# Tentative Goals for Scrum Meeting #4 on 2019-08-02.
* **Henry**
    1. Integrate Steven's trial DQN model (two-currency) with Henry's custom virtual trading platform.
* **Steven**
    1. Refactor his trial DQN with model improvement, present a runnable demo.
        1. Support trading among multiple (>2) currencies.
        * Implement a model design which understand the relation between timeframe.
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

