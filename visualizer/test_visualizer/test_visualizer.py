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

        self.assertIn("end", visualizer._visualizer_states.keys())

    def testAddEvent(self) :
        visualizer = Visualizer("end")
        time1 = int(time.time())
        eventId1 = "Event1"
        eventId2 = "Event2"
        toState = "Monitor"

        vs1 = VISUALIZER_STRUCT("rule1",eventId1, "", toState, time1, time1, "", "OptionalInfo")
        vs2 = VISUALIZER_STRUCT("rule1",eventId2, "", toState, time1, time1, "", "OptionalInfo")
        
        self.assertNotIn(eventId1, visualizer._visualizer_states.keys())

        visualizer._add_event(vs1)

        self.assertIn(toState, visualizer._visualizer_states.keys())
        self.assertIn(eventId1, visualizer._visualizer_states[toState]._queue.keys())

    def testAddTwoEvents(self) :
        visualizer = Visualizer("end")
        time1 = int(time.time())
        eventId1 = "Event1"
        eventId2 = "Event2"
        toState = "Monitor"

        vs1 = VISUALIZER_STRUCT("rule1",eventId1, "", toState, time1, time1, "", "OptionalInfo")
        vs2 = VISUALIZER_STRUCT("rule1",eventId2, "", toState, time1, time1, "", "OptionalInfo")
        
        self.assertNotIn(eventId1, visualizer._visualizer_states.keys())
        self.assertNotIn(eventId2, visualizer._visualizer_states.keys())

        visualizer._add_event(vs1)
        visualizer._add_event(vs2)

        self.assertIn(toState, visualizer._visualizer_states.keys())
        self.assertIn(eventId1, visualizer._visualizer_states[toState]._queue.keys())
        self.assertIn(eventId2, visualizer._visualizer_states[toState]._queue.keys())

