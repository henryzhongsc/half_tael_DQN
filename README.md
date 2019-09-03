# half_tael_DQN
> A foreign exchange trading bot with quite some personalities, utilizing DQN with persona-driven adjustments.
>
> [📌 v4.0](https://github.com/choH/half_tael_DQN/releases/tag/v4.0) | 2019-08-24 | DQN_v3.0 with improved cohesion, textual output, and documentation.

---
A proper [`README.md`](https://github.com/choH/half_tael_DQN/blob/master/README.md) file will be written once the project is fully developed (or once reached a certain milestone). During the developing stage, records will be update on [`CHANGELOG.md`](https://github.com/choH/half_tael_DQN/blob/master/CHANGELOG.md).

To get involved, you are expected to uphold [`CONTRIBUTING.md`](https://github.com/choH/half_tael_DQN/blob/master/CONTRIBUTING.md).

---

## Purpose
Named after [an unified currency of Qin dynasty](https://en.wikipedia.org/wiki/Ban_Liang), half_tael_DQN is aimed to become a foreign-exchange trading bot capable of trading among multiple currencies. Further, with the concept of [Anita](https://www.graphen.ai/dev/anita/), we expect such a bot to be able to generate trading strategies subject to different persona-driven adjustments — as an oversimplified example, to provide a more "aggressive" or more "conservative" trading strategy.

## Structure

half_tale_DQN is composite by three main blocks of code:
1. A **virtual trading platform** which capable of communicating through OANDA API to retrieve historical price data among different currencies, be able to register all virtual trading signals (buy, sell, etc), to generate a `trade_log`, and to track your account balance accordingly.
    * Constituted by [`oanda_interface.py`](https://github.com/choH/half_tael_DQN/blob/master/oanda_interface.py) and [`trade_interface.py`](https://github.com/choH/half_tael_DQN/blob/master/trade_interface.py).
    * To operate this virtual trading platform, check [🔰 User Manual for `trade_interface.py`](https://github.com/choH/half_tael_DQN/blob/master/demo_and_manual/User%20Manual%20for%20%60trade_interface.py%60.md).
2. A **DQN model** with some kind of preprocess (currently CNN), capable of taking DataFrame with format like [./arena_data](https://github.com/choH/half_tael_DQN/tree/master/arena_data) as input and generates trade signals accordingly.
    * Constantly updating, currently as [./DQN_v3.0](https://github.com/choH/half_tael_DQN/tree/master/DQN_v3.0). Where `FX_env.py` defines the custom environment of foreign-exchange trading, `RL_brain.py` builds the logic of model, and `model_interface.py` runs the model buy integrating the upper two together.
3. An **Anita** evaluator to influent the reward of trade actions.
    * Constituted by
    * To operate this evaluator, check

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
as later version of half_tael_DQN might detach the [Anita](https://github.com/choH/half_tael_DQN/tree/master/anita) evaluator as it is a property of Graphen.ai.


## Limitation

Though published, this is my first semi-serious project and also my first exposure to AI. Thus, a lot of works were done in a premature way. The project is published more for the purpose of exhibition and ease of future development, please use it with caution.

* Only be able to register trade signals within the virtual trading platform, but not able to submit real trade request to OANDA.
* Only a very simple CNN is implemented as preprocess method to handle multiple currencies (>2) as input — since there will be multiple price data on every timestamp — and the benchmark is not exactly appealing.
* Only a simple double DQN is implemented as model.
* Only a very basic Anita `traits_factor` — if trade too frequently (amount of non hold trade_actions > 50% of `n_features`) — is implemented.
* Lack of visualization, as the `cost_log` is the only graphical output of this model.

**Check out [Issue #22](https://github.com/choH/half_tael_DQN/issues/22) for the future vision of this project.**

## Acknowledgements

* Henry ZHONG ([@choH](https://github.com/choH))
    * Responsible for project management.
    * Developed the Virtual Trading Platform
    * Updating the DQN model after commit [`ef6e716`](https://github.com/choH/half_tael_DQN/commit/ef6e716af132541a0720bcb456f602c4f13cba06) (the origin of [DQN_v2.5](https://github.com/choH/half_tael_DQN/tree/master/legacy_ref/legacy_DQN/DQN_v2.5)).
    * Developed Anita framework with a demonstrative `traits_factor` implemented.

* Steven XING ([@lx72](https://github.com/lx72))
    * Developed [DQN_v1.0](https://github.com/choH/half_tael_DQN/tree/master/legacy_ref/legacy_DQN/DQN_v1.0), [DQN_v2.0](https://github.com/choH/half_tael_DQN/tree/master/legacy_ref/legacy_DQN/DQN_v2.0), and partially developed [DQN_v2.5](https://github.com/choH/half_tael_DQN/tree/master/legacy_ref/legacy_DQN/DQN_v2.5).
    * Exited the project after commit [`ef6e716`](https://github.com/choH/half_tael_DQN/commit/ef6e716af132541a0720bcb456f602c4f13cba06).


## License

[CC BY-NC 2.0](https://github.com/choH/half_tael_DQN/blob/master/LICENSE.md)