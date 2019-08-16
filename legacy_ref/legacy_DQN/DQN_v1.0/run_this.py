from maze_env import Maze
from RL_brain import DeepQNetwork


def run_maze():
    step = 0
    for episode in range(2):
        # initial observation
        observation = env.reset()

        # print("###############################################")
        print(type(observation))
        # print("###############################################")

        while True:
            # fresh env
            #env.render()

            # RL choose action based on observation

            action = RL.choose_action(observation)

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)

            RL.store_transition(observation, action, reward, observation_)

            if (step > 200) and (step % 5 == 0):
                RL.learn()

            # swap observation
            # print("################# observation_ ############################")
            # print(type(observation_))
            # print("################### observation_ ##########################")
            observation = observation_

            # break while loop when end of this episode
            if done:
                print('game over')
                print(env.balance)
                # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$                             $$$$$$$$$$$$$$$$$$$$$$$$$$$")
                # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$                             $$$$$$$$$$$$$$$$$$$$$$$$$$$")
                # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                break
            step += 1

    # end of game



    #env.destroy()


if __name__ == "__main__":
    # maze game
    env = Maze()
    RL = DeepQNetwork(env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
#     env.after(100, run_maze)
    run_maze()
#     env.mainloop()
    RL.plot_cost()