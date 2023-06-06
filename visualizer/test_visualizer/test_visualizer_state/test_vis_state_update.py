import unittest
from unittest.mock import patch
import time

from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.visualizer_state import VisualizerState
from visualizer.vars import SECONDS_IN_MINUTE, MINUTES_IN_HOUR, SECONDS_IN_HOUR, HOURS_IN_DAY


class EventQueueDataTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

    @patch('time.time', return_value=55)
    def testUpdateResetsSecondsToZero(self, mock_time):
        visualizer_state = VisualizerState("testState")
        start_time = 50
        event_time = mock_time.return_value

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
    def testUpdateResetsSecondsToZero2(self, mock_time):
        visualizer_state = VisualizerState("testState")
        start_time = 55
        event_time = mock_time.return_value

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

    @patch('time.time', return_value=60)
    def testConvertToMinutesResetToZero(self, mock_time) :
        visualizer_state = VisualizerState("testState")
        start_time = 1
        event_time = mock_time.return_value

        visualizer_state._last_update_time = start_time
        vs = VISUALIZER_STRUCT("rule1","idnr1", "", "Monitor", start_time, event_time, "random message", "OptionalInfo")
        visualizer_state._seconds_data.loc[vs.event_type] = [5] * SECONDS_IN_MINUTE
        visualizer_state._minutes_data.loc[vs.event_type] = [5] * MINUTES_IN_HOUR
        
        for i in range(0,60):
            self.assertEqual(visualizer_state._minutes_data.loc[vs.event_type, i], 5)
        
        visualizer_state._update()

        self.assertEqual(visualizer_state._minutes_data.loc[vs.event_type, ((start_time)//SECONDS_IN_MINUTE) % MINUTES_IN_HOUR], 10)
        self.assertEqual(visualizer_state._minutes_data.loc[vs.event_type, ((event_time)//SECONDS_IN_MINUTE) % MINUTES_IN_HOUR], 0)

        for i in range(((event_time) //SECONDS_IN_MINUTE % MINUTES_IN_HOUR) + 1, MINUTES_IN_HOUR):
            self.assertEqual(visualizer_state._minutes_data.loc[vs.event_type, i], 5)

    @patch('time.time', return_value = 63 * SECONDS_IN_MINUTE)
    def testConvertToMinutesResetToZero2(self, mock_time) :
        visualizer_state = VisualizerState("testState")
        start_time = 55 * SECONDS_IN_MINUTE + SECONDS_IN_MINUTE - 1 # 55:59 = last second in the seconds_data,
        event_time = mock_time.return_value

        visualizer_state._last_update_time = start_time
        vs = VISUALIZER_STRUCT("rule1","idnr1", "", "Monitor", start_time, event_time, "random message", "OptionalInfo")
        visualizer_state._seconds_data.loc[vs.event_type] = [2] * SECONDS_IN_MINUTE # all data is valid, since last update time was 55.59
        visualizer_state._minutes_data.loc[vs.event_type] = [5] * MINUTES_IN_HOUR
        
        for i in range(0,60):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type, i], 2)
            self.assertEqual(visualizer_state._minutes_data.loc[vs.event_type, i], 5)
        visualizer_state._update()

        # Since all 60 fields in the seonds array, the minutes array [start_time] should be 120
        self.assertEqual(visualizer_state._minutes_data.loc[vs.event_type, (start_time // SECONDS_IN_MINUTE) % MINUTES_IN_HOUR], SECONDS_IN_MINUTE * 2) 
        
        for i in range(((start_time // SECONDS_IN_MINUTE) % MINUTES_IN_HOUR) + 1, MINUTES_IN_HOUR):
            #remaining part of the minutes array should be reset to 0
            self.assertEqual(visualizer_state._minutes_data.loc[vs.event_type, i], 0)

        for i in range(0, ((event_time // SECONDS_IN_MINUTE) % MINUTES_IN_HOUR) + 1):
            # the first part of the array, until the event_time, should be 0
            self.assertEqual(visualizer_state._minutes_data.loc[vs.event_type, i], 0)

        for i in range(((event_time // SECONDS_IN_MINUTE ) % MINUTES_IN_HOUR) + 1, ((start_time // SECONDS_IN_MINUTE) % MINUTES_IN_HOUR)):
            # the time between event_time and start_time should be 5, since less than an hour has occured, so the data is valid
            self.assertEqual(visualizer_state._minutes_data.loc[vs.event_type, i], 5)

    @patch('time.time', return_value = 27 * SECONDS_IN_HOUR)
    def testConvertToHours(self, mock_time) :
        visualizer_state = VisualizerState("testState")
        start_time = 20 * SECONDS_IN_HOUR + SECONDS_IN_HOUR - 1 # 55:59 = last second in the seconds_data,
        event_time = mock_time.return_value

        visualizer_state._last_update_time = start_time
        vs = VISUALIZER_STRUCT("rule1","idnr1", "", "Monitor", start_time, event_time, "random message", "OptionalInfo")
        visualizer_state._seconds_data.loc[vs.event_type] = [0] * SECONDS_IN_MINUTE # all data is valid, since last update time was 55.59
        visualizer_state._seconds_data.loc[vs.event_type,59] = 2 # last second is 5, so 5 will be inserted in the minutes array field 55
        visualizer_state._minutes_data.loc[vs.event_type] = [2] * MINUTES_IN_HOUR
        visualizer_state._hours_data.loc[vs.event_type] = [5] * HOURS_IN_DAY
        
        #arrange
        for i in range(0,59):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type, i], 0)
        self.assertEqual(visualizer_state._minutes_data.loc[vs.event_type, 59], 2)
        for i in range(0,60):
            self.assertEqual(visualizer_state._minutes_data.loc[vs.event_type, i], 2)
        for i in range(0,24):
            self.assertEqual(visualizer_state._hours_data.loc[vs.event_type, i], 5)

        #act
        visualizer_state._update()

        
        #assert
        # Since all 60 fields in the seonds array, the minutes array [start_time] should be 120
        self.assertEqual(visualizer_state._hours_data.loc[vs.event_type, (start_time // SECONDS_IN_HOUR) % HOURS_IN_DAY], MINUTES_IN_HOUR * 2) 
        
        for i in range(((start_time // SECONDS_IN_HOUR) % HOURS_IN_DAY) + 1, HOURS_IN_DAY):
            #remaining part of the minutes array should be reset to 0
            self.assertEqual(visualizer_state._hours_data.loc[vs.event_type, i], 0)

        for i in range(0, ((event_time // SECONDS_IN_HOUR) % HOURS_IN_DAY) + 1):
            # the first part of the array, until the event_time, should be 0
            self.assertEqual(visualizer_state._hours_data.loc[vs.event_type, i], 0)

        for i in range(((event_time // SECONDS_IN_HOUR ) % HOURS_IN_DAY) + 1, ((start_time // SECONDS_IN_HOUR) % HOURS_IN_DAY)):
            # the time between event_time and start_time should be 5, since less than an hour has occured, so the data is valid
            self.assertEqual(visualizer_state._hours_data.loc[vs.event_type, i], 5)