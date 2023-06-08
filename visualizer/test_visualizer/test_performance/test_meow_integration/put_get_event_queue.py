import time
import threading
import multiprocessing

from visualizer.visualizer import Visualizer
from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.visualizer_state import VisualizerState
from meow_base.visualizer_adapter.to_visualizer import ToVisualizer
from visualizer.i_visualizer_receive_data import IVisualizerReceiveData

channel = multiprocessing.Queue()

visualizer_info = IVisualizerReceiveData()
visualizer_info.receive_channel = channel

meow_adapter = ToVisualizer(visualizer_info)

event_message = {'file_hash': 'c40d60745273f914947df98d7d0290f24ec7a005ab11c525bbd95b800f779f4f', 'monitor_base': 'test_monitor_base', 'event_path': 'test_monitor_base/start/1_7_2.txt', 'event_type': 'watchdog', 'event_rule': "rule1", 'event_time': 1686209645.2814605}
job_path_name = "job_path_info"
count = 100000
runs = 10


total_work_time = 0
for i in range(0,runs):
    # print("queue size before: ", channel.qsize())
    start_time = time.time()
    # print("start in second: ", start_time % 60)
    for j in range(0, count):
        # event_path = event_message + str(i)
        job_path = job_path_name + str(j)
        meow_adapter.from_monitor_message(event_message)

    end_time = time.time()
    work_time = end_time - start_time
    total_work_time += work_time

    # print("done in second: ", end_time % 60)
    # print("putting 100.000 events in queue took: ", end_time - start_time, " seconds")
    # print("Queue size =",channel.qsize())
    # print("Time to put one event in queue from meow: ", work_time / 100000, " seconds")

print("putting", count * runs ,"events in queue took: ", total_work_time, " seconds")
print("Average time to put one event in queue from meow: ", total_work_time / (count * runs), " seconds")
print("Average time to put one event in queue from meow: ", (total_work_time / (count * runs) * 1000000) , " microseconds")
# microseconds are 1.000.000'th of a second
print("Timing how long 1.000.000 events take to flush from queue")
print("Starting to clear queue, might take a minute")
start_time = time.time()

while channel.qsize() > 0:
    a = channel.get()

print("done clearing queue")
end_time = time.time()
print("clearing queue took: ", end_time - start_time, " seconds")

# time.sleep(1)

channel.close()
print("queue size = ", channel.qsize())
# channel.terminate()
print("closed")
# raise SystemExit
# exit()

channel.join_thread()

# for i in range(1, 3):
#     event_path = event_path_name + str(i)
#     job_path = job_path_name + str(i)

#     meow_adapter.from_handler_path(job_path)





