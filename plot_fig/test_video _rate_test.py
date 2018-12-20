import matplotlib.pyplot as plt 
import csv

choose = 1
if choose == 0:
    video_size_file = './video_trace_2/game/frame_trace_'
elif choose == 1:
    video_size_file = './video_trace_2/room/frame_trace_'
else:
    video_size_file = './video_trace_2/sports/frame_trace_'
BITRATE_LEVELS = 1
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
    wr = [['th_time','th']]
    for i in range(len(DlRxPhyStats_time)):
        time_temp = DlRxPhyStats_time[th_count]
        if  i % 50 == 0:
            time_delta = DlRxPhyStats_time[i] - time_temp
            th_count = i
            th_time.append(DlRxPhyStats_time[i])
            th.append(th_size/2/1000000)
            wr.append([DlRxPhyStats_time[i],th_size/2/1000])
            th_size = 0
        else:
            th_size += DlRxPhyStats_tbsize[i]

    new_size = []
    new_time = []
    for i in range(len(DlRxPhyStats_time)):
        if i % 50 == 1:
            new_size.append(DlRxPhyStats_tbsize[i])
            new_time.append(DlRxPhyStats_time[i])
    
    fig.add_subplot(2,1,1)
    plt.ylim((0,(bitrate+1)*3))
    plt.plot(th_time, th)
    plt.ylabel('th')
    plt.xlabel('time')
    fig.add_subplot(2,1,2)
    plt.plot(new_time, new_size)
    plt.ylabel('new_size')
    plt.xlabel('new_time')


if choose == 0:
    plt.savefig("./video_fig/v2/game.png")
elif choose == 1:
    plt.savefig("./video_fig/v2/room.png")
else:
    plt.savefig("./video_fig/v2/sports.png")

with open('video_trace_2_room.csv', 'w', newline='') as f:   # 如果不指定newline='',则每写入一行将有一空行被写入
        writer = csv.writer(f)
        writer.writerows(wr)
#plt.show()