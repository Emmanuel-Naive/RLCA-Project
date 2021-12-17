"""
Reinforcement learning (Q-learning) maze example.
This script is the main part which controls the update method of this example.

Writen by Morvan: https://morvanzhou.github.io/tutorials/
Modified by Weijian: weijiany@stud.ntnu.no

Version: 1 ship, 1 goals and n obstacles (consider collision)
Red rectangle:         ship (explorer)
Black rectangles:      obstacle
Yellow bin circle:     goal
All other states:      open sea
"""

from Env.case1_S1O import Maze               # Choose environment
# from RLbrain.RLorigin import QLearningTable   # Choose reinforcement learning algorithm
from RLbrain.RLmodified import QLearningTable   # Choose reinforcement learning algorithm

import numpy as np
# from scipy import io
import time
def update(iter,rewardtime):
    time.sleep(5)
    i=0
    for episode in range(iter):
        # initial observation
        observation = env.reset()
        rewardtl=0
        j=0
        while True:
            j += 1
            # fresh env
            env.render()

            # RL choose action based on observation
            action = RL.choose_action(str(observation))

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)

            # RL learn from this transition
            RL.learn(str(observation), action, reward, str(observation_))

            # swap observation
            observation = observation_
            rewardtl += reward
            # break while loop when end of this episode
            if done:
                rewardtime[0, i] = j
                rewardtime[1, i] = rewardtl
                break

        i += 1
    # end of game
    # print('game over')
    # env.destroy()

if __name__ == "__main__":
    env = Maze()
    RL = QLearningTable(actions=list(range(env.n_actions)))

    iter = 100
    rewardtime = np.zeros((2, iter))

    env.after(iter, update(iter,rewardtime))
    env.mainloop()
    np.save('RL.npy', rewardtime)
    # io.savemat('ship1.mat', {'matrix': rewardtime})
