import unittest
from unittest.mock import patch
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from visualizer.visualizer import Visualizer
from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.visualizer_state import VisualizerState
from visualizer.gui import GUI
from visualizer.vars import SECONDS_IN_MINUTE, MINUTES_IN_HOUR, HOURS_IN_DAY,\
    SECONDS_IN_HOUR, SECONDS_IN_DAY 

visualizer = Visualizer("end")




time1 = int(time.time())-2

toState1 = "Monitor"
toState2 = "Handler"

visualizer._visualizer_states[toState1] = VisualizerState(toState1)
visualizer._visualizer_states[toState2] = VisualizerState(toState2)
# gui = GUI(visualizer, toState1)
counter = 0
starttime = time.time()
for i in range(0,10):
    for j in range(0,random.randint(0,10)):
        counter += 1
        time2 = int(time.time())
        eventId1 = "event" + str(j)
        eventId2 = "event" + str(j) + str(j)
        vs1 = VISUALIZER_STRUCT("rule2",eventId1, "", toState1, time2, time2, "", "OptionalInfo")
        vs2 = VISUALIZER_STRUCT("rule1",eventId2, "", toState1, time2, time2, "", "OptionalInfo")
        visualizer.receive_channel.put(vs1)
        visualizer.receive_channel.put(vs2)
        if random.randint(0,2):
            vs3 = VISUALIZER_STRUCT("rule1",eventId2, toState1, toState2, time2 , time2, "", "OptionalInfo")
            visualizer.receive_channel.put(vs3)
        # Make sure the threaded put has time to execute before _update checks the queue
    # print(int(time.time() % 60 ))
    # if int(time.time() % 60 ) == 1:
        # print(visualizer._visualizer_states[toState1]._seconds_data)
        # print(visualizer._visualizer_states[toState1]._minutes_data)
    # print(i)
    time.sleep(1)

vs3 = VISUALIZER_STRUCT("rule1",eventId2, toState2, "end", time1 , int(time.time()), "", "OptionalInfo")
visualizer.receive_channel.put(vs3)
time.sleep(3)
# visualizer.shutdown()       

toState1 = "Monitor"



df = visualizer.get_seconds_data(toState1)
plt.figure(figsize=(12, 6))
for rule in df.index:
    plt.bar(np.arange(len(df.columns)), df.loc[rule], label=rule)

plt.xlabel('Column Number')
plt.ylabel('Values')
plt.title('Rules Plot')
plt.legend()
plt.xticks(labels=np.arange(len(df.columns)), ticks=df.columns)
print(df)
plt.show()

# print(counter)
# print("seconds data")

# print(visualizer._visualizer_states[toState2]._seconds_data)

# print("minutes data")
# print(visualizer._visualizer_states[toState1]._minutes_data)
# print(visualizer._visualizer_states[toState2]._minutes_data)

# print(visualizer.get_event_average_live_time(["rule1"]))

# res = list(visualizer._visualizer_states[toState1]._seconds_data.loc["rule1"])

# sum = sum(res[(int(starttime%SECONDS_IN_MINUTE)) :60])
# print(sum)
            


