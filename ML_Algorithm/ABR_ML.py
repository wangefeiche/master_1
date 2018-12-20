import tensorflow as tf
import numpy as np 
from infer import predict

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
            th_10, th_20, th_30, th_40, th_50= 0,0,0,0,0
            th_ave = 0
            segment_count_threshold = 0
            fpsx2 = 50
            segment_count = 0
            bit_rate = 0
            flag = 0 
            th_flag = 0


            for i in range(7000):
                if S_decision_flag[-2-i]:
                    segment_count = i+1
                    flag += 1
                if flag == 1:
                    break

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

            for j in range(segment_count):
                if S_time_interval[-1-j] != 0:
                    if S_send_data_size[-1-j]!= 0 :
                        th_ave += S_send_data_size[-1-j]/S_time_interval[-1-j]/1000  
            ave_throughput = (th_ave*0.2)/25
            

            delta_segment_count = abs(segment_count-50)
            
            buffer_size = S_buffer_size[-1]

            th_list = [th_10, th_20, th_30, th_40, th_50]

            input_list = th_list + [buffer_size,segment_count]

            qoe_1 = predict(input_list + [0])
            qoe_2 = predict(input_list + [1])
            qoe_3 = predict(input_list + [2])
            qoe_4 = predict(input_list + [3])
            qoe_max = max(qoe_1,qoe_2,qoe_3,qoe_4)
            #print(input_list + [0])
            #print(qoe_1,qoe_2,qoe_3,qoe_4)
            if qoe_max == qoe_1:
                bit_rate = 0
            elif qoe_max == qoe_2:
                bit_rate = 1
            elif qoe_max == qoe_3:
                bit_rate = 2
            elif qoe_max == qoe_4:
                bit_rate = 3
            

                



            return bit_rate, target_buffer


         # If you choose other
         #......
