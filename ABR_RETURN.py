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
            th_10, th_20, th_30, th_40, th_50= 0,0,0,0,0
            th_ave = 0
            segment_count_threshold = 0
            fpsx2 = 50
            segment_count = 0
            bit_rate = 0
            flag = 0 
            th_flag = 0
            segment_size = 0
            segment_rate = 0
            
            if len(cdn_has_frame[0]) <= 7:
                next_segment_rate = 0
            else:
                next_segment_rate = sum(cdn_has_frame[0][1:7])/(0.04*6)/1000


            for i in range(7000):
                if S_decision_flag[-2-i]:
                    segment_count = i+1
                    flag += 1
                if flag == 1:
                    break

            for j in range(segment_count):
                if S_time_interval[-1-j] != 0:
                    if S_send_data_size[-1-j]!= 0 :
                        segment_size += S_send_data_size[-1-j]
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

            
            target_buffer = 0
            th_10 = 0
            th_25 = 0
            th_50 = 0
            end_delay = S_end_delay[-1]
            segment_count_threshold = 0
            fpsx2 = 50
            segment_count = 0
            bit_rate = 0
            flag = 0 

            

            # print(var_bitrate)

            for i in range(7000):
                if S_decision_flag[-2-i]:
                    segment_count = i+1
                    flag += 1
                if flag == 1:
                    break
            j_flag = 0
            for j in range(segment_count):
                if S_time_interval[-1-j] != 0:
                    if S_send_data_size[-1-j]!= 0 :
                        th_50 += S_send_data_size[-1-j]/S_time_interval[-1-j]/1000  
            ave_throughput = (th_50)/50
            # if th_10 != 0 and th_25 != 0 and th_50 != 0 :
            #     ave_throughput = 1/(10*0.5/th_10+15*0.5/th_25+25**0.5/th_50)
            # else:
            #     ave_throughput = (th_10*0.5)/10+ (th_25*0.3)/15+(th_50*0.2)/25

            delta_segment_count = abs(segment_count-50)
            #delta_segment_count = delta_delay_buffer
            

            if S_time_interval[-1] != 0:
                current_bitrate = (S_send_data_size[-1]/S_time_interval[-1])/1000 
            else:
                current_bitrate = 0 

            # prediction_bitrate = 0.2*ave_throughput + 0.8*current_bitrate
            if current_bitrate != 0 and ave_throughput != 0: 
                prediction_bitrate = 1/(0.25/ave_throughput + 0.75/current_bitrate)
            else:
                prediction_bitrate = 0.45*ave_throughput + 0.55*current_bitrate

            segment_rate = segment_size/2/1000

            return th_list, buffer_size, segment_count, prediction_bitrate,segment_rate,ave_throughput,current_bitrate,next_segment_rate


         # If you choose other
         #......
