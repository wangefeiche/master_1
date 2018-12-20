import tensorflow as tf


NN_MODEL = "/home/team/iMG/submit/results/nn_model_ep_18200.ckpt" # model path settings

class Algorithm:
     def __init__(self):
     # fill your init vars
         self.buffer_size = 0
         
     # Intial 
     def Initial(self):

             IntialVars = []
                 
             return IntialVars,

     #Define your algorithm
     def run(self, time, S_time_interval, S_send_data_size, S_chunk_len, S_rebuf, S_buffer_size, S_play_time_len,S_end_delay, S_decision_flag, S_buffer_flag,S_cdn_flag, end_of_video, cdn_newest_id,download_id,cdn_has_frame, IntialVars):

            target_buffer = 0
            th_10,th_20,th_30,th_40,th_50 = 0,0,0,0,0
            segment_count_threshold = 0
            fpsx2 = 50
            segment_count = 0
            bit_rate = 0
            flag = 0 
            for i in range(7000):
                if S_decision_flag[-2-i]:
                    segment_count = i+1
                    flag += 1
                if flag == 1:
                    break
            th_flag = 0
            for j in range(segment_count):
                if S_time_interval[-1-j] != 0:
                    if S_send_data_size[-1-j]!= 0 :
                        if th_flag < 10:
                            th_10 += S_send_data_size[-1-j]/S_time_interval[-1-j]/1000
                        elif th_flag < 20:
                            th_20 += S_send_data_size[-1-j]/S_time_interval[-1-j]/1000
                        elif th_flag < 30:
                            th_30 += S_send_data_size[-1-j]/S_time_interval[-1-j]/1000
                        elif th_flag < 40:
                            th_40 += S_send_data_size[-1-j]/S_time_interval[-1-j]/1000
                        elif th_flag < 50:
                            th_50 += S_send_data_size[-1-j]/S_time_interval[-1-j]/1000
                        th_flag += 1
            th_10 = th_10/10
            th_20 = th_20/10
            th_30 = th_30/10
            th_40 = th_40/10
            th_50 = th_50/10
            ave_throughput = (th_10+th_20+th_30+th_40+th_50)/5
            err = max(abs(ave_throughput-th_10),abs(ave_throughput-th_20),abs(ave_throughput-th_30),abs(ave_throughput-th_40),abs(ave_throughput-th_50))
            #prediction_bitrate = ave_throughput/(1+err/ave_throughput)
            #print(ave_throughput)
            delta_segment_count = abs(segment_count-50)
            if delta_segment_count <= 0:
                delta_download_time = 0
            else:
                delta_download_time = 0.4

            buffer_size = S_buffer_size[-1]

            if S_time_interval[-1] != 0:
                current_bitrate = (S_send_data_size[-1]/S_time_interval[-1])/1000 
            else:
                current_bitrate = 0 

            #prediction_bitrate = 0.45*ave_throughput + 0.55*current_bitrate
            if ave_throughput != 0: 
                prediction_bitrate = ave_throughput/(1+err/ave_throughput)
            else:
                prediction_bitrate = current_bitrate
            
            download_time_1 = 500*2/prediction_bitrate + delta_download_time
            download_time_2 = 850*2/prediction_bitrate + delta_download_time
            download_time_3 = 1200*2/prediction_bitrate + delta_download_time
            download_time_4 = 1850*2/prediction_bitrate + delta_download_time

            q_1 = 500*2/1000 - 1.5*max(0,download_time_1 - buffer_size)
            q_2 = 850*2/1000 - 1.5*max(0,download_time_2 - buffer_size)
            q_3 = 1200*2/1000 - 1.5*max(0,download_time_3 - buffer_size)
            q_4 = 1850*2/1000 - 1.5*max(0,download_time_4 - buffer_size)
            q_max = max(q_1,q_2,q_3,q_4)
            #q_list = q_list.sort()
            if q_max == q_1:
                bit_rate = 0
            elif q_max == q_2:
                bit_rate = 1
            elif q_max == q_3:
                bit_rate = 2
            else:
                bit_rate = 3

            return bit_rate, target_buffer


         # If you choose other
         #......
