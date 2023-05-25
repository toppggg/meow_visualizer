import unittest
import time

from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.visualizer import Visualizer
from visualizer.visualizer_state import VisualizerState


class TestVisualizer(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

    
    def testInit(self) : 
        visualizer = Visualizer("end")
        self.assertIsNotNone(visualizer._debug_data)
        self.assertIsNotNone(visualizer._end_state)
        self.assertIsNotNone(visualizer._visualizer_states)

        self.assertIn("end", visualizer._visualizer_states)
        visualizer.shutdown()

    def testAddEvent(self) :
        visualizer = Visualizer("end")
        time1 = int(time.time())
        eventId1 = "Event1"
        toState = "Monitor"
        vs1 = VISUALIZER_STRUCT("rule1",eventId1, "", toState, time1, time1, "", "OptionalInfo")
        
        self.assertNotIn(eventId1, visualizer._visualizer_states)

        visualizer._add_event(vs1)

        self.assertIn(toState, visualizer._visualizer_states)
        self.assertIn(eventId1, visualizer._visualizer_states[toState]._queue)
        visualizer.shutdown()

    def testAddTwoEvents(self) :
        visualizer = Visualizer("end")
        time1 = int(time.time())
        eventId1 = "Event1"
        eventId2 = "Event2"
        toState = "Monitor"
        vs1 = VISUALIZER_STRUCT("rule1",eventId1, "", toState, time1, time1, "", "OptionalInfo")
        vs2 = VISUALIZER_STRUCT("rule1",eventId2, "", toState, time1, time1, "", "OptionalInfo")
        
        self.assertNotIn(eventId1, visualizer._visualizer_states)
        self.assertNotIn(eventId2, visualizer._visualizer_states)

        visualizer._add_event(vs1)
        visualizer._add_event(vs2)

        self.assertIn(toState, visualizer._visualizer_states)
        self.assertIn(eventId1, visualizer._visualizer_states[toState]._queue)
        self.assertIn(eventId2, visualizer._visualizer_states[toState]._queue)
        visualizer.shutdown()

    def testEventsTakenFromQueue(self) :
        visualizer = Visualizer("end")
        time1 = int(time.time())
        eventId1 = "Event1"
        eventId2 = "Event2"
        toState = "Monitor"
        vs1 = VISUALIZER_STRUCT("rule1",eventId1, "", toState, time1, time1, "", "OptionalInfo")
        vs2 = VISUALIZER_STRUCT("rule1",eventId2, "", toState, time1, time1, "", "OptionalInfo")

        visualizer._visualizer_states[toState] = VisualizerState(toState)

        self.assertNotIn(eventId1, visualizer._visualizer_states[toState]._queue)
        self.assertNotIn(eventId2, visualizer._visualizer_states[toState]._queue)

        visualizer.receive_channel.put(vs1)
        visualizer.receive_channel.put(vs2)
        time.sleep(1) # Make sure the threaded put has time to execute before _update checks the queue
        
        self.assertTrue(visualizer.receive_channel.empty())
        self.assertIn(eventId1, visualizer._visualizer_states[toState]._queue)
        self.assertIn(eventId2, visualizer._visualizer_states[toState]._queue)
        visualizer.shutdown()


    def testVisualizerRun10SecondsOnlyEnqueue(self) :
        visualizer = Visualizer("end")
        time1 = int(time.time())

        toState = "Monitor"

        visualizer._visualizer_states[toState] = VisualizerState(toState)
        for i in range(0,10):
            eventId1 = "event" + str(i)
            eventId2 = "event" + str(i) + str(i)
            vs1 = VISUALIZER_STRUCT("rule1",eventId1, "", toState, time1, time1, "", "OptionalInfo")
            vs2 = VISUALIZER_STRUCT("rule1",eventId2, "", toState, time1, time1, "", "OptionalInfo")


            self.assertNotIn(eventId1, visualizer._visualizer_states[toState]._queue)
            self.assertNotIn(eventId2, visualizer._visualizer_states[toState]._queue)

            visualizer.receive_channel.put(vs1)
            visualizer.receive_channel.put(vs2)
            time.sleep(1) # Make sure the threaded put has time to execute before _update checks the queue
        
        self.assertTrue(visualizer.receive_channel.empty())
        for i in range(0,10):
            eventId1 = "event" + str(i)
            eventId2 = "event" + str(i) + str(i)
            self.assertIn(eventId1, visualizer._visualizer_states[toState]._queue)
            self.assertIn(eventId2, visualizer._visualizer_states[toState]._queue)
        visualizer.shutdown()

    def testVisualizerRun10SecondsEnqueuePlusDequeue(self) :
        visualizer = Visualizer("end")
        time1 = int(time.time())

        toState1 = "Monitor"
        toState2 = "Handler"

        visualizer._visualizer_states[toState1] = VisualizerState(toState1)
        visualizer._visualizer_states[toState2] = VisualizerState(toState2)
        for i in range(0,10):
            eventId1 = "event" + str(i)
            eventId2 = "event" + str(i) + str(i)
            vs1 = VISUALIZER_STRUCT("rule1",eventId1, "", toState1, time1, time1, "", "OptionalInfo")
            vs2 = VISUALIZER_STRUCT("rule1",eventId2, "", toState1, time1, time1, "", "OptionalInfo")
            vs3 = VISUALIZER_STRUCT("rule1",eventId2, toState1, toState2, time1, time1, "", "OptionalInfo")


            self.assertNotIn(eventId1, visualizer._visualizer_states[toState1]._queue)
            self.assertNotIn(eventId2, visualizer._visualizer_states[toState1]._queue)
            self.assertNotIn(eventId2, visualizer._visualizer_states[toState2]._queue)

            visualizer.receive_channel.put(vs1)
            visualizer.receive_channel.put(vs2)
            visualizer.receive_channel.put(vs3)
            time.sleep(1) # Make sure the threaded put has time to execute before _update checks the queue
        
        self.assertTrue(visualizer.receive_channel.empty())
        for i in range(0,10):
            eventId1 = "event" + str(i)
            eventId2 = "event" + str(i) + str(i)
            self.assertIn(eventId1, visualizer._visualizer_states[toState1]._queue)
            self.assertNotIn(eventId2, visualizer._visualizer_states[toState1]._queue)
            self.assertIn(eventId2, visualizer._visualizer_states[toState2]._queue)
        visualizer.shutdown()        
