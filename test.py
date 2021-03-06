import matplotlib.pyplot as plt 

video_size_file = './video_trace/AsianCup_China_Uzbekistan/frame_trace_'
BITRATE_LEVELS = 4
FPS = 25

video_size = {}  # in bytes
cdn_arrive_time = {}
gop_time_len = {}
gop_flag = {}


fig = plt.figure(figsize=(16,12),dpi=80)
plt.ion()
plt.xlabel("time")
plt.axis('off')

for bitrate in range(BITRATE_LEVELS):
    video_size[bitrate] = []
    cdn_arrive_time[bitrate] = []
    gop_time_len[bitrate] = []
    gop_flag[bitrate] = []
    cnt = 0
    with open(video_size_file + str(bitrate)) as f:
        for line in f:
            #print(line.split(), bitrate)
            video_size[bitrate].append(float(line.split()[1]))
            gop_time_len[bitrate].append(float(1/FPS))
            gop_flag[bitrate].append(int(float(line.split()[2])))
            cdn_arrive_time[bitrate].append(float(line.split()[0]))
            cnt += 1


    DlRxPhyStats_time = cdn_arrive_time[bitrate]
    DlRxPhyStats_tbsize = video_size[bitrate]
    th_time, th = [],[]
    th_count = 0
    th_size = 0
    for i in range(len(DlRxPhyStats_time)):
        time_temp = DlRxPhyStats_time[th_count]
        if  DlRxPhyStats_time[i] - time_temp > 20:
            time_delta = DlRxPhyStats_time[i] - time_temp
            th_count = i
            th_time.append(DlRxPhyStats_time[i])
            th.append(th_size/time_delta/1000000)
            th_size = 0
        else:
            th_size += DlRxPhyStats_tbsize[i]
    fig.add_subplot(4,1,bitrate+1)
    plt.plot(th_time, th)
    plt.ylabel('th')
    plt.xlabel('time')
plt.savefig("log.png")
#plt.show()