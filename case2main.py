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

from Env.case2_S1O import Maze               # Choose environment
# from RLbrain.RLorigin import QLearningTable   # Choose reinforcement learning algorithm
from RLbrain.RLmodified import QLearningTable   # Choose reinforcement learning algorithm

import numpy as np
import time
def update(iter,rewardtime):
    time.sleep(5)
    i=0
    for episode in range(iter):
        # initial observation
        observation1 = env.reset()
        rewardtl1=0
        j=0
        while True:
            j += 1
            # fresh env
            env.render()

            # RL choose action based on observation
            action1 = RL.choose_action(str(observation1))

            # RL take action and get next observation and reward
            observation_1, reward1, done1 = env.step1(action1)

            # Correction for goal
            rewardcg = env.checkgoal(observation_1)/j
            reward1 = reward1 + rewardcg

            # RL learn from this transition
            RL.learn(str(observation1), action1, reward1, str(observation_1))

            # swap observation
            observation1 = observation_1
            rewardtl1 += reward1
            print(reward1)
            # break while loop when end of this episode
            if done1:
                rewardtime[0, i] = j
                rewardtime[1, i] = rewardtl1
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
