# CHANGELOG

> This file serves as the journal for the [half_tael_DQN](https://github.com/choH/half_tael_DQN) project.

---
## Broadcast


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

### 2019-09-02 | Scrum #11 | Henry (final delivery for Graphen.ai).\
* **Henry**
    1. ✅ Developed [Anita v2.0: Basic framework for persona-driven reward influencing interface](https://github.com/choH/half_tael_DQN/milestone/4).
    2. ✅ Accomplished everything in the [half_tael_v4.5: Refactor to work with Anita_v2.0 + Proper documentation](https://github.com/choH/half_tael_DQN/milestone/8).
    3. ✅ Released [half_tael_DQN v4.5](https://github.com/choH/half_tael_DQN/releases/tag/v4.5).


### 2019-08-25 | Scrum #10 | Henry (end-of-internship review).
* **Henry**
    1. ✅ Release [half_tael_DQN v3.0: Virtual Trading Platform with DQN v3.0](https://github.com/choH/half_tael_DQN/releases/tag/v3.0).
        * Accomplished everything in the [related milestone](https://github.com/choH/half_tael_DQN/milestone/5).
        * Works presented as [half_tael_DQN v3.0: Virtual Trading Platform with DQN v3.0](https://github.com/choH/half_tael_DQN/releases/tag/v3.0).
    2. ✅ Release [half_tael_v4.0: Textual output + Improved cohesion + Documentations](https://github.com/choH/half_tael_DQN/releases/tag/v4.0).
        * Accomplished everything in the [related milestone](https://github.com/choH/half_tael_DQN/milestone/6).
        * Works presented as [DQN_v3.0 with improved cohesion, textual output, and documentation](https://github.com/choH/half_tael_DQN/releases/tag/v3.0).
    3. ❌ 🚧 Develop [Anita v2.0: Basic framework for persona   -driven reward influencing interface](https://github.com/choH/half_tael_DQN/milestone/4).

### 2019-08-16 | Scrum #9 | Henry (report to Ching-Yung Lin and Oscar Tseng).
* **Henry**
    1. ✅ Bugfix [cost (loss) graph converges way too quick and smooth.](https://github.com/choH/half_tael_DQN/issues/15).


### 2019-08-14 | Scrum #8 | Henry.
* **Henry**
    1. ✅ 🚧 Refactor half_tael_v2.0 to v3.0, in compliant with DQN_v2.5 (multiple currency model working with the trading platform).
        * Delivered a runnable demo with certain freedom on params (`3` price info at the same timestamp.
        * Bugfix required on [cost (loss) graph converges way too quick and smooth.](https://github.com/choH/half_tael_DQN/issues/15).
    2. ~~Anita v2.0~~
        * Postponed as legacy Anita is unusable, check **2019-08-08 | Legacy Anita plot hole discovered | Henry** in section **Development Journal** for details.

### 2019-08-12 | Scrum #7 | Henry, Steven.
* **Henry**
    1. ✅ Test the reward design (for Anita).
    2. ~~Anita v2.0~~
        * Postponed due to prioritized on debugging DQN v2.5.
    3. ✅ DQN v2.5: Debugged and partially adjusted the CNN + DQN model which supports multiple (>2) currencies based on Steven X.'s design ([ef6e716](https://github.com/choH/half_tael_DQN/commit/ef6e716af132541a0720bcb456f602c4f13cba06)). Presented a runnable demo only on [a specific dummy data set](https://github.com/choH/half_tael_DQN/tree/v2.0/DQV_v2.5/EUR_GBP.csv) -- Henry.
        * Main works presented as [f7259b3](https://github.com/choH/half_tael_DQN/commit/f7259b3eff2cf9e0d9886ea613d87bee958bdb68). Stored as [DQN_v2.5](https://github.com/choH/half_tael_DQN/tree/v2.0/master/DQN_v2.5).

* **Steven**
    1. ✅ DQN v2.5: Research and redesigned [DQN_v1.0](https://github.com/choH/half_tael_DQN/tree/v1.0/trial_DQN) as [DQN_v2.5](https://github.com/choH/half_tael_DQN/tree/v2.0/master/DQN_v2.5) to support multiple (>2) currencies using a CNN + DQN structure.
        * Works presented as [ef6e716](https://github.com/choH/half_tael_DQN/commit/ef6e716af132541a0720bcb456f602c4f13cba06). Need debug.
        * Absent, but marked as "green check" since goal (DQN v2.5) accomplished -- Henry.

### 2019-08-07 | Scrum #6 | Henry, Steven.
* **Henry**
    1. ✅ Understand CNN basic.
* **Steven**
    1. ✅ Fully understand the basic of CNN as in the relationship between `w_1`, `b_1`, `n_features`, and input `data_env`
    * ❌ 🚧 DQN v2.5.
        * Postpone to 2019-08-09, but made significant progress on understanding the mapping of matrix convolution.

### 2019-08-06 | Scrum #5 | Henry, Steven.
* ~~Steven absent, postpone to 2019-08-06 to discuss DQN v2.5.~~
* ❌ 🚧 DQN v2.5.
    * Tried to utilize CNN to scan input with multiple dimension (support trading among multiple (>2) currencies). But it is indeed technically challenged since:
        * The original DQN v1.0 (and also DQN v2.0) was built on a modification of Morvan's environment, which only considered one-dimensional input.
        * There aren't too much readable TensorFlow CNN+DQN source code we can referenced on. And it will forgo a serious portion of work on DQN v1.0 and v2.0 if we want to redesign our environment base on another project.
    * Resolution: Steven will try to deliver his demo by Scrum #6 (2019-08-07). If not, we will shift focus from Morvan to another tutorial and redesign the environment. We want to stick with Morvan if possible as DQN v2.0 is fully developed, but as the reward part is relatively stand-alone from DQN v1.0 but more coupled to the trading platform (which is fully developed and will keep using), the cost is still acceptable as long as we can quickly implement the transformation code to change the environment from pixel games to numerical forex market. Potential reference include:
        * [reinforcement-learning/DQN](https://github.com/dennybritz/reinforcement-learning/tree/master/DQN)
        * [https://www.datahubbs.com/deepmind-dqn/](https://www.datahubbs.com/deepmind-dqn/)
        * [Using Keras and Deep Q-Network to Play FlappyBird | Ben Lau](https://yanpanlau.github.io/2016/07/10/FlappyBird-Keras.html)
        * [Beat Atari with Deep Reinforcement Learning! (Part 1: DQN)](https://becominghuman.ai/lets-build-an-atari-ai-part-1-dqn-df57e8ff3b26)
        * [floodsung/DQN-Atari-Tensorflow](https://github.com/floodsung/DQN-Atari-Tensorflow)
        * With LSTM:
            * [附：强化学习——DRQN分析详解 | ECKai](https://zhuanlan.zhihu.com/p/54898904)
            * [论文笔记之：Deep Recurrent Q-Learning for Partially Observable MDPs | uuummmmiiii](https://zhuanlan.zhihu.com/p/37294342)
            * [Deep Recurrent Q-Learning for Partially Observable MDPs | Matthew Hausknecht, Peter Stone](https://arxiv.org/abs/1507.06527v3)

### 2019-08-02 | Scrum #4 | Henry, Steven.
* **Goal**
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
* **Review**
    * **Henry**
        1. ✅ Delivered as [DQN_v2.0 Folder](https://github.com/choH/half_tael_DQN/tree/half_tael_v2.0/DQN_v2.0) by [commit `#6a051da`](https://github.com/choH/half_tael_DQN/commit/6a051dab9e63ec483e97f8b39b5fe6e1d5910e3f). Check [milestone #2](https://github.com/choH/half_tael_DQN/milestone/2).
    * **Steven**
        2. ❌ 🚧 Work in progress as required to set up with server, will deliver on 2019-08-05. Check [milestone #3](https://github.com/choH/half_tael_DQN/milestone/3)


### 2019-07-30 | Scrum #3 | Henry, Steven, Jian.
* **Goals**
    * **Henry**
        1. Draft version control standard and contribution guideline (2019-07-26).
        * Finish basic DQN learning.
    * **Steven**
        2. Document the two-currency DQN model (2019-07-26).
    * **Jian**
        3. Develop a set of evaluation functions to evaluate the status (weight) of certain metrics introduced in [Anita Folder](https://github.com/choH/half_tael_DQN/tree/master/legacy_ref/anita).
            * Such functions should take `_time`, `_currency_pair`, `_volume`, `trade_action` (long, short, hold) and any other necessary parameters (e.g. historical `trade_log`) as inputs and return a `float` number between `-1` to `1` as a reflection of the status of such metrics at this particular position.

            * Sample data as:
                * [USD_JPY_GBP_2017-01-01T00:00:00_2018-01-01T00:00:00_M5.csv](https://github.com/choH/half_tael_DQN/blob/master/arena_data/USD_JPY_GBP_2017-01-01T00:00:00_2018-01-01T00:00:00_M5.csv) (74,277 rows).
                * If the above data is too huge , you may always refer to [USD_JPY_GBP_2019-01-01T00:00:00_2019-02-01T00:00:00_M5.csv](https://github.com/choH/half_tael_DQN/blob/master/arena_data/USD_JPY_GBP_2019-01-01T00:00:00_2019-02-01T00:00:00_M5.csv) as a lightweight alternative (6,358 rows).
* **Review**
    * **Henry**
        1. ✅ Delivered as [`CONTRIBUTING.md`](https://github.com/choH/half_tael_DQN/blob/master/CONTRIBUTING.md) by [commit `#dd7e0ce`](https://github.com/choH/half_tael_DQN/commit/dd7e0ce97c59fd023e22cda412bf0aa8ba18a44f).
        2. ✅ Finished most DQN part. Check [issue #2](https://github.com/choH/half_tael_DQN/issues/2).
    * **Steven**
        3. ✅ Delivered as [trial_DQN_doc.docx](https://github.com/choH/half_tael_DQN/blob/half_tael_v2.0/demo_and_manual/trial_DQN_doc.docx) by [commit `#2b10528`](https://github.com/choH/half_tael_DQN/commit/2b105286c2d6aed95595cbcfb605390e1bab92c3). Check [issue #1](https://github.com/choH/half_tael_DQN/issues/1).
            * Absent due to sickness, showed up and discussed on 2019-08-01.
    * **Jian**
        1. ✅ Delivered a bunch of file in [anita_v1.1 folder](https://github.com/choH/half_tael_DQN/tree/anita_v1.1/anita_v1.1) by [commit `#90fd3c0`](https://github.com/choH/half_tael_DQN/commit/90fd3c0e38bdc56d32045a0467c31e8659a54dc5), [commit `#4e93d2b`](https://github.com/choH/half_tael_DQN/commit/4e93d2b937c3b049e93e99dffa72384da46e0e9f), and [commit `#d9bd1aa`](https://github.com/choH/half_tael_DQN/commit/d9bd1aaf1c0757c660d70797643020aeaee8f4d2).
            * ❓ QA not yet performed. Will update [milestone #1](https://github.com/choH/half_tael_DQN/milestone/1) once performed.
            * Absent due to interview conflict, not yet showed up.



### 2019-07-24 | Scrum #2 | Henry, Jian, Steven.
* **Goals**:
    * **Henry**
        1. Implement trading interface.
        * Write user manual on such trading interface.
        * Draft version control standard and contribution guideline.
    * **Steven**
        1. Run a trial DQN model on any `USD_JPY` file in [./dummy_data](https://github.com/choH/half_tael_DQN/tree/master/arena_data).
    * **Jian**
        1. Help Steven on building the basic DQN model.
        * Quantified Anita's personality on trading behavior.
        * Research some high-end DQN structure and make a presentation.

* **Review**
    * **Henry**
        1. ✅ [`trade_interface.py`](https://github.com/choH/half_tael_DQN/blob/master/trade_interface.py) fully developed by [commit `#5d86b5d`](https://github.com/choH/half_tael_DQN/commit/5d86b5dfb5547ca807544dbb449e54f8dadebf14).
        * ✅ Available as:
            * Demo code delivered by [commit `#5a62409`](https://github.com/choH/half_tael_DQN/commit/5a62409a1ea16b7762c9431eb75c67a4afc44f22)
            * User manual delivered by [commit `#042ef13`](https://github.com/choH/half_tael_DQN/commit/042ef13b1e1b8f43e1cdc1af90a639de7f70b40d)
        * ❌ *Version control standard and contribution guideline* postpone to 2019-07-25.

    * **Steven**
        1. ✅ Trial DQN is runnable, will commit after Henry's *version control standard and contribution guideline* becomes available.
    * **Jian**
        1. ☑️ Trial DQN is a solo work done by Steven, however Jian did implemented a Cartpole demo.
        * ❌ Did not delivery as Jian believes it is not feasible to do it stand-alone (without the DQN code).
            * After discussion, we all agree it is doable and such task is postpone to 2019-07-30.
        * ✅ Introduced some fundamental DQN features (remember, replay).

### 2019-07-19 | Scrum #1 | Henry, Steven.
* **Goals**
    * **ALL**:
        1. Get familiar with basic Q-learning and DQN concept in general.
    * **Henry**:
        1. Build a basic wrapper to communicate with [OANDA](https://www.oanda.com/us-en/) API as the backend of the project. Anul's code [`Oanda_Trader.py`](placeholder) can be use as reference.
    * **Steven**:
        1. Run a trial DQN model on ~~SP 500~~ [`USD_JPY_0.csv`](https://github.com/choH/half_tael_DQN/blob/master/dummy_data/USD_JPY_0.csv).
            * Task change due to CSV file of foreign exchange between USD and JPY is easily obtainable -- Henry.
    * **Jian**:
        1. ~~Research and present some insight regarding the possible designs of DQN model.~~
        * Understand the concept of [Anita](https://www.graphen.ai/dev/anita/), and define a quantified standard for "trading personality" according to [Mapping Personality Traits to Investment Behavior (Revised)](https://github.com/choH/half_tael_DQN/blob/master/legacy_ref/anita/Mapping%20Personality%20Traits%20to%20Investment%20Behavior%20(Revised).pptx) and [Strategies and Metrics.xlsx](https://github.com/choH/half_tael_DQN/blob/master/legacy_ref/anita/Strategies%20and%20Metrics.xlsx)
            * Task change due to update form Dr. Lin regarding [Anita](https://www.graphen.ai/dev/anita/). As "trading bot with personalities" is the unique selling point of this project, we should only research in designs which are compatible with such idea. Thus we should quantify the concept of "trading personality" first -- Henry.


* **Review**
    * **All**
        * **Henry**: ❌ 🚧 Work-in-progress on DQN.
        * **Steven**: ✅ Basic DQN learned.
        * **Jian**: ✅ Basic DQN learned
    * **Henry**
        1. ✅ Delivered by [commit `ac4d217`](https://github.com/choH/half_tael_DQN/commit/ac4d21741ae3a7c45a16025de1a4b93b42891e39).

    * **Steven**
        2. ❌ 🚧 Work-in-progress, will delivery by on 2019-07-24.
    * **Jian**
        1. ~~❓ Absent for the day, will catch up on 2019-07-22 -- Henry.~~
            * ❌ 🚧 Work-in-progress, will deliver by on 2019-07-24.



### 2019-07-11 | Kick-off briefing | Anul Sinha, Henry, Jian, Steven.
* Anul gave a presentation of his `forex` side-project, mainly regarding the method of interaction with OANDA, his model try-out, and why he abandoned this project.
* Due to the lacks of documentation of Anul's work, we decided to not to take over his project (also because he has moved on to a more combined design base on his `forex`), but to build our own bot. However, we will take his code as an important reference, especially regarding the OANDA API part and model environment setup.

---
## Development Journal

### 2019-09-02 | half_tael_DQN v4.5 release | Henry.
* Update [`CHANGELOG.md`](https://github.com/choH/half_tael_DQN/blob/master/CHANGELOG.md) and [🔰 User Manual for `anita_interface.py`](https://github.com/choH/half_tael_DQN/blob/master/demo_and_manual/User%20Manual%20for%20anita_interface.py.md).
* Remove (and regenerate to discard the published one) OANDA credential.
* Fix command line instruction mistake in [README.md](https://github.com/choH/half_tael_DQN/blob/master/README.md) *Run* section.
* Update [`README.md`](https://github.com/choH/half_tael_DQN/blob/master/README.md) with information regarding anita_v2.0.
* Bugfix log output directory — and also raw_data folder? — not exist issue (with `mkdir`).
* Provide a `Trade_Interface config` input with longer time duration.
* Generate dynamic `action_list` base on input account currencies (`self.TI_train.all_currency_list`).

### 2019-08-29 | anita_v2.0 code portion done | Henry.
* Coded [anita_v2.0](https://github.com/choH/half_tael_DQN/blob/anita_v2.0/anita/anita_interface.py).
    * Code mainly delivered as commit [`c4aece1`](https://github.com/choH/half_tael_DQN/commit/c4aece134ae937f96fb0ca64faa3736ca76dd4a6) and [`e9fdf04`](https://github.com/choH/half_tael_DQN/commit/e9fdf042078ad0a3cc653cac712723458868e089).
    * A "first-draft" [user manual for `anita_interface.py`](https://github.com/choH/half_tael_DQN/blob/anita_v2.0/demo_and_manual/User%20Manual%20for%20anita_interface.py.md) is also written by [`f73a207`](https://github.com/choH/half_tael_DQN/commit/f73a207e5f0e8ff7db64bcdbdd4bb66a9885e7f5)
### 2019-08-25 | half_tael_DQN v4.0 release | Henry.
* Check [half_tael_DQN v4.0: DQN_v3.0 with improved cohesion, textual output, and documentation](https://github.com/choH/half_tael_DQN/releases/tag/v4.0).
    * Most effort spent into documenting the project.

### 2019-08-16 | half_tael_DQN v3.0 release | Henry.
* Check [half_tael_v3.0: Refactor DQN_v2.5 to work with virtual trading platform](https://github.com/choH/half_tael_DQN/milestone/5?closed=1).
    * Most effort spent into [Replace hardcore setting in half_tael_v3.0 model to accept dynamic input](https://github.com/choH/half_tael_DQN/issues/17) by [3ef23cf](https://github.com/choH/half_tael_DQN/commit/3ef23cf8e6bebec8754116296b71142e718c3770).

### 2019-08-15 | Bugfix cost converges too quick & smooth | Henry.
* Fixed the issued regarding [Cost (loss) graph converges way too quick and smooth](https://github.com/choH/half_tael_DQN/issues/15).
    * Wrong index for `a, r` in `batch_memory` while retrieving `eval_act_index`. So when replacing the reward(s), it is not the `a, r` being replaced, but two `_close` prices data at `batch_memory[: , self.n_features]` and `batch_memory[: , self.n_features + 1]` (therefore it is usually `0` or `1` as we use `as type(int)` during the retrieval) .
    * Changed to:


        ```
        eval_act_index = batch_memory[:, self.n_features * self.n_currencys].astype(int)
        reward = batch_memory[: , self.n_features * self.n_currencys + 1]
        ```    
     and fixed the bug in commit [d2fa6e7](https://github.com/choH/half_tael_DQN/commit/d2fa6e7a6b5fd7187fb7d41cc03cb269e05b49be).

* Partially removed hardcore code regarding `self.n_features` and `self.n_currency`.
    * CNN `conv2d()` part not yet done, but fixed all reshape-related setting to accept dynamic input.


### 2019-08-14 | Redesigned seetings of CNN  | Henry, with help from [Ziyu, CHEN](https://www.linkedin.com/in/zailchen17/).

* As Steven X. is absent for three days and unresponsive on IM for four days probably due to some unexpected urgencies, I seek Ziyu for help.
* Ziyu noticed the original `strides` were set to `strides = [1, 2, 25, 1]`, combine with`padding = 'SAME'` and `filter = [6, 6, 1, 32]` on input `[-1, 3, 300, 1]`, which effectively "over-padded" the input. as:

    \\[
    W_{out} = \frac{W - F_W + 2P}{S_W} + 1 \\
    \Rightarrow 300 = \frac{300 - 6 + 2P}{25} + 1  \ \ \Rightarrow P = 3603 \ (\text{too many}) \\
    H_{out} = \frac{H - F_H + 2P}{S_H} + 1 \\
    \Rightarrow 3 = \frac{3 - 6 + 2P}{2} + 1  \ \ \Rightarrow P = 1.5 \ (\text{not int?}) \\
    \\]

* We adjusted the setting to be:

    ```
    strides = [1, 1, 1, 1]
    filter = [3, 3, 1, 32]
    ```
* I also adjusted the reshape setting in `l1` from `32` to `3200` to work with `stride = [1, 1, 1, 1]` as there will be more output:

    ```
    W_fc1 = self.weight_variable([3 * 3200, 100])
    h_pool1_flat = tf.reshape(h_pool1, [-1, 3*3200])
    ```
    Otherwise the line will break on:

    ```
    q_target[batch_index, eval_act_index] = reward + self.gamma * np.max(q_next, axis=1)

    # Before adjustment
    # q_target[batch_index, eval_act_index].shape: (32, 7)
    # q_target.shape: (3200, 7)
    # np.max(q_next, axis =1): (3200, 7)
    ```

* Problem regarding cost converging too fast and smooth remains unsolved, updated [`cost_log.txt`](https://github.com/choH/half_tael_DQN/commit/7c081777ae285053d288ebf1abc53a4cc66fb27d) for future investigation.
    * After discussion with Ziyu, it is believed that the CNN part is correctly implemented, but mostly on the DQN part — however Ziyu is not particularly familiar with DQN, I will therefore continue the investigation. It is probably just a simple overfit issue as we only feeds `300` rows of train data and `300` rows of test data chronologically right after the training set, due to the power limitation of the laptop.



### 2019-08-13 | Refactored DQN_v2.5 to work with the trading platform | Henry.
* Be able to trade among three currencies with hardcore setting used in [`RL_brain.py`](https://github.com/choH/half_tael_DQN/commit/5ce65e38a0fdb52e428a2963e8bada26e299fb21).
* Problem regarding cost converging too fast and smooth remains unsolved, [`cost_log.txt`](https://github.com/choH/half_tael_DQN/commit/0d7164e8ce7b0621088a3715c014f630048bf799) saved for future investigation.

### 2019-08-11 | Bugfix and partial adjustments on DQN_v2.0, DQN_v2.5 delivered | Henry.
* Debugged on Steven's sketch code [ef6e716](https://github.com/choH/half_tael_DQN/commit/ef6e716af132541a0720bcb456f602c4f13cba06) with various `reshape` manipulations regarding `self.memory`, `store_transition` and `batch_memory`'s slicing in `feed_dict`.
* Several cosmetic on monitory print-outs.
* [Cost converges unreasonable fast and smooth](https://github.com/choH/half_tael_DQN/tree/v2.0/DQV_v2.5/cost_log.txt), potentially overfit, need investigation.

### 2019-08-09 | Debug DQN_v2.0 | Henry, Steven.
* Debug DQV_v2.0
    * solved bugs related to `self.s` and `self.s_` for `placeholder` and `reshape`.
    * solved bugs related to `self.x` and `self.x_` on `conv2d()`.
    * Work in progress on figuring out the bugs related to:

    ```
    transition = np.hstack((s, [a, r], s_))
    index = self.memory_counter % self.memory_size
    self.memory[index, :] = transition
    ```

### 2019-08-08 | Legacy Anita plot hole discovered | Henry.

* **Findings:**
    * After some careful review of [legacy_ref/anita folder](https://github.com/choH/half_tael_DQN/tree/master/legacy_ref/anita), I found that the mapping is between **personality** and **financial products**. e.g. (letter referred Big Five Personality Traits)
        * A persona with high E and low N is good for small cap investment.
        * A person with high C, high E, low A, low N is good for foreign exchange investment.
    * There are also many disparities between the [presentation slides](https://github.com/choH/half_tael_DQN/blob/master/legacy_ref/anita/Mapping%20Personality%20Traits%20to%20Investment%20Behavior%20(Revised).pptx) and the [metrics spreadsheet](https://github.com/choH/half_tael_DQN/blob/master/legacy_ref/anita/Strategies%20and%20Metrics.xlsx). e.g.
        * Slides indicate *"Momentum Investing (med-high c, high e, high a),"* but OCEAN value being 41.25, 40, 36.875, 36.25, and 35 respectively. Where the "mid-high C" is higher than the "high E" and "high A."
        * Slide indicate *"Income Investing (medium-high e, high n),"* but OCEAN value being 36.25, 35, 30, 30, and 32.5. Where the "mid-high E" is in fact the lowest value among five, and the supposedly "high N" ranks only among middle.


* **Conclusion:** Thus, this is essentially useless to our model as it cannot evaluate if a `trade_action` fits a given personality of not.
* **Solution:** My thinking is I will discard all Anita legacy and use some technical/fundamental analysis indicators to evaluate the "suitableness between a `trade_action` and given indicator" and therefore influent the reward. How a personality is defined by the indicators will left to future development.


### 2019-08-01 | Delivered half_tael_v2.0 running on DQN v2.0 | Henry.
* Implemented `balance_protection` feature on `trade_interface.py`. If the balance of sell currency is not enough to execute the requested trade, such trade will be canceled. The trade log will mark such trade as "failed." ([commit `#b735aff`](https://github.com/choH/half_tael_DQN/commit/b735aff1ccaf9ff9b34e6b6a215974597ef54e58))
* Discussed with Steven on the action update policy, decided the model does not need to know if an action is actually executed since the NN design will understand that at this `state` the `x` action will have bad reward (since equal balance will result in a reward of `-1`).
* Delivered half_tael_v2.0 by [commit `#6a051da`](https://github.com/choH/half_tael_DQN/commit/6a051dab9e63ec483e97f8b39b5fe6e1d5910e3f), Still hardcored to GBP due to the fact that DQN v1.0 only supports two-currency. Thus the non-base_currency is set manually. Will automate such part when refactoring with DQN v2.5 to avoid reengineering.  
    * Check [milestone #2](https://github.com/choH/half_tael_DQN/milestone/2?closed=1).


```
...
####################game over####################
##### Displaying information regarding account "Initial_Checkout_Review (episode: 2)". #####

	record_from:                  2018-04-13T18:30:00.000000000Z
	record_to:                    2018-04-16T09:29:00.000000000Z
	request_interval:             M1
	record_rows:                  889

	trade_log_len:                2
	USD:                          0
	EUR:                          100000.0
	GBP:                          0

##### The information of account "Initial_Checkout_Review (episode: 2)" has been successfully displayed. #####

##### Displaying information regarding account "End_Checkout_Review (episode: 2)". #####

	record_from:                  2018-04-13T18:30:00.000000000Z
	record_to:                    2018-04-16T09:29:00.000000000Z
	request_interval:             M1
	record_rows:                  889

	trade_log_len:                293
	USD:                          0
	EUR:                          100025.13121083906
	GBP:                          0.0

##### The information of account "End_Checkout_Review (episode: 2)" has been successfully displayed. #####
...
```

### 2019-07-31 | Starting to refactor DQN v1.0 | Henry.
* Till [30ec22c](https://github.com/choH/half_tael_DQN/commit/30ec22c343cb27f5338b1454d63b035df3b340ec), a understanding of DQN v1.0 is built.
* Bug fix on account cumulation with `execute_trade()` from `trade_interface.py`.
* Update hardcore setting (`n_features = 300`, record length to `4800` etc, currency as `EUR` and `GBP`) with relatively more universal adaptability.
* Work in progress on [commit `#0e0b676`](https://github.com/choH/half_tael_DQN/commit/0e0b6766cff67db23e79430caccd9726dc06b93ac), as a redesign of exception handling on `currency_balance[_sell_currency] < 0` is needed.
    * Ask Steven if the model need to know that some of its actions are not executed due to the balance issue.


### 2019-07-30 | Finished basic DQN learning | Henry.
* Finished most DQN part ([4.3](https://morvanzhou.github.io/tutorials/machine-learning/reinforcement-learning/4-3-DQN3/), up to date with what DQN v1.0 uses).
    * Check [issue #2](https://github.com/choH/half_tael_DQN/issues/2).


### 2019-07-29 | Dev branches base on half_tael_v1.0 | Henry.
* Branches [half_tael_v2.0](https://github.com/choH/half_tael_DQN/tree/half_tael_v2.0), [DQN_v2.5](https://github.com/choH/half_tael_DQN/tree/DQN_v2.5), and [anita_v1.1](https://github.com/choH/half_tael_DQN/tree/anita_v1.1) checked out from this commit — aka [Release half_tale_DQN v1.0: Virtual Trading Platform + Trial DQN](https://github.com/choH/half_tael_DQN/releases/tag/v1.0). ([commit `#113431e`](https://github.com/choH/half_tael_DQN/commit/113431e8247f200f5a0800b23e355072c5a9280b))

### 2019-07-26 | Initial commit for trial DQN between two currency | Steven, Henry.
* Initial commit for trial DQN between two currency -- Steven.
* Release tag v1.0 set -- Henry.
    * [half_tale_DQN v1.0: Virtual Trading Platform + Trial DQN](https://github.com/choH/half_tael_DQN/releases)

### 2019-07-25 | Draft contributors' guideline for the project | Henry.
* Research git `rebase` and git `branch`. Designed and drafted [`CONTRIBUTING.md`](https://github.com/choH/half_tael_DQN/blob/master/CONTRIBUTING.md) by [commit `#dd7e0ce`](https://github.com/choH/half_tael_DQN/commit/dd7e0ce97c59fd023e22cda412bf0aa8ba18a44f) to specify the workflow of this project.

### 2019-07-24 | Discussed merging Steven's experimental DQN code with Henry's trading environment code | Henry, Steve.
* Discussed the design and concern of merging Steven's experimental DQN code with Henry's trading environment code, particularly in:
    * How to support trading between multiple currencies (> 2) while making the machine realize some `_close` value is in the same time.
    * Possibility of using `vector` as first layer nodes in ANN/RNN design.
    * How to deal with missing `np.nan` in `_close` columns.
        * Increase `request_interval` from `M1` to `M5`.
        * Fill in `np.nan` cell gradual increment/decrement according to non-empty neighborhood cells, while setting `_volume` to `0`.

### 2019-07-24 | Drafted [`User Manual for trade_interface.py.md`](https://github.com/choH/half_tael_DQN/blob/master/demo_and_manual/User%20Manual%20for%20%60trade_interface.py%60.md), implemented `checkout_all_in()` method | Henry.
* Drafted [`User Manual for trade_interface.py.md`](https://github.com/choH/half_tael_DQN/blob/master/demo_and_manual/User%20Manual%20for%20%60trade_interface.py%60.md) with demo code available at [`train_interface_demo.py`](https://github.com/choH/half_tael_DQN/blob/master/demo_and_manual/train_interface_demo.py).
* Implemented `checkout_all_in()` method in `trade_interface.py` to checkout all currency(s) in account to a particular currency (e.g. `USD`).
* Debugged with Steven on his trial DQN model.

    ```
    ##### Displaying information regarding account "End_Checkout_Review". #####

    	record_from:                  2019-01-01T22:00:00.000000000Z
    	record_to:                    2019-01-01T23:59:00.000000000Z
    	request_interval:             M1
    	record_rows:                  118

    	trade_log_len:                9
    	USD:                          68536.17872218802
    	JPY:                          0.0
    	GBP:                          0.0

    ##### The information of account "End_Checkout_Review" has been successfully displayed. #####
    ```




### 2019-07-23 | Implemented custom exceptions handling, and stand alone training input portal | Henry.
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


### 2019-07-22 | Fully supports trading among multiple currency | Henry.
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



### 2019-07-19 | Refactored trading interface to handle trading among multiple currency (Bug-fixing in progress) | Henry.

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

### 2019-07-18 | Developed internal trading interface for model testing | Henry.
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

### 2019-07-17 | Developed wrapper functions output pricing record | Henry.
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

### 2019-07-11 | Finished Q-learning courses | Henry.
* Finished the *Q-learning* section of the [Morvan](https://morvanzhou.github.io/tutorials/machine-learning/reinforcement-learning/) course.
* Started the DQN section.
* Hand over the pervious project to be fully committed on this one.