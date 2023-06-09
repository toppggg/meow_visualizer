import unittest
from unittest.mock import patch
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import threading

from visualizer.visualizer import Visualizer
from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.visualizer_state import VisualizerState
from visualizer.GUI.gui import GUI
from visualizer.vars import SECONDS_IN_MINUTE, MINUTES_IN_HOUR, HOURS_IN_DAY,\
    SECONDS_IN_HOUR, SECONDS_IN_DAY 

visualizer = Visualizer("end")

time1 = int(time.time())-2

toState1 = "Monitor"
toState2 = "Handler"
toState3 = "end"

visualizer._visualizer_states[toState1] = VisualizerState(toState1)
visualizer._visualizer_states[toState2] = VisualizerState(toState2)

# from spam import Spam
# gui = Spam(visualizer)
gui = GUI(visualizer, toState1)

time0 = str(time.time())
counter = 0
starttime = time.time()

arr2d = [[] for i in range(100000)]

def monitor () : 
    for j in range(0,100000):
        # monitorevents:list[VISUALIZER_STRUCT] = []
        for i in range(0,random.randint(0,50) ) :
            time1 = str(time.time())
            vs1 = VISUALIZER_STRUCT("rule" + str(i), "i" + str(i) + "j" + str(j), "", toState1, time0, time1, "", "OptionalInfo")
            visualizer.receive_channel.put(vs1)
            # monitorevents = monitorevents + [vs1]
            arr2d[j].append(vs1)
        time.sleep(0.2)

    return 1

t = threading.Thread(target=monitor)
t.start()

def handler() :
    for j in range(0,100000):
        time.sleep(0.1)    
        for visualizer_struct in arr2d[j] :
                time2 = str(time.time())
                vs2 = visualizer_struct
                vs2.previous_state = toState1
                vs2.current_state = toState2
                vs2.event_time = time2
                # print(vs2)
                visualizer.receive_channel.put(vs2)
        if j < 100:
            time.sleep(0.1)
        time.sleep(0.2) 

time.sleep(5)
t2 = threading.Thread(target=handler)
t2.start()

def end() :
    for j in range(0,100000):
        for visualizer_struct in arr2d[j] :
                time2 = str(time.time())
                vs2 = visualizer_struct
                vs2.previous_state = toState2
                vs2.current_state = toState3
                vs2.event_time = time2
                visualizer.receive_channel.put(vs2)
        if j < 100:
            time.sleep(0.1)
        time.sleep(0.4) 
time.sleep(6)
t3 = threading.Thread(target=end)
t3.start()


t.join()
t2.join()
t3.join()

