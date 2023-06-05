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

def monitor () : 
    for j in range(1000):
        monitorevents:list[VISUALIZER_STRUCT] = []
        for i in range(0,50) :
            time1 = str(time.time())
            id = random.randint(0,40)
            if random.randint(0,40) < 30  :
                vs1 = VISUALIZER_STRUCT("rule" + str(i), "i" + str(i) + "j" + str(j), "", toState1, time0, time1, "", "OptionalInfo")
                visualizer.receive_channel.put(vs1)
                monitorevents = monitorevents + [vs1]
        
        time.sleep(0.2)

    return 1

t = threading.Thread(target=monitor)
t.start()

def handler() :
    for j in range(1000):
        time.sleep(0.1)    
        for i in range(0,50) :
            if random.randint(0,30) < 20 :
                time2 = str(time.time())
                vs2 = VISUALIZER_STRUCT("rule" + str(i), "i" + str(i) + "j" + str(j), toState1, toState2, time0, time2, "", "OptionalInfo")
                visualizer.receive_channel.put(vs2)
        if j < 100:
            time.sleep(0.1)
        time.sleep(0.1) 

# time.sleep(5)
t2 = threading.Thread(target=handler)
t2.start()

def end() :
    # time.sleep(8)
    for j in range(1000):
        time.sleep(0.2)    
        if random.randint(0,3) < 2 :
            for i in range(0,40) :
                time2 = str(time.time())
                vs2 = VISUALIZER_STRUCT("rule" + str(i), "i" + str(i) + "j" + str(j), toState2, toState3, time0, time2, "", "OptionalInfo")
                visualizer.receive_channel.put(vs2)
            if j < 100:
                time.sleep(0.3)

time.sleep(3)
t3 = threading.Thread(target=end)
t3.start()


t.join()
t2.join()
t3.join()

