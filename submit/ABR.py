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
    
             if S_time_interval[-1] != 0:
                 net_bitrate = (S_send_data_size[-1]/S_time_interval[-1])/1000 
             else:
                 net_bitrate = 0  

             if S_buffer_size[-1] < 0.5:
                 bit_rate = 0
             elif S_buffer_size[-1] >= 2.5:
                 bit_rate = 3
             elif S_buffer_size[-1] >= 1:
                 if S_buffer_size >=1.5 and net_bitrate >= 1800:
                     bit_rate = 3
                 else:
                     bit_rate = 2 
             else:
                 if S_buffer_size[-1] >=1 and net_bitrate >= 1200:
                     bit_rate = 2 
                 else:
                     bit_rate = 1
             target_buffer = 0
            
             return bit_rate, target_buffer


         # If you choose other
         #......
