import time
import threading
import multiprocessing

from visualizer.visualizer import Visualizer
from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.visualizer_state import VisualizerState
from visualizer.GUI.gui import GUI

visualizer = Visualizer("end")

time0 = int(time.time())

toState1 = "Monitor"
toState3 = "end"

visualizer._visualizer_states[toState1] = VisualizerState(toState1)

gui = GUI(visualizer, toState3)

def test (channel) :

    print(time.time())
    for j in range(500):
        start_time_this_round = time.time()
        number_to_test = 2000
        number_of_states = 2
        for i in range(0,number_to_test//number_of_states) :
            time1 = str(time.time())
            vs1 = VISUALIZER_STRUCT("rule", "i" + str(i) + "j" + str(j), "", toState1, time0, time1, "", "OptionalInfo")
            channel.put(vs1)

        for i in range(0,number_to_test//number_of_states) :
            time2 = str(time.time())
            vs1 = VISUALIZER_STRUCT("rule", "i" + str(i) + "j" + str(j), toState1, toState3, time0, time2, "", "OptionalInfo")
            channel.put(vs1)
        sleep_time = (start_time_this_round + 1) - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            print("Over one second!")
    print(time.time())



p = multiprocessing.Process(target=test, args=(visualizer.receive_channel,))
p.start()
time.sleep(1)


print("visualizer's reciver Thread: ", visualizer._receiver.native_id)
print("GUi plot thread : ", gui._plot_thread.native_id)
print("Main  PID: ", threading.get_native_id())
print("Test thread  PID: ", p.pid)
p.join()

