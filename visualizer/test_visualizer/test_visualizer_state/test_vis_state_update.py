import unittest
from unittest.mock import patch
import time

from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.visualizer_state import VisualizerState
from visualizer.vars import SECONDS_IN_MINUTE, MINUTES_IN_HOUR


class EventQueueDataTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

    @patch('time.time', return_value=55)
    def testUpdateResetsSecondsToZero(self, patched_time_time):
        visualizer_state = VisualizerState("testState")
        start_time = 50
        event_time = 55

        visualizer_state._last_update_time = start_time
        vs = VISUALIZER_STRUCT("rule1","idnr1", "", "Monitor", start_time, event_time, "random message", "OptionalInfo")
        visualizer_state._seconds_data.loc[vs.event_type] = [5] * SECONDS_IN_MINUTE
        visualizer_state._minutes_data.loc[vs.event_type] = [5] * MINUTES_IN_HOUR
        
        for i in range(0,60):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type,i], 5)

        visualizer_state._update()

        for i in range((start_time+1) % SECONDS_IN_MINUTE, (event_time % SECONDS_IN_MINUTE)):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type, i], 0)

        for i in range((event_time+1) % SECONDS_IN_MINUTE, SECONDS_IN_MINUTE):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type,i], 5)
        for i in range(0, (start_time + 1) % SECONDS_IN_MINUTE):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type,i], 5)
    
    
    @patch('time.time', return_value=65)
    def testUpdateResetsSecondsToZero2(self, patched_time_time):
        visualizer_state = VisualizerState("testState")
        start_time = 55
        event_time = 65

        visualizer_state._last_update_time = start_time
        vs = VISUALIZER_STRUCT("rule1","idnr1", "", "Monitor", start_time, event_time, "random message", "OptionalInfo")
        visualizer_state._seconds_data.loc[vs.event_type] = [5] * SECONDS_IN_MINUTE
        visualizer_state._minutes_data.loc[vs.event_type] = [5] * MINUTES_IN_HOUR
        
        for i in range(0,60):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type,i], 5)

        visualizer_state._update()

        for i in range((start_time+1 % SECONDS_IN_MINUTE), SECONDS_IN_MINUTE):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type, i], 0)

        for i in range(0, (event_time+1)%SECONDS_IN_MINUTE):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type, i], 0)    

        for i in range((event_time+1) % SECONDS_IN_MINUTE, (start_time + 1) % SECONDS_IN_MINUTE):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type,i], 5)

    def testUpdateResetsSecondsToZero3(self):
        visualizer_state = VisualizerState("testState")
        start_time = int(time.time()- SECONDS_IN_MINUTE)
        visualizer_state._last_update_time = start_time
        vs = VISUALIZER_STRUCT("rule1","idnr1", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
        visualizer_state._seconds_data.loc[vs.event_type] = [5] * SECONDS_IN_MINUTE
        visualizer_state._minutes_data.loc[vs.event_type] = [0] * MINUTES_IN_HOUR
        
        for i in range(0,SECONDS_IN_MINUTE):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type,i], 5)

        visualizer_state._update()

        end_time = int(time.time())
        # assert end_time - start_time == SECONDS_IN_MINUTE

        for i in range(0,SECONDS_IN_MINUTE):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type][i % SECONDS_IN_MINUTE], 0)
        
        self.assertCountEqual(visualizer_state._minutes_data.loc[vs.event_type], \
                              [5 * (start_time % SECONDS_IN_MINUTE + 1)] * 1 + [0] * (MINUTES_IN_HOUR - 1))
        # If int(time.time()) % 60() is equal to 10 seconds, then there seconds 0-10 would be 5, and 11-59 would be 0, therefore it should mod seconds_in_minute + 1.

