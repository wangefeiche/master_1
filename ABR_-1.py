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
            fpsx2 = 50
            segment_count = 0
            flag = 0 
            for i in range(7000):
                if S_decision_flag[-2-i]:
                    segment_count = i+1
                    flag += 1
                if flag == 1:
                    break
            for j in range(segment_count):
                if S_time_interval[-1-j] != 0:
                    th += S_send_data_size[-1-j]/S_time_interval[-1-j]/1000
            ave_throughput = th/fpsx2
            buffer_size = S_buffer_size[-1]

            if buffer_size <= 0.5:
                bit_rate = 0 
            elif buffer_size >= 2.5:
                bit_rate = 3
            elif buffer_size >= 1:
                if buffer_size >=2 and ave_throughput >= 1250:
                    bit_rate = 3
                elif buffer_size >=1.5 and ave_throughput >= 1500:
                    bit_rate = 3
                else:
                    bit_rate = 2
            else:
                bit_rate = 1



            target_buffer = 0
            
            return bit_rate, target_buffer


         # If you choose other
         #......
