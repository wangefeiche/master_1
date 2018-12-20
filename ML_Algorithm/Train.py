from Enverienment import Maze
#from RL_brain import DeepQNetwork
from Deep_Q_Network import DeepQNetwork
import numpy as np


def run_maze():
    step = 0
    for episode in range(10000):
        # initial observation
        #observation = env.reset()
        observation = np.array([0.,0.])
        #observation = np.array([0.002778,0.854167])
        while True:
            # fresh env
            #env.render()

            # RL choose action based on observation
            action = RL.choose_action(observation)
            #print(observation,action)

            # RL take action and get next observation and reward
            observation_, reward, done, info = env.step(action)
            #reward /= 40
            print(step,observation,action,reward,info)
            done_int = 1 if done else 0
            RL.store_transition(observation, action, reward, done_int, observation_)

            if (step > 20) and (step % 5 == 0):
                RL.learn()

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break
            step += 1

    # end of game
    print('game over')


if __name__ == "__main__":
    # maze game
    env = Maze()
    RL = DeepQNetwork(env.n_actions, env.n_features,
                      learning_rate=0.1,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      output_graph=True
                      )
    run_maze()
    #env.mainloop()
    RL.plot_cost()