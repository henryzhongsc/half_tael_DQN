from FX_env import FX
from RL_brain import DQN

import copy
import sys
sys.path.append('.')
import trade_interface as TI



def run_model(TI_account):
    step = 0

    TI_initial = copy.deepcopy(TI_account)

    for episode in range(5):
        # initial observation
        observation = env.reset()

        while True:
            # RL choose action based on observation
            action = DQN.choose_action(observation)

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)

            DQN.store_transition(observation, action, reward, observation_)

            if (step > 200) and (step % 5 == 0):
                DQN.learn()

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                print('#'*150)
                print('game over')
                print('#'*150)
                break
            step += 1

    # end of game



    #env.destroy()


if __name__ == "__main__":

    _account_name = 'DQN_v1.0_trial_data_5000_line' # 4800 rows.
    _currency_balance = {'USD': 0, 'EUR': 100000, 'GBP': 0}
    _from = "2018-04-13T18:30:00Z"
    _to = "2018-04-19T03:27:00Z"
    _interval = "M1"
    TI_train = TI.Trade_Interface(_account_name, _currency_balance, _from, _to, _interval)



    env = FX(TI_train)
    DQN = DQN(env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )

    run_model(TI_train)

    DQN.plot_cost()