import unittest
import time

from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.visualizer_state import VisualizerState


class EventQueueDataTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()


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

    # def testEnqueueWrongType(self) :
    #     time1 = str(time.time())
    #     eventId = "idnr1"
    #     vs = ("random info", eventId, "", "Monitor", time1, time1, "random message", "OptionalInfo", "")
    #     visualizer_state = VisualizerState("testState")
    #     jnr = JupyterNotebookRecipe("recipe", BAREBONES_NOTEBOOK)
    #     self.assertNotIn(vs,visualizer_state._queue)       

    #     with self.assertRaises(TypeError):
    #             visualizer_state.enqueue(jnr)               

    #     self.assertNotIn(vs, visualizer_state._queue)       


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
        self.assertAlmostEqual(visualizer_state._average_state_time[test_event_type], initial_averagetime) 


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

    ### Test that event_type is added to DataFrame _hours_array###
    def testEnqueueAddEventTypeToHoursDF(self) :
        time1 = str(time.time())
        event_id = "idnr1"
        test_event_type = "event1"
        visualizer_state = VisualizerState("testState")

        self.assertNotIn(test_event_type,visualizer_state._hours_data.index)
        
        vs = VISUALIZER_STRUCT(test_event_type,event_id, "", "Monitor", time1, time1, "random message", "OptionalInfo")
        visualizer_state.enqueue(vs)
        
        self.assertIn(test_event_type,visualizer_state._hours_data.index)        
            
    ### Test that a new event_type beging registered, creates a new entry in _average_state_time###
    def testEnqueueCreatesAverageTimeForEventType(self) :
        time1 = time.time()
        eventId = "idnr1"
        test_event_type = "event1"
        visualizer_state = VisualizerState("testState")

        self.assertNotIn(test_event_type,visualizer_state._average_state_time)
        
        vs = VISUALIZER_STRUCT(test_event_type,eventId, "", "Monitor", str(time1 - 200), str(time1), "random message", "OptionalInfo")
        visualizer_state.enqueue(vs)

        self.assertIn(test_event_type,visualizer_state._average_state_time)


    def testCreateAverageTimeForEventTypeSetsTupleToZero(self) :
        time1 = time.time()
        eventId = "idnr1"
        test_event_type = "event1"
        visualizer_state = VisualizerState("testState")

        self.assertNotIn(test_event_type,visualizer_state._average_state_time)
        
        vs = VISUALIZER_STRUCT(test_event_type,eventId, "", "Monitor", str(time1 - 200), str(time1), "random message", "OptionalInfo")
        visualizer_state.enqueue(vs)

        self.assertIn(test_event_type,visualizer_state._average_state_time)
        self.assertAlmostEqual(visualizer_state._average_state_time[test_event_type][0], 0)
        self.assertAlmostEqual(visualizer_state._average_state_time[test_event_type][1], 0.0)
