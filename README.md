# half_tael_DQN
> To automate foreign exchange trading by utilizing the deep Q-network.

---
A proper `README.md` file will be written once the project is fully developed. During the developing stage, the records will be update on [`CHANGELOG.md`](https://github.com/choH/half_tael_DQN/blob/master/CHANGELOG.md).

---
# Tentative Goals for Scrum Meeting #3 on 2019-07-26.
* **Henry & Steven**
    1. Integrate Steven's trial DQN model with Henry's custom virtual trading platform.
* **Henry**
    1. Finish basic DQN learning.
* **Steven**
    1. Refactor his trial DQN model to support trading among multiple currencies (data input as: [`USD_JPY_GBP_2018-01-01T00:00:00_2019-01-01T00:00:00_M5.csv`](https://github.com/choH/half_tael_DQN/blob/master/arena_data/USD_JPY_GBP_2018-01-01T00:00:00_2019-01-01T00:00:00_M5.csv)).
    * Research about the possibility of using `vector` as first layer nodes in ANN/RNN design.

# Tentative Goals for Scrum Meeting #4 on 2019-07-30.
* **Jian**
    1. Develop a set of evaluation functions to evaluate the status (weight) of certain metrics introduced in [Anita folder](https://github.com/choH/half_tael_DQN/tree/master/legacy_ref/anita).
        1. Such functions should take `_time`, `_currency_pair`, `_volume` and any other necessary parameters as inputs and return a `float` number between `-1` to `1` as a reflection of the status of such metrics at this particular position.
        2. Sample data is available at: [`USD_JPY_GBP_2018-01-01T00:00:00_2019-01-01T00:00:00_M5.csv`](https://github.com/choH/half_tael_DQN/blob/master/arena_data/USD_JPY_GBP_2018-01-01T00:00:00_2019-01-01T00:00:00_M5.csv)



---
## Purpose of this Project.

## UI Showcase & Demo.

## User Manuel.

## Vision for Future.

## Acknowledgements.

