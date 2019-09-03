# half_tael_DQN
> A foreign exchange trading bot with quite some personalities, utilizing CNN + DQN with persona-driven adjustments.
>
> [📌 v4.5](https://github.com/choH/half_tael_DQN/releases/tag/v4.5) | 2019-09-02 | Refactor to work with Anita_v2.0 + Proper documentation.

---
A proper [`README.md`](https://github.com/choH/half_tael_DQN/blob/master/README.md) file will be written once the project is fully developed (or once reached a certain milestone). During the developing stage, records will be update on [`CHANGELOG.md`](https://github.com/choH/half_tael_DQN/blob/master/CHANGELOG.md).


---

## 1. Purpose
Named after [an unified currency of Qin dynasty](https://en.wikipedia.org/wiki/Ban_Liang), half_tael_DQN is aimed to be a foreign-exchange trading bot capable of trading among multiple currencies. Further, with the concept of [Anita](https://www.graphen.ai/dev/anita/), we expect such a bot to be able to generate trading strategies subject to different persona-driven adjustments — as an overly simplified example: to provide a more "aggressive" or a more "conservative" trading strategy.

## 2. Structure

half_tale_DQN is composite by three main blocks of code:
1. A **virtual trading platform** which capable of communicating through OANDA API to retrieve historical price data among different currencies, be able to register all virtual trading signals (buy & sell among any two-currency for a given value, etc), to generate a `trade_log`, and to track your account balance accordingly. A relatively thoughtful exception-handling system is implemented as well.
    * Constituted by [`oanda_interface.py`](https://github.com/choH/half_tael_DQN/blob/master/oanda_interface.py) and [`trade_interface.py`](https://github.com/choH/half_tael_DQN/blob/master/trade_interface.py).
    * To operate this virtual trading platform, check [🔰 User Manual for `trade_interface.py`](https://github.com/choH/half_tael_DQN/blob/master/demo_and_manual/User%20Manual%20for%20trade_interface.py.md). A standalone demo is also offered as [`train_interface_demo.py`](https://github.com/choH/half_tael_DQN/blob/master/demo_and_manual/train_interface_demo.py).
2. A **DQN model** with some kind of preprocess (currently CNN), capable of taking DataFrame with format like [./arena_data](https://github.com/choH/half_tael_DQN/tree/master/arena_data) as input and generates trade signals accordingly.
    * Constantly updating, currently as [./DQN_v3.0](https://github.com/choH/half_tael_DQN/tree/master/DQN_v3.0). Where `FX_env.py` defines the custom environment of foreign-exchange trading, `RL_brain.py` builds the logic of model, and `model_interface.py` runs the model buy integrating the former two together.
    * Other than the above three "core" files, [`model_config.py`](https://github.com/choH/half_tael_DQN/blob/master/model_config.py) and `train_interface.py` are provided as the configuration panel and the entry point of this program.
3. An **Anita** evaluator to influent the reward of a (or a set of) trade action(s) according to persona-driven adjustments.
    * Constituted by [`anita_interface.py`](https://github.com/choH/half_tael_DQN/tree/master/anita) along.
    * To operate this evaluator, check [🔰 User Manual for `anita_interface.py`](https://github.com/choH/half_tael_DQN/blob/master/demo_and_manual/User%20Manual%20for%20anita_interface.py.md).

## 3. Run

1. Register a *fxTrade Practice* account at [OANDA](https://www1.oanda.com/register/#/sign-up/demo). Then look up your `account_number` at [Manage Funds --> My Fund --> Account Summary --> v20 Account Number](https://www.oanda.com/demo-account/funding/); and obtain your OANDA's API token by visiting [Manage API Access --> Generate/Revoke](https://www.oanda.com/demo-account/tpa/personal_token).

2. Edit [`oanda_config.py`](https://github.com/choH/half_tael_DQN/blob/master/oanda_config.py) by assigning your account number and API token to `my_account_id` and `my_access_token` respectively (as `str`).


1. Edit [`model_config.py`](https://github.com/choH/half_tael_DQN/blob/master/model_config.py) with the desired parameters you'd like.


1. You can either identify a version of DQN model you'd like to run with, go into such folder (e.g. [./DQN_v3.0](https://github.com/choH/half_tael_DQN/tree/master/DQN_v3.0)), locate the `train_interace.py` file, then run against it within your IDE.

    Or in terminal, `cd` into the root folder of `half_tael_DQN`, identify the folder which contains your desired version of model, then:
    ```
    python3 model_version_folder/train_interace.py
    ```

    As for the example of [./DQN_v3.0](https://github.com/choH/half_tael_DQN/tree/master/DQN_v3.0), the command should be:
    ```
    python3 DQN_v3.0/train_interface.py  
    ```

## 4. Contribution

**To get involved, you are expected to uphold [`CONTRIBUTING.md`](https://github.com/choH/half_tael_DQN/blob/master/CONTRIBUTING.md).**

If you are from [Graphen.ai](https://www.graphen.ai) and want to carry on this project, you are recommended to branch out from tag [`v4.5`](https://github.com/choH/half_tael_DQN/releases/tag/v4.5) like:
```
git checkout -b your_branch_name v4.5
```
Since later version of half_tael_DQN might detach the [Anita](https://github.com/choH/half_tael_DQN/tree/master/anita) evaluator as it is a property of Graphen.ai.


## 5. Limitations

Though published, this is my ([@choH](https://github.com/choH)) first semi-serious project and also my first exposure to AI. Thus, a lot of works here were done in a premature way. The project is published more for the purpose of exhibition and ease of future development — **please use it with caution**.

Known limitations of this project include but not limited to:

1. Only be able to register trade signals within the virtual trading platform, but not able to submit real trade request to OANDA.
* Only a very simple CNN is implemented as preprocess method to handle multiple currencies (>2) as input — since there will be multiple price data on every timestamp — and the benchmark is not exactly appealing.
* Only a simple double DQN is implemented as model.
* Only a very basic method is implemented for `Anita_Trait`.
* Lack of visualization, as the `cost_log` is the only graphical output of this model.

**Check out [Issue #22](https://github.com/choH/half_tael_DQN/issues/22) for potential improvements for this project.**


---

## 6. Acknowledgements

* Henry ZHONG ([@choH](https://github.com/choH))
    * Responsible for project management.
    * Developed the Virtual Trading Platform.
    * Developed the DQN model after commit [`ef6e716`](https://github.com/choH/half_tael_DQN/commit/ef6e716af132541a0720bcb456f602c4f13cba06) (the origin of [DQN_v2.5](https://github.com/choH/half_tael_DQN/tree/master/legacy_ref/legacy_DQN/DQN_v2.5)).
    * Refactored DQN models to work with the Virtual Trading Platform.
    * Developed a demonstrative Anita framework.

* Steven XING ([@lx72](https://github.com/lx72))
    * Developed [DQN_v1.0](https://github.com/choH/half_tael_DQN/tree/master/legacy_ref/legacy_DQN/DQN_v1.0) and [DQN_v2.0](https://github.com/choH/half_tael_DQN/tree/master/legacy_ref/legacy_DQN/DQN_v2.0).
    * Partially developed [DQN_v2.5](https://github.com/choH/half_tael_DQN/tree/master/legacy_ref/legacy_DQN/DQN_v2.5).
    * Exited the project after commit [`ef6e716`](https://github.com/choH/half_tael_DQN/commit/ef6e716af132541a0720bcb456f602c4f13cba06).


## 7. License

[CC BY-NC 2.0](https://github.com/choH/half_tael_DQN/blob/master/LICENSE.md)

