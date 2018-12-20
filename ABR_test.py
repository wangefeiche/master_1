import tensorflow as tf
import numpy as np 


NN_MODEL = "/home/team/iMG/submit/results/nn_model_ep_18200.ckpt" # model path settings

class Algorithm:
     def __init__(self):
     # fill your init vars
         self.buffer_size = 0
         self.bit_rate = 0
         
     # Intial 
     def Initial(self):

             IntialVars = []
                 
             return IntialVars,

     #Define your algorithm
     def run(self, time, S_time_interval, S_send_data_size, S_chunk_len, S_rebuf, S_buffer_size, S_play_time_len,S_end_delay, S_decision_flag, S_buffer_flag,S_cdn_flag, end_of_video, cdn_newest_id,download_id,cdn_has_frame, IntialVars):

            target_buffer = 0
            th_50 = 0
            end_delay = S_end_delay[-1]
            buffer_size = S_buffer_size[-1]
            cdn_buffer = end_delay + 0.04 - buffer_size
            BITRATE = [1,1.7,2.4,3.7]
            segment_size = 0
            llast_buffer,last_buffer = 0, 0
            segment_count = 0
            llast_segment_count = 0
            bit_rate = 0
            flag_1 = 0 
            flag_2 = True
            segment_count_threshold = 0
            rebuff_flag = S_buffer_flag[-1]


            for i in range(3000):
                if S_decision_flag[-2-i]:
                    flag_1 += 1
                if flag_1 == 1 and flag_2:
                    segment_count = i+1
                    last_buffer = S_buffer_size[-2-i]
                    flag_2 = False
                elif flag_1 == 2:
                    llast_segment_count = i+1
                    llast_buffer = S_buffer_size[-2-i]
                    break
            if abs(llast_segment_count - segment_count - 50) > 1 and abs(segment_count - 50) > 1:
                cdn_rebuff_flag = True
            else:
                cdn_rebuff_flag = False
            #print(llast_segment_count,segment_count,cdn_rebuff_flag)
            if llast_buffer - last_buffer > 0 and last_buffer - buffer_size > 0 and llast_buffer < 3 :
                buffer_down_flag = True
                target_buffer = 1
            else:
                buffer_down_flag = False 
            
            for j in range(segment_count):
                if S_time_interval[-1-j] != 0:
                    if S_send_data_size[-1-j]!= 0 :
                        th_50 += S_send_data_size[-1-j]/S_time_interval[-1-j]/1000  
                        segment_size += S_send_data_size[-1-j]
            ave_throughput = th_50/50
            

            delta_segment_count = abs(segment_count-50)

            if S_time_interval[-1] != 0:
                current_bitrate = (S_send_data_size[-1]/S_time_interval[-1])/1000 
            else:
                current_bitrate = 0 

            #prediction_bitrate = 0.5*current_bitrate + 0.5*ave_throughput
            if current_bitrate != 0 and ave_throughput != 0: 
                prediction_bitrate = 1/(0.25/ave_throughput + 0.75/current_bitrate)
            else:
                prediction_bitrate = 0.45*ave_throughput + 0.55*current_bitrate
            segment_rate = segment_size/2/1000/0.8
            
            if len(cdn_has_frame[0]) <= 7:
                next_segment_rate = 0
            else:
                next_segment_rate = sum(cdn_has_frame[0][1:7])/(0.04*6)/1000

            if prediction_bitrate < next_segment_rate*BITRATE[0]:
                download_flag = 0
            elif prediction_bitrate < next_segment_rate*BITRATE[1]:
                download_flag = 1
            elif prediction_bitrate < next_segment_rate*BITRATE[2]:
                download_flag = 2
            elif prediction_bitrate < next_segment_rate*BITRATE[3]:
                download_flag = 3
            else :
                download_flag = 4
            
            if next_segment_rate == 0:
            
                if prediction_bitrate < 500:
                    if buffer_size < 3:
                        bit_rate = 0
                    else:
                        bit_rate = 1
                elif prediction_bitrate < 750:
                    if buffer_size < 2.85:
                        bit_rate = 0
                    else:
                        bit_rate = 1
                elif prediction_bitrate < 1000:
                    if buffer_size < 2.35:
                        bit_rate = 0
                    else:
                        bit_rate = 1
                elif prediction_bitrate < 1250:
                    if buffer_size < 1.2:
                        bit_rate = 0
                    else:
                        bit_rate = 1
                elif prediction_bitrate < 1500:
                    if buffer_size < 1.2:
                        bit_rate = 0
                    elif buffer_size < 3:
                        bit_rate = 1
                    else:
                        bit_rate = 2
                elif prediction_bitrate < 1750:
                    if buffer_size < 2.5:
                        bit_rate = 1
                    else:
                        bit_rate = 2
                elif prediction_bitrate < 2000:
                    if buffer_size < 1.5:
                        bit_rate = 1
                    elif buffer_size < 3:
                        bit_rate = 2
                    else:
                        bit_rate = 3
                elif prediction_bitrate < 2250:
                    if buffer_size < 1.2:
                        bit_rate = 1
                    elif buffer_size < 2.8:
                        bit_rate = 2
                    else:
                        bit_rate = 3
                elif prediction_bitrate < 2500:
                    if buffer_size < 2:
                        bit_rate = 2
                    else:
                        bit_rate = 3
                else:
                    if buffer_size < 1.5:
                        bit_rate = 2
                    else:
                        bit_rate = 3
                
                if delta_segment_count == 0 and bit_rate != 3:
                    bit_rate = bit_rate + 1
                    
            else:
                if prediction_bitrate < 500:
                    if buffer_size > 3 and download_flag <= 1:
                        bit_rate = 1
                    else:
                        bit_rate = 0
                elif prediction_bitrate < 750:
                    if buffer_size > 2.85 and download_flag <= 1:
                        bit_rate = 1
                    else:
                        bit_rate = 0
                elif prediction_bitrate < 1000:
                    if buffer_size > 2.35:
                        bit_rate = 1
                    else:
                        bit_rate = 0
                elif prediction_bitrate < 1250 :
                    if buffer_size < 1.2:
                        bit_rate = 0
                    else:
                        bit_rate = 1
                elif prediction_bitrate < 1500:
                    if buffer_size < 1.2:
                        bit_rate = 0
                    elif buffer_size < 3:
                        bit_rate = 1
                    else:
                        bit_rate = 2
                elif prediction_bitrate < 1750:
                    if buffer_size < 2.5:
                        bit_rate = 1
                    else:
                        bit_rate = 2
                elif prediction_bitrate < 2000:
                    if buffer_size < 1.5:
                        bit_rate = 1
                    elif buffer_size < 3:
                        bit_rate = 2
                    else:
                        bit_rate = 3
                elif prediction_bitrate < 2250:
                    if buffer_size < 1.2:
                        bit_rate = 1
                    elif buffer_size < 2.8:
                        bit_rate = 2
                    else:
                        bit_rate = 3
                elif prediction_bitrate < 2500:
                    if buffer_size < 2:
                        bit_rate = 2
                    else:
                        bit_rate = 3
                else:
                    if buffer_size < 1.5:
                        bit_rate = 2
                    else:
                        bit_rate = 3
                
            
            
            
            

            #target_buffer = 0
            """ if (cdn_buffer >=3 and buffer_size <= 1 and bit_rate != 0) or (buffer_down_flag and bit_rate != 0) :
                bit_rate = bit_rate - 1  """
            self.bit_rate = bit_rate
            return bit_rate, target_buffer


         # If you choose other
         #......
