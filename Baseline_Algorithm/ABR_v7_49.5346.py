import tensorflow as tf
import numpy as np 


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
            th_10 = 0
            th_25 = 0
            th_50 = 0
            segment_count_threshold = 0
            fpsx2 = 50
            net_bitrate = [] 
            segment_count = 0
            bit_rate = 0
            flag = 0 

            for i in range(50):
                if S_time_interval[-1-i] != 0:
                    net_bitrate.append(S_send_data_size[-1-i]/S_time_interval[-1-i]/1000)
            var_bitrate = np.var(net_bitrate)

            # print(var_bitrate)

            for i in range(7000):
                if S_decision_flag[-2-i]:
                    segment_count = i+1
                    flag += 1
                if flag == 1:
                    break
            for j in range(segment_count):
                if S_time_interval[-1-j] != 0:
                    if S_send_data_size[-1-j]!= 0 and segment_count <= 10:
                        th_10 += S_send_data_size[-1-j]/S_time_interval[-1-j]/1000   
                    elif  S_send_data_size[-1-j]!= 0 and segment_count <= 25:
                        th_25 += S_send_data_size[-1-j]/S_time_interval[-1-j]/1000
                    else:
                        th_50 += S_send_data_size[-1-j]/S_time_interval[-1-j]/1000  
            ave_throughput = (th_10*0.5)/10+ (th_25*0.3)/15+(th_50*0.2)/25
            # if th_10 != 0 and th_25 != 0 and th_50 != 0 :
            #     ave_throughput = 1/(10*0.5/th_10+15*0.5/th_25+25**0.5/th_50)
            # else:
            #     ave_throughput = (th_10*0.5)/10+ (th_25*0.3)/15+(th_50*0.2)/25

            delta_segment_count = abs(segment_count-50)
            
            buffer_size = S_buffer_size[-1]

            if S_time_interval[-1] != 0:
                current_bitrate = (S_send_data_size[-1]/S_time_interval[-1])/1000 
            else:
                current_bitrate = 0 

            # prediction_bitrate = 0.2*ave_throughput + 0.8*current_bitrate
            if current_bitrate != 0 and ave_throughput != 0: 
                prediction_bitrate = 1/(0.25/ave_throughput + 0.75/current_bitrate)
            else:
                prediction_bitrate = 0.45*ave_throughput + 0.55*current_bitrate

            # print("last_bitrate:",current_bitrate,"prediction_bitrate:",prediction_bitrate)

            if prediction_bitrate <= 500:
                if delta_segment_count <= segment_count_threshold:
                    bit_rate = 0
                else:
                    if buffer_size >= 2.35:
                        bit_rate = 1
                    else:
                        bit_rate = 0

            elif prediction_bitrate <= 850:
                if delta_segment_count <= segment_count_threshold:
                    if buffer_size >= 2.35:
                        bit_rate = 1
                    elif buffer_size >= 0.9:
                        bit_rate = 0
                else:
                    if buffer_size >= 2.35:
                        bit_rate = 2
                    elif buffer_size >= 0.9:
                        bit_rate = 1
                    else:
                        bit_rate = 0

            elif prediction_bitrate <= 1250:
                if delta_segment_count <= segment_count_threshold:
                    if buffer_size >= 2.35:
                        bit_rate = 2
                    elif buffer_size >= 0.9:
                        bit_rate = 1
                    else:
                        bit_rate = 0
                else:
                    if buffer_size >= 2.35:
                        bit_rate = 3
                    elif buffer_size >= 0.9:
                        bit_rate = 2
                    else:
                        bit_rate = 1 
                 
            elif prediction_bitrate <= 1550:
                if delta_segment_count <= segment_count_threshold:
                    if buffer_size >= 2.35:
                        bit_rate = 3
                    else:
                        bit_rate = 2
                else:
                    if buffer_size >= 1.85:
                        bit_rate = 3
                    else:
                        bit_rate = 2

            elif prediction_bitrate <= 1850:
                if delta_segment_count <= segment_count_threshold:
                    if buffer_size >= 1.85:
                        bit_rate = 3
                    else:
                        bit_rate = 2
                else:
                    if buffer_size >= 0.9:
                        bit_rate = 3
                    else:
                        bit_rate = 2
             
            elif prediction_bitrate <= 2150:
                if delta_segment_count <= segment_count_threshold:
                    if buffer_size >= 1.35:
                        bit_rate = 3
                    else:
                        bit_rate = 2 
                else:
                    bit_rate = 3

            elif prediction_bitrate <= 2500:
                if delta_segment_count <= segment_count_threshold:
                    if buffer_size >= 0.9:
                        bit_rate = 3
                    else:
                        bit_rate = 2 
                else:
                    bit_rate = 3
            
            elif prediction_bitrate <= 3000:
                if delta_segment_count <= segment_count_threshold:
                    if buffer_size >= 0.4:
                        bit_rate = 3
                    else:
                        bit_rate = 2 
                else:
                    bit_rate = 3

            else:
                bit_rate = 3

            # if prediction_bitrate >= 1000:
            #     target_buffer = 0
            # else:
            #     target_buffer = 1
            # target_buffer = 0
            
            
            return bit_rate, target_buffer


         # If you choose other
         #......
