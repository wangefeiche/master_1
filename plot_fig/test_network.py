import matplotlib.pyplot as plt 
import LiveStreamingEnv.load_trace as load_trace

TRAIN_TRACES = './network_trace_2/'
BITRATE_LEVELS = 4
FPS = 25

all_cooked_time, all_cooked_bw, all_file_names = load_trace.load_trace(TRAIN_TRACES)




for trace_idx in range(len(all_cooked_time)):
    fig = plt.figure(figsize=(16,12),dpi=80)
    cooked_time = all_cooked_time[trace_idx]
    cooked_bw = all_cooked_bw[trace_idx]
    plt.plot(cooked_time, cooked_bw)
    plt.ylim((0,10))
    plt.ylabel('th')
    plt.xlabel('time')
    plt.savefig("./network_fig/v2/network_"+ str(trace_idx) +".png")

#plt.show()