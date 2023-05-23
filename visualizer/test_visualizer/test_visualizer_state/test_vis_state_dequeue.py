import unittest
from unittest.mock import patch
import time

from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.visualizer_state import VisualizerState


class EventQueueDataTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()



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
        