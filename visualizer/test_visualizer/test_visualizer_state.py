import unittest
from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.visualizer_state import VisualizerState
import time
import pandas as pd

from meow_base.recipes.jupyter_notebook_recipe import JupyterNotebookRecipe
from meow_base.tests.shared import BAREBONES_NOTEBOOK

class EventQueueDataTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()


    def TestInit(self):
        visualizer_state = VisualizerState("monitor")

        self.assertEqual(visualizer_state.name, "monitor")


    ### Test for enqueue ###
    def testEnqueueValidButNoDebugMessage(self) :
        time1 = str(time.time())
        eventId = "idnr1"
        vs = VISUALIZER_STRUCT("rule1",eventId, "", "Monitor", time1, time1, "", "OptionalInfo")
        visualizer_state = VisualizerState("testState")

        self.assertNotIn(vs,visualizer_state._queue.values())

        visualizer_state.enqueue(vs)

        self.assertIn(vs,visualizer_state._queue.values())

    def testEnqueueValidWithDebugMessage(self) :
        time1 = str(time.time())
        eventId = "idnr1"
        vs = VISUALIZER_STRUCT("rule1",eventId, "", "Monitor", time1, time1, "random message", "OptionalInfo")
        visualizer_state = VisualizerState("testState")

        self.assertNotIn(vs,visualizer_state._queue.values())

        visualizer_state.enqueue(vs)

        self.assertIn(vs,visualizer_state._queue.values())        

    def testEnqueueWrongType(self) :
        time1 = str(time.time())
        eventId = "idnr1"
        vs = ("random info", eventId, "", "Monitor", time1, time1, "random message", "OptionalInfo", "")
        visualizer_state = VisualizerState("testState")
        jnr = JupyterNotebookRecipe("recipe", BAREBONES_NOTEBOOK)
        self.assertNotIn(vs,visualizer_state._queue)       

        with self.assertRaises(TypeError):
                visualizer_state.enqueue(jnr)               

        self.assertNotIn(vs, visualizer_state._queue)       


    ## enqueue does not update average time
    def testEnqueueAverageTimeUnchanged (self) :
        time1 = time.time()
        eventId = "idnr1"
        test_event_type = "event1"
        visualizer_state = VisualizerState("testState")
        
        initial_averagetime = (0,2.0)
        visualizer_state._average_state_time[test_event_type] = initial_averagetime
        
        vs = VISUALIZER_STRUCT(test_event_type, eventId, "", "Monitor", str(time1 - 200), str(time1), "random message", "OptionalInfo")
        visualizer_state.enqueue(vs)
        
        self.assertIn(test_event_type,visualizer_state._average_state_time)
        self.assertEqual(visualizer_state._average_state_time[test_event_type], initial_averagetime) 


    ### Test that event_type is added to DataFrame _seconds_array###
    def testEnqueueAddEventTypeToSecondsDF(self) :
        time1 = str(time.time())
        event_id = "idnr1"
        test_event_type = "event1"
        visualizer_state = VisualizerState("testState")

        self.assertNotIn(event_id,visualizer_state._seconds_data.index)
        
        vs = VISUALIZER_STRUCT(test_event_type,event_id, "", "Monitor", time1, time1, "random message", "OptionalInfo")
        visualizer_state.enqueue(vs)
        
        self.assertIn(test_event_type,visualizer_state._seconds_data.index)   

    ### Test that event_type is added to DataFrame _minutes_array###
    def testEnqueueAddEventTypeToMinutesDF(self) :
        time1 = str(time.time())
        event_id = "idnr1"
        test_event_type = "event1"
        visualizer_state = VisualizerState("testState")

        self.assertNotIn(test_event_type,visualizer_state._minutes_data.index)
        
        vs = VISUALIZER_STRUCT(test_event_type,event_id, "", "Monitor", time1, time1, "random message", "OptionalInfo")
        visualizer_state.enqueue(vs)
        
        self.assertIn(test_event_type,visualizer_state._minutes_data.index)           
            
    def testEnqueueCreatesAverageTimeForEventType(self) :
        time1 = time.time()
        eventId = "idnr1"
        test_event_type = "event1"
        visualizer_state = VisualizerState("testState")

        self.assertNotIn(test_event_type,visualizer_state._average_state_time)
        
        vs = VISUALIZER_STRUCT(test_event_type,eventId, "", "Monitor", str(time1 - 200), str(time1), "random message", "OptionalInfo")
        visualizer_state.enqueue(vs)

        self.assertIn(test_event_type,visualizer_state._average_state_time)


    ### Test for dequeue ###
    def testDequeueNoDebugMessage(self) :
        time1 = str(time.time())
        eventId = "idnr1"
        dequeue_struct = VISUALIZER_STRUCT("rule1", eventId, "", "Monitor", time1, time1, "", "OptionalInfo")
        visualizer_state = VisualizerState("testState")

        visualizer_state._queue[eventId] = dequeue_struct
        visualizer_state._average_state_time[dequeue_struct.event_type] = (0,0.0)
        self.assertIn(dequeue_struct.event_type,visualizer_state._average_state_time) #arrange
        self.assertIn(dequeue_struct,visualizer_state._queue.values()) #arrange

        visualizer_state.dequeue(dequeue_struct) #act

        self.assertNotIn(dequeue_struct,visualizer_state._queue.values()) #assert

    def testDequeueWrongType(self) :
        time1 = str(time.time())
        eventId = 1
        vs = ("rule1", eventId, "", "Monitor", time1, time1, "", "OptionalInfo")
        visualizer_state = VisualizerState("testState")
        visualizer_state._queue[eventId] = vs

        self.assertIn(vs,visualizer_state._queue.values()) 

        with self.assertRaises(TypeError):
                visualizer_state.dequeue(eventId)

        self.assertIn(vs,visualizer_state._queue.values())
        
    def testDequeueAverageTimeUpdated(self) :
        time1 = time.time()-200
        time2 = time.time()
        
        event_id1 = "eventId1"
        vsIn = VISUALIZER_STRUCT("event1", event_id1, "", "Monitor", str(time1), str(time1), "", "OptionalInfo")
        vsOut = VISUALIZER_STRUCT("event1", event_id1, "", "Monitor", str(time1), str(time2), "", "OptionalInfo")

        visualizer_state = VisualizerState("testState")
        visualizer_state._queue[event_id1] = vsIn
        visualizer_state._average_state_time[vsIn.event_type] = (0,0.0)
        
        self.assertAlmostEqual(visualizer_state._average_state_time[vsOut.event_type][1], 0.0)
        self.assertEqual(visualizer_state._average_state_time[vsOut.event_type][0], 0)
        
        visualizer_state.dequeue(vsOut)

        self.assertAlmostEqual(visualizer_state._average_state_time[vsOut.event_type][1], time2-time1)
        self.assertEqual(visualizer_state._average_state_time[vsOut.event_type][0], 1)
        
    ### Test that dequeuing an eventtype that already contains 
    def testDequeueAverageTimeUpdated2ndRound(self) :
        time1 = time.time()-200
        time2 = time.time()
        
        event_id1 = "eventId1"
        vsIn = VISUALIZER_STRUCT("rule1", event_id1, "", "Monitor", str(time1), str(time1), "", "OptionalInfo")
        vsOut = VISUALIZER_STRUCT("rule1", event_id1, "", "Monitor", str(time1), str(time2), "", "OptionalInfo")
        
        visualizer_state = VisualizerState("testState")
        visualizer_state._average_state_time[vsIn.event_type] = (1,2.0)
        visualizer_state._queue[event_id1] = vsIn

        self.assertAlmostEqual(visualizer_state._average_state_time[vsOut.event_type][1], (2.0))
        self.assertEqual(visualizer_state._average_state_time[vsOut.event_type][0], 1)

        visualizer_state.dequeue(vsOut)

        self.assertAlmostEqual(visualizer_state._average_state_time[vsOut.event_type][1], (2.0 + time2-time1)/2)
        self.assertEqual(visualizer_state._average_state_time[vsOut.event_type][0], 2)
        
    ### return all visualizer structs from the queueu
    def testGetQueueData(self) :
        time1 = str(time.time())
        event_id1 = "eventId1"
        event_id2 = "eventId2"
        event_id3 = "eventId3"
        vs1 = ("rule1", event_id1, "", "Monitor", time1, time1, "", "OptionalInfo")
        vs2 = ("rule2", event_id2, "", "Monitor", time1, time1, "", "OptionalInfo")
        vs3 = ("rule3", event_id3, "", "Monitor", time1, time1, "", "OptionalInfo")
        
        visualizer_state = VisualizerState("testState")
        visualizer_state._queue[event_id1] = vs1
        visualizer_state._queue[event_id2] = vs2
        visualizer_state._queue[event_id3] = vs3

        returnval = visualizer_state.get_queue_data()

    ### Test for Seconds Array

    def testSecondsArrayUpdated (self):
        pass

    def testSecondsToMinutesConversion(self) :
        pass
        


