# half_tael_DQN
> To automate foreign exchange trading by utilizing the deep Q-network.

---
A proper `README.md` file will be written once the project is fully developed. During the developing stage, the records will be update on [`CHANGELOG.md`](https://github.com/choH/half_tael_DQN/blob/master/CHANGELOG.md).

---
### Tentative Goals for Scrum Meeting #3 on 2019-08-02
* **Henry**
    1. Draft version control standard and contribution guideline (2019-07-26).
    * Finish basic DQN learning.
* **Steven**
    1. Document the two-currency DQN model (2019-07-26).
* **Jian**
    1. Develop a set of evaluation functions to evaluate the status (weight) of certain metrics introduced in [Anita folder](https://github.com/choH/half_tael_DQN/tree/master/legacy_ref/anita).
        * Such functions should take `_time`, `_currency_pair`, `_volume` and any other necessary parameters as inputs and return a `float` number between `-1` to `1` as a reflection of the status of such metrics at this particular position.
        * Sample data is available at: [`USD_JPY_GBP_2018-01-01T00:00:00_2019-01-01T00:00:00_M5.csv`](https://github.com/choH/half_tael_DQN/blob/master/arena_data/USD_JPY_GBP_2018-01-01T00:00:00_2019-01-01T00:00:00_M5.csv)

# Tentative Goals for Scrum Meeting #4 on 2019-07-30.
* **Henry**
    1. Integrate Steven's trial DQN model (two-currency) with Henry's custom virtual trading platform.
* **Steven**
    1. Refactor his trial DQN model as DQN+RNN, present a runnable demo.
        * To support trading among multiple (>2) currencies. Data input as: [`USD_JPY_GBP_2018-01-01T00:00:00_2019-01-01T00:00:00_M5.csv`](https://github.com/choH/half_tael_DQN/blob/master/arena_data/USD_JPY_GBP_2018-01-01T00:00:00_2019-01-01T00:00:00_M5.csv).
        * Research about the possibility of using `vector` as first layer nodes in RNN design.




---
## Purpose of this Project.

## UI Showcase & Demo.

## User Manuel.

## Vision for Future.

## Acknowledgements.

