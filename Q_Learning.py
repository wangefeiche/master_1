"""
A simple example for Reinforcement Learning using table lookup Q-learning method.
An agent "o" is on the left of a 1 dimensional world, the treasure is on the rightmost location.
Run this program and to see how the agent will improve its strategy of finding the treasure.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

import numpy as np
import pandas as pd
import time
import csv

#np.random.seed(3)  # reproducible

data_file = "sim0_cl0_throughputLog.txt"
qtable_file = "qtable.txt"
N_STATES = 5   # the length of the 1 dimensional world
ACTIONS = ['1', '2','3','4','5','6','7','8','9','10']     # available actions
EPSILON = 0.8   # greedy police
ALPHA = 0.1     # learning rate
GAMMA = 0.9    # discount factor
MAX_EPISODES = 500   # maximum episodes
FRESH_TIME = 0.01    # fresh time for one move
bufferLength = 0 # the client buffer length
downloadStart = 0
downloadEnd = 0
segmentDuration = 1

IS_FIRST_TABLE = False
add_permission = False
repeat_after = False
ADD_COUNT_MAX = 5
add_count = 0

SegmentSize_360s_list = []
with open("SegmentSize_360s.txt",'r') as SegmentSize_360s_readfile:
    n=0
    while True:
        lines = SegmentSize_360s_readfile.readline() # 整行读取数据
        if not lines:
            break
        i = lines.split()
        SegmentSize_360s_list.append([float(x) for x in i])
        n = n+1
#print(SegmentSize_360s_list)
SegmentSize_360s_list = [[float(x) for x in row] for row in SegmentSize_360s_list]

DlRxPhyStats_time, DlRxPhyStats_tbsize = [], []
with open(data_file,'r') as DlRxPhyStats_to_read:
    n=0
    while True:
        lines = DlRxPhyStats_to_read.readline() # 整行读取数据
        if not lines:
            break
        i = lines.split()
        DlRxPhyStats_time.append(float(i[0]))
        DlRxPhyStats_tbsize.append(float(i[1])*8)
        n = n+1

#print(DlRxPhyStats_time)


def build_q_table(n_states, actions):
    if not IS_FIRST_TABLE:
        table = pd.read_csv('qtable.csv',names=actions,header=0)
    else:
        table = pd.DataFrame(
            np.zeros((n_states, len(actions))),     # q_table initial values
            columns=actions,    # actions's name
        )

    if repeat_after:
        table_length = table.iloc[:,0].size - ADD_COUNT_MAX
        table = table[0:table_length]
    # print(table)    # show table
    return table

def check_state_exist(state,table):
    if state not in table.index:
        # append new state to q table
        table = table.append(
            pd.Series(
                [0]*len(ACTIONS),
                index=table.columns,
                name=state,
            )
        )
    return table

def choose_action(state, q_table):
    # This is how to choose an action
    state_actions = q_table.iloc[state, :]
    if (np.random.uniform() > EPSILON) or ((state_actions == 0).all()):  # act non-greedy or state-action have no value
        action_name = np.random.choice(ACTIONS)
    else:   # act greedy
        action_name = state_actions.idxmax()    # replace argmax to idxmax as argmax means a different function in newer version of pandas
    return action_name


def get_env_feedback(S,T,B,A,q_table):
    # This is how agent will interact with the environment
    action = int(A)
    segmentSize = SegmentSize_360s_list[action-1][S-1]*segmentDuration*8
    downloadStart = DlRxPhyStats_time[T]
    downloadEnd = 0
    size_sum = 0
    T_ = T
    B_ = B
    R = 0
    for data_size in DlRxPhyStats_tbsize[T:]:
        if size_sum < segmentSize:
            size_sum = size_sum + data_size
            T_ = T_ + 1
        else:
            downloadEnd = DlRxPhyStats_time[T_]
            break

    state_count = q_table.iloc[:,0].size
    #print("===============",downloadStart,downloadEnd)
    if S == 1:
        B_ = B_ + segmentDuration
    else:
        B_ = B_ + segmentDuration - (downloadEnd-downloadStart)

    if B > downloadEnd-downloadStart and B_ < 1.5 :
        if S == state_count-1:
            S_ = S+1
            R = 1
        else:
            S_ = S + 1
            R = 0
    else:
        if S == 1 and downloadEnd-downloadStart < 3 and downloadEnd-downloadStart > 0.8:
            S_ = S + 1
            R = 0
        else:
            S_ = 0
            R = -1
    print("==============="," S: ",S," A: ",A," S_: ",S_," B_: ",B_,downloadStart,downloadEnd)
    if downloadEnd == 0:
        S_ = 0
        R = 1
    return S_,T_,B_,R



def update_env(S, episode, step_counter):
    # This is how environment be updated
    env_list = ['-']*(N_STATES-1) + ['T']   # '---------T' our environment
    if S == 'terminal':
        interaction = 'Episode %s: total_steps = %s' % (episode+1, step_counter)
        print('\r{}'.format(interaction), end='')
        time.sleep(2)
        print('\r                                ', end='')
    else:
        env_list[S] = 'o'
        interaction = ''.join(env_list)
        print('\r{}'.format(interaction), end='')
        time.sleep(FRESH_TIME)


def rl(add_permission,add_count):
    # main part of RL loop
    q_table = build_q_table(N_STATES, ACTIONS)
    print(q_table)
    for episode in range(MAX_EPISODES):
        step_counter = 0
        S = 1
        T = 0
        B = 0
        is_terminated = False
        #update_env(S, episode, step_counter)
        if int(episode/(MAX_EPISODES/ADD_COUNT_MAX)) == add_count-1:
            pass
        else:
            add_permission = True
                

        while not is_terminated:
            #print("==================",int(episode/(MAX_EPISODES/ADD_COUNT_MAX)))
            qtable_length = q_table.iloc[:,0].size
            A = choose_action(S, q_table)
            if IS_FIRST_TABLE:
                if S<qtable_length-ADD_COUNT_MAX:
                    A = q_table.iloc[S, :].idxmax()
            else:
                if S<qtable_length-add_count:
                    A = q_table.iloc[S, :].idxmax()
            S_,T,B,R = get_env_feedback(S,T,B,A,q_table)  # take action & get next state and reward
            q_predict = q_table.loc[S, A]
            if add_permission:
                if S_ == qtable_length:
                    q_table = check_state_exist(S_,q_table)
                    add_permission = False
                    add_count += 1
                    #print(q_table)
            else:
                if S_ == qtable_length:
                    S_ = 0
                    #print(S_)
            #print(q_table.iloc[:,0].size)
            if S_ != 0:
                q_target = R + GAMMA * q_table.iloc[S_, :].max()   # next state is not terminal
            else:
                q_target = R     # next state is terminal
                is_terminated = True    # terminate this episode
            print(episode,add_count,add_permission," reward: ",R)
            print(q_table.loc[S, A],q_target)
            if IS_FIRST_TABLE:
                if (q_table.loc[S, A]>0.9 and q_target < q_predict) or S < qtable_length-ADD_COUNT_MAX:
                    pass
                else:
                    q_table.loc[S, A] += ALPHA * (q_target - q_predict)  # update
            else:
                if (q_table.loc[S, A]>0.9 and q_target < q_predict) or S < qtable_length-add_count:
                    pass
                else:
                    q_table.loc[S, A] += ALPHA * (q_target - q_predict)  # update
            #print(q_table)
            #print(episode,step_counter)
            S = S_  # move to next state

            #update_env(S, episode, step_counter+1)
            step_counter += 1
        #print(q_table)
    return q_table


if __name__ == "__main__":
    q_table = rl(add_permission,add_count)
    print('\r\nQ-table:\n')
    print(q_table)
    q_table.to_csv('qtable.csv')
