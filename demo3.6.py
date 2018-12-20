''' Demo SDK for LiveStreaming
    Author Dan Yang
    Time 2018-10-15
    For LiveStreaming Game'''
# import the env from pip
import LiveStreamingEnv.env as env
import LiveStreamingEnv.load_trace as load_trace
import matplotlib.pyplot as plt
import time
import numpy as np
# path setting
TRAIN_TRACES = './network_trace/'   #train trace path setting,
video_size_file = './video_trace/Fengtimo_2018_11_3/frame_trace_'      #video trace path setting,
LogFile_Path = "./log/"                #log file trace path setting,
# Debug Mode: if True, You can see the debug info in the logfile
#             if False, no log ,but the training speed is high
DEBUG = False
DRAW = True#False
# load the trace
all_cooked_time, all_cooked_bw, all_file_names = load_trace.load_trace(TRAIN_TRACES)
#random_seed 
random_seed = 2
video_count = 0
FPS = 25
frame_time_len = 0.04
#init the environment
#setting one:
#     1,all_cooked_time : timestamp
#     2,all_cooked_bw   : throughput
#     3,all_cooked_rtt  : rtt
#     4,agent_id        : random_seed
#     5,logfile_path    : logfile_path
#     6,VIDEO_SIZE_FILE : Video Size File Path
#     7,Debug Setting   : Debug
net_env = env.Environment(all_cooked_time=all_cooked_time,
			  all_cooked_bw=all_cooked_bw,
			  random_seed=random_seed,
			  logfile_path=LogFile_Path,
			  VIDEO_SIZE_FILE=video_size_file,
			  Debug = DEBUG)

BIT_RATE      = [500.0,850.0,1200.0,1850.0] # bps
TARGET_BUFFER = [2.0,3.0]   # seconds
# ABR setting
RESEVOIR = 0.5
CUSHION  = 2
DELTA = 0


cnt = 0
# defalut setting
last_bit_rate = 0
bit_rate = 0
target_buffer = 0
# QOE setting
reward_frame = 0
reward_all = 0
reward_all_1 = 0
reward_all_2 = 0
reward_all_3 = 0
SMOOTH_PENALTY= 0.02 
REBUF_PENALTY = 1.5 
LANTENCY_PENALTY = 0.005 

# plot info
idx = 0
id_list = []
download_rate_list = []
bit_rate_record = []
buffer_record = []
throughput_record = []
segment_ave_list = []
# plot the real time image
if DRAW:
    fig = plt.figure(figsize=(16,12),dpi=80)
    plt.ion()
    plt.xlabel("time")
    plt.axis('off')

