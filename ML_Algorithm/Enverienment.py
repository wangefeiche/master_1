import numpy as np
import time



bufferLength = 0 # the client buffer length
downloadStart = 0
downloadEnd = 0
segmentDuration = 1
#==========预处理=========
SegmentSize_360s_list = []
with open("SegmentSize_360s.txt",'r') as SegmentSize_360s_readfile:
    n=0
    while True:
        lines = SegmentSize_360s_readfile.readline() # 整行读取数据
        if not lines:
            break
        i = lines.split()
        SegmentSize_360s_list.append([float(x) for x in i])
        n = n+1
#print(SegmentSize_360s_list)
SegmentSize_360s_list = [[float(x) for x in row] for row in SegmentSize_360s_list]

DlRxPhyStats_time, DlRxPhyStats_tbsize = [], []
with open('sim0_cl0_throughputLog.txt','r') as DlRxPhyStats_to_read:
    n=0
    while True:
        lines = DlRxPhyStats_to_read.readline() # 整行读取数据
        if not lines:
            break
        
        i = lines.split()
        DlRxPhyStats_time.append(float(i[0]))
        DlRxPhyStats_tbsize.append(float(i[1])*8)
        n = n+1

th_time, th = [],[]
th_count = 0
th_size = 0
for i in range(len(DlRxPhyStats_time)):
    time_temp = DlRxPhyStats_time[th_count]
    if  DlRxPhyStats_time[i] - time_temp > 0.1:
        time_delta = DlRxPhyStats_time[i] - time_temp
        th_count = i
        th_time.append(DlRxPhyStats_time[i])
        th.append(th_size/time_delta)
        th_size = 0
    else:
        th_size += DlRxPhyStats_tbsize[i]
#======================================================================

class Maze():
    def __init__(self):
        self.action_space = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.n_actions = len(self.action_space) 
        self.n_features = 2
        self.sg_count = 0
        self.T = 0
        self.B = 0
        self.observation = np.array([0,0])
        
        

    



    def step(self, action):
        #self.action = action 
        segmentSize = SegmentSize_360s_list[action][self.sg_count]*segmentDuration*8
        downloadStart = DlRxPhyStats_time[self.T]
        downloadEnd = 0
        size_sum = 0
        T_ = self.T
        B_ = self.B
        R = 0
        for data_size in DlRxPhyStats_tbsize[T_:]:
            if size_sum < segmentSize:
                size_sum = size_sum + data_size
                T_ = T_ + 1
            else:
                downloadEnd = DlRxPhyStats_time[T_]
                break
        #print("===============",downloadStart,downloadEnd)
        bit_rate = segmentSize/(downloadEnd-downloadStart)
        if self.sg_count == 0:
            B_ = B_ + segmentDuration
        else:
            B_ = B_ + segmentDuration - (downloadEnd-downloadStart)

        #self.observation = np.array([downloadStart,self.B])
        self.observation = np.array([bit_rate,B_])
        if B_ > 1 and B_ < 1.5 :
            if self.sg_count%5 == 0:#T_ == len(DlRxPhyStats_tbsize):
                R = 1
                done = False
            else:
                R = 0.1
                done = False
        else:
            if self.sg_count == 0 and downloadEnd-downloadStart < 1 :
                R = 0.1
                done = False
            else:
                R = -1
                done = True
        
        info = np.array([self.B, B_, downloadEnd-downloadStart])
        
        
        s_ = self.observation
        s_[0] = s_[0]/10000000
        #s_[1] = s_[1]-1
        #next_coords = self.canvas.coords(self.rect)  # next state
        #s_ = np.array([next_coords[0]/(MAZE_W*UNIT),next_coords[1]/(MAZE_H*UNIT)])
        reward = R 
        if done:
            self.T=0
            self.B=0
            self.sg_count=0
        else:
            self.T=T_
            self.B=B_
            self.sg_count += 1
        return s_, reward, done, info

    


