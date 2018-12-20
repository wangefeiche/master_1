''' Demo SDK for LiveStreaming
    Author Dan Yang
    Time 2018-10-15
    For LiveStreaming Game'''
# import the env from pip
import LiveStreamingEnv.fixed_env as fixed_env
#import fixed_env
import LiveStreamingEnv.load_trace as load_trace
#import matplotlib.pyplot as plt
import time
import csv
import pandas as pd
import numpy as np
import tensorflow as tf
import ABR
import ABR_RETURN
# path setting
#===========Q_learning=============
""" MAX_EPISODES = 100
stop_count = 2000
EPSILON = 1
ALPHA = 0.1     # learning rate
GAMMA = 0.9    # discount factor
IS_FIRST_TABLE = True
actions = ['0','1','2','3']
n_states = stop_count+1
if not IS_FIRST_TABLE:
    table = pd.read_csv('qtable.csv',names=actions,header=0)
else:
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))),     # q_table initial values
        columns=actions,    # actions's name
    )
    table.to_csv('qtable.csv') """



#===========Q_learning=============

def test(user_id):
    #TRAIN_TRACES = '/home/game/test_sim_traces/'   #train trace path setting,
    #video_size_file = '/home/game/video_size_'      #video trace path setting,
    #LogFile_Path = "/home/game/log/"                #log file trace path setting,
    
    TRAIN_TRACES = './network_trace_2/'   #train trace path setting,
    #video_size_file = './video_trace/AsianCup_China_Uzbekistan/frame_trace_'      #video trace path setting,
    #video_size_file = './video_trace/Fengtimo_2018_11_3/frame_trace_'      #video trace path setting,
    #video_size_file = './video_trace/YYF_2018_08_12/frame_trace_'      #video trace path setting,

    #video_size_file = './video_trace_2/game/frame_trace_'
    video_size_file = './video_trace_2/room/frame_trace_'
    #video_size_file = './video_trace_2/sports/frame_trace_'

    LogFile_Path = "./log/"                #log file trace path setting,
    # Debug Mode: if True, You can see the debug info in the logfile
    #             if False, no log ,but the training speed is high
    DEBUG = False
    # load the trace
    all_cooked_time, all_cooked_bw, all_file_names = load_trace.load_trace(TRAIN_TRACES)
    #random_seed 
    random_seed = 2
    count = 0
    video_count = 0
    FPS = 25
    frame_time_len = 0.04
    reward_all_sum = 0
    #init 
    #setting one:
    #     1,all_cooked_time : timestamp
    #     2,all_cooked_bw   : throughput
    #     3,all_cooked_rtt  : rtt
    #     4,agent_id        : random_seed
    #     5,logfile_path    : logfile_path
    #     6,VIDEO_SIZE_FILE : Video Size File Path
    #     7,Debug Setting   : Debug
    net_env = fixed_env.Environment(all_cooked_time=all_cooked_time,
                                  all_cooked_bw=all_cooked_bw,
                                  random_seed=random_seed,
                                  logfile_path=LogFile_Path,
                                  VIDEO_SIZE_FILE=video_size_file,
                                  Debug = DEBUG)
    abr_return = ABR_RETURN.Algorithm()
    abr_return_init = abr_return.Initial()
    abr = ABR.Algorithm()
    abr_init = abr.Initial()

    BIT_RATE      = [500.0,850.0,1200.0,1850.0] # kpbs
    TARGET_BUFFER = [2.0,3.0]   # seconds
    # ABR setting
    RESEVOIR = 0.5
    CUSHION  = 2

    cnt = 0
    # defalut setting
    last_bit_rate = 0
    bit_rate = 0
    target_buffer = 0
    th_list = [0]*5
    buffer, cdn_count = 0,0
    debug_list = [['time','throughput','time_interval', 'send_data_size', 'chunk_len',\
               'rebuf', 'buffer_size', 'play_time_len','end_delay',\
                'cdn_newest_id', 'download_id', 'cdn_has_frame', 'decision_flag',\
                'buffer_flag', 'cdn_flag', 'end_of_video']]
    wr = [['time','prediction_bitrate','next_segment_rate','segment_rate','cdn_list','ave_th','curr_th','th_10','th_20','th_30','th_40','th_50','buffer','cdn_buffer','buffer_flag','cdn_flag','cdn_count','end_delay','cdn_newest_id','download_id','bit_rate','qoe_label','qoe_1','qoe_2','qoe_3','qoe_4']]
    # QOE setting
    reward_frame = 0
    reward_all = 0
    reward_all_1,reward_all_2,reward_all_3,reward_all_4 = 0,0,0,0
    last_reward_all_1,last_reward_all_2,last_reward_all_3,last_reward_all_4 = 0,0,0,0
    last_segment_reward = 0
    ll_segment_info = [0]*8
    SMOOTH_PENALTY= 0.02
    REBUF_PENALTY = 1.5
    LANTENCY_PENALTY = 0.005
    # past_info setting
    past_frame_num  = 7500
    S_time_interval = [0] * past_frame_num
    S_send_data_size = [0] * past_frame_num
    S_chunk_len = [0] * past_frame_num
    S_rebuf = [0] * past_frame_num
    S_buffer_size = [0] * past_frame_num
    S_end_delay = [0] * past_frame_num
    S_chunk_size = [0] * past_frame_num
    S_play_time_len = [0] * past_frame_num
    S_decision_flag = [0] * past_frame_num
    S_buffer_flag = [0] * past_frame_num
    S_cdn_flag = [0] * past_frame_num
    # params setting
    
    is_terminated = False
    cnt_segment = 0
    #q_table = pd.read_csv('qtable.csv',names=actions,header=0)
    while True:
        reward_frame = 0
        reward_1,reward_2,reward_3,reward_4 = 0,0,0,0
        
        # input the train steps
        #if cnt > 5000:
            #plt.ioff()
        #    break
        #actions bit_rate  target_buffer
        # every steps to call the environment
        # time           : physical time 
        # time_interval  : time duration in this step
        # send_data_size : download frame data size in this step
        # chunk_len      : frame time len
        # rebuf          : rebuf time in this step          
        # buffer_size    : current client buffer_size in this step          
        # rtt            : current buffer  in this step          
        # play_time_len  : played time len  in this step          
        # end_delay      : end to end latency which means the (upload end timestamp - play end timestamp)
        # decision_flag  : Only in decision_flag is True ,you can choose the new actions, other time can't Becasuse the Gop is consist by the I frame and P frame. Only in I frame you can skip your frame
        # buffer_flag    : If the True which means the video is rebuffing , client buffer is rebuffing, no play the video
        # cdn_flag       : If the True cdn has no frame to get 
        # end_of_video   : If the True ,which means the video is over.
        time,time_interval, send_data_size, chunk_len,\
               rebuf, buffer_size, play_time_len,end_delay,\
                cdn_newest_id, download_id, cdn_has_frame, decision_flag,\
                buffer_flag, cdn_flag, end_of_video = net_env.get_video_frame(bit_rate,target_buffer)
        if time_interval!=0:
            throughput = send_data_size/time_interval/1000
        else:
            throughput = 0
        debug_list.append([time,throughput,time_interval, send_data_size, chunk_len,\
               rebuf, buffer_size, play_time_len,end_delay,\
                cdn_newest_id, download_id, cdn_has_frame, decision_flag,\
                buffer_flag, cdn_flag, end_of_video])

        # S_info is sequential order
        S_time_interval.pop(0)
        S_send_data_size.pop(0)
        S_chunk_len.pop(0)
        S_buffer_size.pop(0)
        S_rebuf.pop(0)
        S_end_delay.pop(0)
        S_play_time_len.pop(0)
        S_decision_flag.pop(0)
        S_buffer_flag.pop(0)
        S_cdn_flag.pop(0)

        S_time_interval.append(time_interval)
        S_send_data_size.append(send_data_size)
        S_chunk_len.append(chunk_len)
        S_buffer_size.append(buffer_size)
        S_rebuf.append(rebuf)
        S_end_delay.append(end_delay)
        S_play_time_len.append(play_time_len)
        S_decision_flag.append(decision_flag)
        S_buffer_flag.append(buffer_flag)
        S_cdn_flag.append(cdn_flag)        

        # QOE setting 
        if not cdn_flag:
            reward_frame = frame_time_len * float(BIT_RATE[bit_rate]) / 1000  - REBUF_PENALTY * rebuf - LANTENCY_PENALTY  * end_delay
            reward_1 = frame_time_len * float(BIT_RATE[bit_rate]) / 1000
            reward_2 = REBUF_PENALTY * rebuf
            reward_3 = LANTENCY_PENALTY  * end_delay
        else:
            reward_frame = -(REBUF_PENALTY * rebuf)
            reward_1 = 0
            reward_2 = REBUF_PENALTY * rebuf
            reward_3 = 0
        if decision_flag or end_of_video:
            cnt_segment += 1
            # reward formate = play_time * BIT_RATE - 4.3 * rebuf - 1.2 * end_delay
            reward_frame += -1 * SMOOTH_PENALTY * (abs(BIT_RATE[bit_rate] - BIT_RATE[last_bit_rate]) / 1000)
            reward_4 = 1 * SMOOTH_PENALTY * (abs(BIT_RATE[bit_rate] - BIT_RATE[last_bit_rate]) / 1000)
            # last_bit_rate
            #print(len(th_list),th_list)
            reward_temp_1 = -last_reward_all_1 + reward_all_1
            reward_temp_2 = last_reward_all_2 - reward_all_2
            reward_temp_3 = last_reward_all_3 - reward_all_3
            reward_temp_4 = last_reward_all_4 - reward_all_4
            last_bit_rate = bit_rate
            last_reward_all_1 = reward_all_1
            last_reward_all_2 = reward_all_2
            last_reward_all_3 = reward_all_3
            last_reward_all_4 = reward_all_4
            #==================================Q_learning==============================

            
            """ action = last_bit_rate
            state = cnt_segment - 1
            next_state = cnt_segment
            R = last_segment_reward
            R = R - 0.1*abs(buffer_size-2.35)
                
            
            q_predict = q_table.loc[state, str(action)]
            if end_of_video:#state != stop_count:
                q_target = R + GAMMA * q_table.iloc[next_state, :].max()   # next state is not terminal
            else:
                q_target = R     # next state is terminal
                is_terminated = True    # terminate this episode
            

            
            q_table.loc[state, str(action)] += ALPHA * (q_target - q_predict)
            #q_table.loc[state, str(action)] = R

            if is_terminated:
                #print(q_table)
                q_table.to_csv('qtable.csv')
                break

            state_actions = q_table.iloc[next_state, :]
            if (np.random.uniform() > EPSILON) or ((state_actions == 0).all()):  # act non-greedy or state-action have no value
                action_name = np.random.choice(actions)
            else:   # act greedy
                action_name = state_actions.idxmax()    # replace argmax to idxmax as argmax means a different function in newer version of pandas
            
            #print(state,action,R,next_state,q_table.loc[state, str(action)],action_name)
            #print(q_table)
            #==================================Q_learnign=========================== """

            # -------------------------------------------Your Althgrithom ------------------------------------------- 
            # which part is the althgrothm part ,the buffer based , 
            # if the buffer is enough ,choose the high quality
            # if the buffer is danger, choose the low  quality
            # if there is no rebuf ,choose the low target_buffer
            th_list, buffer, cdn_count, prediction_bitrate,segment_rate,ave_th,curr_th,next_sg_rate= abr_return.run(time,S_time_interval,S_send_data_size,S_chunk_len,S_rebuf,S_buffer_size, S_play_time_len,S_end_delay,S_decision_flag,S_buffer_flag,S_cdn_flag, end_of_video, cdn_newest_id, download_id,cdn_has_frame,abr_init)
            bit_rate , target_buffer = abr.run(time,S_time_interval,S_send_data_size,S_chunk_len,S_rebuf,S_buffer_size, S_play_time_len,S_end_delay,S_decision_flag,S_buffer_flag,S_cdn_flag, end_of_video, cdn_newest_id, download_id,cdn_has_frame,abr_init)
            last_segment_info = ll_segment_info + [last_segment_reward,reward_temp_1,reward_temp_2,reward_temp_3,reward_temp_4]
            #print(end_delay,cdn_newest_id,download_id)
            wr.append(last_segment_info)
            #bit_rate = int(action_name)
            ll_segment_info = [time,prediction_bitrate,next_sg_rate,segment_rate,cdn_has_frame,ave_th,curr_th,th_list[0],th_list[1],th_list[2],th_list[3],th_list[4],buffer,end_delay-buffer+0.04,buffer_flag,cdn_flag,cdn_count,end_delay,cdn_newest_id,download_id,bit_rate]
            last_segment_reward = 0
            
            # ------------------------------------------- End  ------------------------------------------- 
            
        if end_of_video:
            q_table.to_csv('qtable.csv')
            print("video count", video_count, reward_all,reward_all_1,reward_all_2,reward_all_3,reward_all_4)
            reward_all_sum += reward_all / 1000
            video_count += 1
            if video_count >= 1:#len(all_file_names):
                    break
            cnt = 0
            last_bit_rate = 0
            reward_all = 0
            reward_all_1,reward_all_2,reward_all_3,reward_all_4 = 0,0,0,0
            bit_rate = 0
            target_buffer = 0

            S_time_interval = [0] * past_frame_num
            S_send_data_size = [0] * past_frame_num
            S_chunk_len = [0] * past_frame_num
            S_rebuf = [0] * past_frame_num
            S_buffer_size = [0] * past_frame_num
            S_end_delay = [0] * past_frame_num
            S_chunk_size = [0] * past_frame_num
            S_play_time_len = [0] * past_frame_num
            S_decision_flag = [0] * past_frame_num
            S_buffer_flag = [0] * past_frame_num
            S_cdn_flag = [0] * past_frame_num
            
        reward_all += reward_frame
        last_segment_reward += reward_frame
        reward_all_1 += reward_1
        reward_all_2 += reward_2
        reward_all_3 += reward_3
        reward_all_4 += reward_4

    with open('MPC_train.csv', 'w', newline='') as f:   # 如果不指定newline='',则每写入一行将有一空行被写入
        writer = csv.writer(f)
        writer.writerows(wr)
    """ with open('debug.csv', 'w', newline='') as d:   # 如果不指定newline='',则每写入一行将有一空行被写入
        writer = csv.writer(d)
        writer.writerows(debug_list) """
    return reward_all_sum

for episode in range(MAX_EPISODES):
    a = test("aaa")
    print(a,"episode: ",episode)
