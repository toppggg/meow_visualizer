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

time0 = int(time.time())

toState1 = "Monitor"
toState3 = "end"

visualizer._visualizer_states[toState1] = VisualizerState(toState1)

# from spam import Spam
# gui = Spam(visualizer)
gui = GUI(visualizer, toState3)

def monitor () : 
    for j in range(1000):
        for i in range(0,1000) :
            time1 = str(time.time())
            vs1 = VISUALIZER_STRUCT("rule", "i" + str(i) + "j" + str(j), "", toState1, time0, time1, "", "OptionalInfo")
            visualizer.receive_channel.put(vs1)
        time.sleep(1)

        for i in range(0,1000) :
            time2 = str(time.time())
            vs1 = VISUALIZER_STRUCT("rule", "i" + str(i) + "j" + str(j), toState1, toState3, time0, time2, "", "OptionalInfo")
            visualizer.receive_channel.put(vs1)


t = threading.Thread(target = monitor)
t.start()
print("test  PID: ", threading.get_native_id())
print("test thread  PID: ", t.native_id)
t.join