segment_count = 0
segment_size = []
segment_time = []
segment_ave = 0
frame_count = 0
cdn_flag_count = 0
play_time = 0
while True:
        frame_count += 1
        reward_frame = 0
        reward_1 = 0
        reward_2 = 0
        reward_3 = 0
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

        #
        time, time_interval, send_data_size, chunk_len, rebuf, buffer_size, play_time_len,end_delay,cdn_newest_id, downlaod_id,cdn_has_frame,decision_flag, buffer_flag,cdn_flag, end_of_video = net_env.get_video_frame(bit_rate,target_buffer)
        cnt += 1
        if time_interval != 0:
            segment_size.append(send_data_size)
            segment_time.append(time_interval)
            # plot download rae
            download_rate_list.append(send_data_size/time_interval/1000)
            # plot bit_rate 
            id_list.append(idx)
            idx += time_interval
            play_time += play_time_len
            bit_rate_record.append(BIT_RATE[bit_rate])
            if len(segment_ave_list) == 0:
                segment_ave_list.append(sum(download_rate_list[-10:])/10)
            else:
                if decision_flag:
                    segment_ave_list.append(sum(download_rate_list[-10:])/10)
                else:
                    segment_ave_list.append(segment_ave_list[-1])
            
            if cdn_flag:
                cdn_flag_count += 1
            
            # plot buffer 
            buffer_record.append(buffer_size)
            # plot throughput 
            trace_idx = net_env.get_trace_id()
            #print(trace_idx, idx,play_time,len(all_cooked_bw[trace_idx]),decision_flag,cdn_flag,rebuf,buffer_size,end_delay,segment_count,BIT_RATE[bit_rate],download_rate_list[-1],reward_all)
            if frame_count%2 ==0: #decision_flag:
                segment_ave = sum(segment_size)/(sum(segment_time))
                segment_count = 0
                segment_size = []
                segment_time = []
            else:
                segment_count+=1
            if int(idx/0.5) < len(all_cooked_bw[trace_idx]) and int(idx/0.5)<5880:
                throughput_record.append(all_cooked_bw[trace_idx][int(idx/0.5)] * 1000 )
            else:
                break
        if not cdn_flag:
            reward_frame = frame_time_len * float(BIT_RATE[bit_rate]) / 1000  - REBUF_PENALTY * rebuf - LANTENCY_PENALTY * end_delay
            reward_1 = frame_time_len * float(BIT_RATE[bit_rate]) / 1000
            reward_2 = REBUF_PENALTY * rebuf
            reward_3 = LANTENCY_PENALTY * end_delay
        else:
            reward_frame = -(REBUF_PENALTY * rebuf)
            reward_1 = 0
            reward_2 = REBUF_PENALTY * rebuf
            reward_3 = 0
        if decision_flag or end_of_video:
            # reward formate = play_time * BIT_RATE - 4.3 * rebuf - 1.2 * end_delay
            reward_frame += -1 * SMOOTH_PENALTY * (abs(BIT_RATE[bit_rate] - BIT_RATE[last_bit_rate]) / 1000)
            # last_bit_rate
            last_bit_rate = bit_rate

       
            
            # draw setting
            if DRAW:
                ax = fig.add_subplot(511)
                plt.ylabel("BIT_RATE")
                plt.ylim(300,2000)
                plt.plot(id_list,bit_rate_record,'-r')
                
                ax = fig.add_subplot(512)
                plt.ylabel("Buffer_size")
                plt.ylim(0,7)
                plt.plot(id_list,buffer_record,'-b')

                ax = fig.add_subplot(513)
                plt.ylabel("throughput")
                plt.ylim(0,4000)
                plt.plot(id_list,throughput_record,'-g')

                ax = fig.add_subplot(514)
                plt.ylabel("download_rate")
                plt.ylim(0,4000)
                plt.plot(id_list,throughput_record,'-r')

                ax = fig.add_subplot(515)
                plt.ylabel("estimate_rate")
                plt.ylim(0,4000)
                plt.plot(id_list,segment_ave_list,'-r')

                #plt.draw()
                #plt.pause(0.0001)

        #print(reward_frame)

        # -------------------------------------------Your Algorithm ------------------------------------------- 
        # which part is the althgrothm part ,the buffer based , 
        # if the buffer is enough ,choose the high quality
        # if the buffer is danger, choose the low  quality
        # if there is no rebuf ,choose the low target_buffer
        if decision_flag:

            if buffer_size < RESEVOIR:
                bit_rate = 0
            else:
                if segment_ave <= (BIT_RATE[0]*1000+DELTA):
                    bit_rate = 0
                elif segment_ave <= (BIT_RATE[1]*1000+DELTA):
                    bit_rate = 0
                elif segment_ave <= (BIT_RATE[2]*1000+DELTA):
                    bit_rate = 1
                elif segment_ave <= (BIT_RATE[3]*1000+DELTA):
                    bit_rate = 2
                else:
                    bit_rate = 3
            if cdn_flag_count > 2 and bit_rate < 3:
                bit_rate += 1
            cdn_flag_count = 0


            if buffer_size < 0.5:
                bit_rate = 0
            elif buffer_size >= 2.5:
                bit_rate = 3
            elif buffer_size >= 1:
                bit_rate = 2
            else: 
                bit_rate = 1

        #bit_rate = 3
        target_buffer = 1
        # ------------------------------------------- End  ------------------------------------------- 

        reward_all += reward_frame
        reward_all_1 += reward_1
        reward_all_2 += reward_2
        reward_all_3 += reward_3
        if end_of_video:
            # Narrow the range of results
            break
            
if DRAW:
    #plt.show()
    plt.savefig("log.png")
print(reward_all,reward_all_1,reward_all_2,reward_all_3)

