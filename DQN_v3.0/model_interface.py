from FX_env import FX
from RL_brain import DQN

import contextlib
import json
import os
import copy
import sys
sys.path.append('.')
# print(sys.path)
from model_config import *


import trade_interface as TI


def run_model(_train_episode = 100,
                _learn_threshold = 200,
                _learn_interval = 5,
                _base_currency = 'USD',
                _trade_log_mode = 'NONE',
                _trade_log_to_file = False,
                _show_checkout = True,
                _show_step = True):

    step = 0

    for episode in range(_train_episode):
        observation, TI_initial, initial_time = env.reset()
        TI_initial_balance = copy.deepcopy(TI_initial)
        train_name = TI_initial.account_name

        while True:
            action = DQN.choose_action(observation)
            observation_, reward, done, TI_end, end_time = env.step(action, print_step = _show_step)
            DQN.store_transition(observation, action, reward, observation_)

            if (step > _learn_threshold) and (step % _learn_interval == 0):
                DQN.learn()
            observation = observation_

            if done:
                print('$'*20 + ' GAME OVER ' + '$'*20)

                TI_initial_balance.account_name = 'Initial_Checkout_Review' + ' (episode: ' + str(episode+1) + ')'
                TI_initial_balance.checkout_all_in(initial_time, _base_currency)
                TI_end_balance = copy.deepcopy(TI_end)
                TI_end_balance.account_name = 'End_Checkout_Review' + ' (episode: ' + str(episode+1) + ')'
                TI_end_balance.checkout_all_in(end_time, _base_currency)

                if _show_checkout == True:
                    TI_initial_balance.account_review()
                    TI_end_balance.account_review()

                if _trade_log_mode == False:
                    pass
                elif _trade_log_mode == 'ALL':
                    TI_end_balance.trade_log_review(raw_flag = _trade_log_raw)
                elif _trade_log_mode == 'TWOENDS':
                    TI_end.trade_log_review(tar_action_id = 0, raw_flag = _trade_log_raw)
                    TI_end.trade_log_review(tar_action_id = 'LAST', raw_flag = _trade_log_raw)
                else:
                    print('Invalid _trade_log_mode input ({}). Must be \'ALL\', \'TWOENDS\', or False'.format(_trade_log_mode))
                    return -1

                if _trade_log_to_file:
                    trade_log_base_dir = './logs/trade_logs/'
                    if not os.path.exists(trade_log_base_dir):
                        os.makedirs(trade_log_base_dir)
                    trade_log_file_name = trade_log_base_dir + str(train_name)

                    log_file_readable = open(trade_log_file_name + '.txt', 'w+')
                    with contextlib.redirect_stdout(log_file_readable):
                        TI_end.trade_log_review()
                    print("### READABLE trade_log of {} successfully exported to: ###\n\t\t{}".format(str(train_name), trade_log_file_name + '.txt'))
                    log_file_readable.close()

                    log_file_raw = open(trade_log_file_name + '.json', 'w+')
                    json.dump(TI_end.trade_log, log_file_raw, indent = 4)
                    print("### RAW trade_log of {} successfully exported to: ###\n\t\t{}".format(str(train_name), trade_log_file_name + '.json'))
                    log_file_raw.close()

                break
            step += 1


if __name__ == "__main__":

    TI_train = TI.Trade_Interface(config_account_name, config_currency_balance, config_from, config_to, config_interval, config_output_arena_csv, config_output_raw_csv)

    env = FX(TI_train,
            _base_currency = config_base_currency,
            _n_features = config_n_features,
            _anita_switch = config_anita_switch)

    DQN = DQN(len(env.TI_initial.currency_pairs),
                env.n_actions,
                env.n_features,
                learning_rate = config_learning_rate,
                reward_decay = config_reward_decay,
                e_greedy = config_e_greedy,
                replace_target_iter = config_replace_target_iter,
                memory_size = config_memory_size,
                output_graph = config_output_graph)

    run_model(_train_episode = config_train_episode,
                _learn_threshold = config_learn_threshold,
                _learn_interval = config_learn_interval,
                _base_currency = config_base_currency,
                _trade_log_mode = config_trade_log_mode,
                _trade_log_to_file = config_trade_log_to_file,
                _show_checkout = config_show_checkout,
                _show_step = config_show_step)

    DQN.plot_cost()