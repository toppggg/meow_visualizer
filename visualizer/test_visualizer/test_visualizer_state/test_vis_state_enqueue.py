from unittest.mock import patch
import unittest
import time

from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.visualizer_state import VisualizerState
from visualizer.vars import SECONDS_IN_MINUTE, MINUTES_IN_HOUR, HOURS_IN_DAY, SECONDS_IN_HOUR, SECONDS_IN_DAY


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


    ## enqueue does not update average time
    def testEnqueueAverageTimeUnchanged (self) :
        time1 = time.time()
        eventId = "idnr1"
        test_event_type = "event1"
        visualizer_state = VisualizerState("testState")
        
        initial_averagetime = (0,2.0)
        visualizer_state._average_state_time[test_event_type] = initial_averagetime
        
        vs = VISUALIZER_STRUCT(test_event_type, eventId, "", "Monitor",
                                str(time1 - 200), str(time1), "random message", "OptionalInfo")
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
        
        vs = VISUALIZER_STRUCT(test_event_type,event_id, "", "Monitor",
                                time1, time1, "random message", "OptionalInfo")
        visualizer_state.enqueue(vs)
        
        self.assertIn(test_event_type,visualizer_state._seconds_data.index)   

    ### Test that event_type is added to DataFrame _minutes_array###
    def testEnqueueAddEventTypeToMinutesDF(self) :
        time1 = str(time.time())
        event_id = "idnr1"
        test_event_type = "event1"
        visualizer_state = VisualizerState("testState")

        self.assertNotIn(test_event_type,visualizer_state._minutes_data.index)
        
        vs = VISUALIZER_STRUCT(test_event_type,event_id, "", "Monitor",
                                time1, time1, "random message", "OptionalInfo")
        visualizer_state.enqueue(vs)
        
        self.assertIn(test_event_type,visualizer_state._minutes_data.index)     

    ### Test that event_type is added to DataFrame _hours_array###
    def testEnqueueAddEventTypeToHoursDF(self) :
        time1 = str(time.time())
        event_id = "idnr1"
        test_event_type = "event1"
        visualizer_state = VisualizerState("testState")

        self.assertNotIn(test_event_type,visualizer_state._hours_data.index)
        
        vs = VISUALIZER_STRUCT(test_event_type,event_id, "", "Monitor",
                                time1, time1, "random message", "OptionalInfo")
        visualizer_state.enqueue(vs)
        
        self.assertIn(test_event_type,visualizer_state._hours_data.index)        
            
    ### Test that a new event_type beging registered, creates a new entry in _average_state_time###
    def testEnqueueCreatesAverageTimeForEventType(self) :
        time1 = time.time()
        eventId = "idnr1"
        test_event_type = "event1"
        visualizer_state = VisualizerState("testState")

        self.assertNotIn(test_event_type,visualizer_state._average_state_time)
        
        vs = VISUALIZER_STRUCT(test_event_type,eventId, "", "Monitor", \
                               str(time1 - 200), str(time1), "random message", "OptionalInfo")
        visualizer_state.enqueue(vs)

        self.assertIn(test_event_type,visualizer_state._average_state_time)


    def testCreateAverageTimeForEventTypeSetsTupleToZero(self) :
        time1 = time.time()
        eventId = "idnr1"
        test_event_type = "event1"
        visualizer_state = VisualizerState("testState")

        self.assertNotIn(test_event_type,visualizer_state._average_state_time)
        
        vs = VISUALIZER_STRUCT(test_event_type,eventId, "", "Monitor", \
                               str(time1 - 200), str(time1), "random message", "OptionalInfo")
        visualizer_state.enqueue(vs)

        self.assertIn(test_event_type,visualizer_state._average_state_time)
        self.assertAlmostEqual(visualizer_state._average_state_time[test_event_type][0], 0)
        self.assertAlmostEqual(visualizer_state._average_state_time[test_event_type][1], 0.0)


    # @patch('time.sleep', return_value=[int(time.time()- 5),int(time.time())])
    @patch('time.time', return_value=int(1000000))
    def testBackDatedEventIsAddedToCorrectMinutesDF(self, mock_time):
        visualizer_state = VisualizerState("testState")
        start_time = mock_time.return_value
        visualizer_state._last_update_time = start_time
        vs = VISUALIZER_STRUCT("rule1","idnr1", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
        visualizer_state._seconds_data.loc[vs.event_type] = [0] * 60
        visualizer_state._minutes_data.loc[vs.event_type] = [0] * 60
        visualizer_state._hours_data.loc[vs.event_type] = [0] * 24
        mock_time.return_value = start_time + 70
        visualizer_state.enqueue(vs)
        
        self.assertAlmostEqual(visualizer_state._seconds_data.loc[vs.event_type].sum(),0)
        self.assertAlmostEqual(visualizer_state._minutes_data.loc[vs.event_type]\
                               [(start_time // SECONDS_IN_MINUTE) % MINUTES_IN_HOUR], 1)
        # self.assertAlmostEqual(visualizer_state._hours_data.loc[vs.event_type][(start_time // SECONDS_IN_HOUR) % HOURS_IN_DAY], 0)

    @patch('time.time', return_value=int(1000000))
    def testBackDatedEventIsAddedToCorrectHoursDF(self, mock_time):
        visualizer_state = VisualizerState("testState")
        start_time = mock_time.return_value
        visualizer_state._last_update_time = start_time
        vs = VISUALIZER_STRUCT("rule1","idnr1", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
        visualizer_state._seconds_data.loc[vs.event_type] = [0] * 60
        visualizer_state._minutes_data.loc[vs.event_type] = [0] * 60
        visualizer_state._hours_data.loc[vs.event_type] = [0] * 24

        mock_time.return_value = start_time + SECONDS_IN_DAY + 70 
        visualizer_state.enqueue(vs)
        
        self.assertAlmostEqual(visualizer_state._seconds_data.loc[vs.event_type].sum(),0)
        self.assertAlmostEqual(visualizer_state._minutes_data.loc[vs.event_type].sum(), 0)
        self.assertAlmostEqual(visualizer_state._hours_data.loc[vs.event_type][(start_time // SECONDS_IN_HOUR) % HOURS_IN_DAY], 1)