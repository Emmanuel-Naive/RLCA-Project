"""
Reinforcement learning (Q-learning) maze example.
This script is the main part which controls the update method of this example.

Writen by Morvan: https://morvanzhou.github.io/tutorials/
Modified by Weijian: weijiany@stud.ntnu.no

Version: 2 ship, 2 goals and 2 obstacles (consider collision)
Red rectangle:         ship (explorer)
Black rectangles:      obstacle
Yellow bin circle:     goal
All other states:      open sea
"""

from Env.case3_S2CO import Maze               # Choose environment
from RLbrain.RLmodified import QLearningTable   # Choose reinforcement learning algorithm

import numpy as np
import time

def update(iter,rewardtime1,rewardtime2):
    time.sleep(5)
    i = 0
    for episode in range(iter):
        # initial observation
        observation1 = env.reset()
        observation2 = env.reset()
        rewardtl1 = 0
        rewardtl2 = 0
        j=0
        while True:
            # fresh env
            env.render()
            j += 1
            if observation1 != 'terminal':
                # RL choose action based on observation
                action1 = RL.choose_action(str(observation1))
                # RL take action and get next observation and reward
                observation1_, reward1, done1 = env.step1(action1)
            if observation2 != 'terminal':
                # RL choose action based on observation
                action2 = RL.choose_action(str(observation2))
                # RL take action and get next observation and reward
                observation2_, reward2, done2 = env.step2(action2)

            reward1c, reward2c = env.checkgoal(observation1_,observation2_)
            reward1, done1, reward2, done2 = env.checkcollison(observation1_, reward1, done1, observation2_, reward2, done2)
            reward1 = reward1 + reward1c / j
            reward2 = reward2 + reward2c / j
            # RL learn from this transition
            RL.learn(str(observation1), action1, reward1, str(observation1_))
            RL.learn(str(observation2), action2, reward2, str(observation2_))

            # swap observation
            observation1 = observation1_
            observation2 = observation2_
            rewardtl1 += reward1
            rewardtl2 += reward2
            # break while loop when end of this episode
            if observation1 != 'terminal':
                Exciter1 = 1
                rewardtime1[0, i] = j
                rewardtime1[1, i] = rewardtl1
            if Exciter1 == 1 and observation1 == 'terminal':
                Exciter1 = 0
                rewardtime1[0, i] = j
                rewardtime1[1, i] = rewardtl1
            if observation2 != 'terminal':
                Exciter2 = 1
                rewardtime2[0, i] = j
                rewardtime2[1, i] = rewardtl2
            if Exciter2 == 1 and observation2 == 'terminal':
                Exciter2 = 0
                rewardtime2[0, i] = j
                rewardtime2[1, i] = rewardtl2
            if done1 or done2:
                break
        i += 1
    # end of game
    print('game over')
    # env.destroy()

if __name__ == "__main__":
    env = Maze()
    RL = QLearningTable(actions=list(range(env.n_actions)))
    iter = 100
    rewardtime1 = np.zeros((2, iter))
    rewardtime2 = np.zeros((2, iter))
    env.after(iter, update(iter,rewardtime1,rewardtime2))
    env.mainloop()
    np.save('RL1.npy', rewardtime1)
    np.save('RL2.npy', rewardtime2)