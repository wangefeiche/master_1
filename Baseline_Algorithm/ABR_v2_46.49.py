import tensorflow as tf


NN_MODEL = "/home/team/iMG/submit/results/nn_model_ep_18200.ckpt" # model path settings

class Algorithm:
     def __init__(self):
     # fill your init vars
         self.buffer_size = 0
         
     # Intial 
     def Initial(self):

             IntialVars = []
                 
             return IntialVars

     #Define your algorithm
     def run(self, time, S_time_interval, S_send_data_size, S_chunk_len, S_rebuf, S_buffer_size, S_play_time_len,S_end_delay, S_decision_flag, S_buffer_flag,S_cdn_flag, end_of_video, cdn_newest_id,download_id,cdn_has_frame, IntialVars):

            th = 0
            segment_count_threshold = 1
            segment_count = 0
            flag = 0
            fpsx = 25
            for i in range(7000):
                if S_send_data_size[-1-i] != 0:
                    flag += 1
                if flag == fpsx:
                    segment_count = i+1
                    break
            for j in range(segment_count):
                if S_time_interval[-1-j] != 0:
                    th += S_send_data_size[-1-j]/S_time_interval[-1-j]/1000000
            delta_segment_count = abs(segment_count-fpsx)
            ave_throughput = th/fpsx
            if S_time_interval[-1]!=0:
                ave_throughput = 0.4*ave_throughput+0.6*S_send_data_size[-1]/S_time_interval[-1]/1000000
            else:
                pass
            #ave_throughput = 0.5*ave_throughput+0.5*
            buffer_size = S_buffer_size[-1]
            #print(ave_throughput)
            if ave_throughput <= 0.5:
                bit_rate = 0
            elif ave_throughput <= 0.85:
                if delta_segment_count <= segment_count_threshold:
                    if buffer_size < 0.5:
                        bit_rate = 0
                    else: 
                        bit_rate = 0
                else:
                    if buffer_size < 0.5:
                        bit_rate = 0
                    else: 
                        bit_rate = 1
            elif ave_throughput <= 1.2:
                if delta_segment_count <= segment_count_threshold:
                    if buffer_size < 0.5:
                        bit_rate = 0
                    else: 
                        bit_rate = 1
                else:
                    if buffer_size < 0.5:
                        bit_rate = 1
                    else: 
                        bit_rate = 2
            elif ave_throughput <= 1.8:
                if delta_segment_count <= segment_count_threshold:
                    if buffer_size < 0.5:
                        bit_rate = 1
                    else: 
                        bit_rate = 2
                else:
                    if buffer_size < 0.5:
                        bit_rate = 2
                    else: 
                        bit_rate = 3
            else:
                if delta_segment_count <= segment_count_threshold:
                    if buffer_size < 0.5:
                        bit_rate = 2
                    else: 
                        bit_rate = 3
                else:
                    bit_rate = 3



            target_buffer = 0
            
            return bit_rate, target_buffer


         # If you choose other
         #......
