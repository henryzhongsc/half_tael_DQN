from FX_env import FX
from RL_brain import DQN

import copy
import sys
sys.path.append('.')
import trade_interface as TI


time_initial = '2018-04-13T18:30:00.000000000Z'
time_end = '2018-04-19T03:26:00.000000000Z'


def run_model():
    step = 0

    for episode in range(2):
        observation, TI_initial, initial_time = env.reset()
        TI_initial_balance = copy.deepcopy(TI_initial)

        while True:
            action = DQN.choose_action(observation)
            observation_, reward, done, TI_end, end_time = env.step(action)

            DQN.store_transition(observation, action, reward, observation_)
            if (step > 200) and (step % 5 == 0):
                DQN.learn()
            observation = observation_

            if done:
                print('#'*20 + 'game over' + '#'*20)

                TI_initial_balance.account_name = 'Initial_Checkout_Review' + ' (episode: ' + str(episode+1) + ')'
                TI_initial_balance.checkout_all_in(initial_time, 'EUR')
                TI_initial_balance.account_review()

                print('@'*20)
                TI_end.trade_log_review(tar_action_id = 0)
                TI_end.trade_log_review(tar_action_id = 'LAST')
                print('@'*20)


                TI_end_balance = copy.deepcopy(TI_end)
                TI_end_balance.account_name = 'End_Checkout_Review' + ' (episode: ' + str(episode+1) + ')'
                TI_end_balance.checkout_all_in(end_time, 'EUR')
                TI_end_balance.account_review()


                # TI_end_balance.trade_log_review()
                break

            step += 1


if __name__ == "__main__":

###########################################################################################

    _account_name = 'DQN_v1.0_trial_data_5000_line'
    _currency_balance = {'USD': 0, 'EUR': 100000, 'GBP': 0}
    _from = "2018-04-13T18:30:00Z"
    # _to = "2018-04-19T03:27:00Z" # 4800 rows.
    _to = "2018-04-16T09:30:00Z" # 904 rows
    _interval = "M1"
    TI_train = TI.Trade_Interface(_account_name, _currency_balance, _from, _to, _interval)

###########################################################################################


    env = FX(TI_train, trade_on = 'EUR_GBP_close', base_currency = 'EUR')
    DQN = DQN(env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    run_model()

    DQN.plot_cost()