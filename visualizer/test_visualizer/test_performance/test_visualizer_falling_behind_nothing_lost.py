import time
import multiprocessing

from visualizer.visualizer import Visualizer
from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.GUI.gui import GUI

visualizer = Visualizer("end")
gui = GUI(visualizer, "end")

start_time = time.time()
time0 = int(start_time)


# set these params
number_of_events_pr_sec = 30000 # total number, must be equal or higher than number of states * number of event type
number_of_states = 5 # end state included
number_of_event_types = 20
number_of_runs = 3
actual_number_of_events_pr_second = ((number_of_events_pr_sec // number_of_event_types) // number_of_states ) * number_of_event_types * number_of_states

def test (channel,name) :
    endState = "end"

    state_names = [str(i) for i in range(0,number_of_states-1)] + [endState]
    
    def test_run(l):
        for s in range(number_of_states):
            for j in range(number_of_event_types): 
                for i in range(0,(number_of_events_pr_sec//number_of_states)//number_of_event_types) :
                    
                    if s == 0 :
                        from_state = ""
                        to_state = state_names[s]
                    else : 
                        from_state = state_names[s-1]
                        to_state = state_names[s]

                    time1 = str(time.time())

                    vs1 = VISUALIZER_STRUCT("rule" + str(j), name + "i" + str(i) + "j" + str(j)+ "l" + str(l),
                                             from_state, to_state, time0, time1, "", "OptionalInfo")
                    
                    channel.put(vs1)


    for l in range(number_of_runs):
        start_time_this_round = time.time()

        test_run(l)

        sleep_time = (start_time_this_round + 1) - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        print("events in visualizer queue: ", visualizer.receive_channel.qsize())



p = multiprocessing.Process(target=test, args=(visualizer.receive_channel,"1"))
p.start()
p.join()

while visualizer.receive_channel.empty() == False:
    time.sleep(0.1)

end_time = time.time()
print("All ", actual_number_of_events_pr_second * number_of_runs , "events are processed by the visualizer in ", end_time - start_time , " seconds")


