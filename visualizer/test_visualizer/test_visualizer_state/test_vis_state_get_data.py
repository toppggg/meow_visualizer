from unittest.mock import patch
import unittest
import time
import pandas as pd
import random

from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.visualizer_state import VisualizerState
from visualizer.vars import SECONDS_IN_MINUTE, MINUTES_IN_HOUR, HOURS_IN_DAY,\
    SECONDS_IN_HOUR, SECONDS_IN_DAY 


class EventQueueDataTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()


    ###Test that new visualizer state is created with correct name
    def TestInit(self):
        visualizer_state = VisualizerState("monitor")

        self.assertAlmostEqual(visualizer_state.name, "monitor")


    ### return all visualizer structs from the queueu
    def testGetQueueData(self) :
        time1 = str(time.time())
        event_id1 = "eventId1"
        event_id2 = "eventId2"
        event_id3 = "eventId3"
        vs1 = ("event1", event_id1, "", "Monitor", time1, time1, "", "OptionalInfo")
        vs2 = ("event2", event_id2, "", "Monitor", time1, time1, "", "OptionalInfo")
        vs3 = ("event3", event_id3, "", "Monitor", time1, time1, "", "OptionalInfo")
        
        visualizer_state = VisualizerState("testState")
        visualizer_state._queue[event_id1] = vs1
        visualizer_state._queue[event_id2] = vs2
        visualizer_state._queue[event_id3] = vs3

        returnval = visualizer_state.get_queue_data()

        self.assertIn(event_id1, returnval)
        self.assertIn(event_id2, returnval)
        self.assertIn(event_id3, returnval)

    ### Test for Seconds Array

    @patch.object(time, 'time')
    # def test_method1(self, mock_time):
    def testGetSecondsArray (self, mock_time):
        mock_time = mock_time = time.time()
        visualizer_state = VisualizerState("testState")
        start_time = int(time.time())
        visualizer_state._last_update_time = start_time
        vs1 = VISUALIZER_STRUCT("rule1","idnr1", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
        vs2 = VISUALIZER_STRUCT("rule2","idnr2", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
        vs3 = VISUALIZER_STRUCT("rule3","idnr3", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
        vs1_array = [random.randint(1,10)] * SECONDS_IN_MINUTE
        vs2_array = [random.randint(1,10)] * SECONDS_IN_MINUTE
        vs3_array = [random.randint(1,10)] * SECONDS_IN_MINUTE

        """fill seconds data"""
        visualizer_state._seconds_data.loc[vs1.event_type] = vs1_array
        visualizer_state._seconds_data.loc[vs2.event_type] = vs2_array
        visualizer_state._seconds_data.loc[vs3.event_type] = vs3_array

        """fill minutes data"""
        visualizer_state._minutes_data.loc[vs1.event_type] = [5] * MINUTES_IN_HOUR
        visualizer_state._minutes_data.loc[vs2.event_type] = [5] * MINUTES_IN_HOUR
        visualizer_state._minutes_data.loc[vs3.event_type] = [5] * MINUTES_IN_HOUR
        
        returnval : pd.DataFrame = visualizer_state.get_seconds_data()

        
        self.assertCountEqual(vs1_array, returnval.loc[vs1.event_type])
        self.assertCountEqual(vs2_array, returnval.loc[vs2.event_type])
        self.assertCountEqual(vs3_array, returnval.loc[vs3.event_type])


    @patch.object(time, 'time')
    def testGetSecondsArrayOneEventType (self, mock_time):
        mock_time = time.time()
        visualizer_state = VisualizerState("testState")
        start_time = int(time.time())
        visualizer_state._last_update_time = start_time
        event1 = "rule1"
        event2 = "rule2"
        event3 = "rule3"
        vs1 = VISUALIZER_STRUCT(event1,"idnr1", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
        vs2 = VISUALIZER_STRUCT(event2,"idnr2", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
        vs3 = VISUALIZER_STRUCT(event3,"idnr3", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
        vs1_array = [random.randint(1,10)] * SECONDS_IN_MINUTE
        vs2_array = [random.randint(1,10)] * SECONDS_IN_MINUTE
        vs3_array = [random.randint(1,10)] * SECONDS_IN_MINUTE

        """fill seconds data"""
        visualizer_state._seconds_data.loc[vs1.event_type] = vs1_array
        visualizer_state._seconds_data.loc[vs2.event_type] = vs2_array
        visualizer_state._seconds_data.loc[vs3.event_type] = vs3_array

        """fill minutes data"""
        visualizer_state._minutes_data.loc[vs1.event_type] = [5] * MINUTES_IN_HOUR
        visualizer_state._minutes_data.loc[vs2.event_type] = [5] * MINUTES_IN_HOUR
        visualizer_state._minutes_data.loc[vs3.event_type] = [5] * MINUTES_IN_HOUR
        
        returnval : pd.DataFrame = visualizer_state.get_seconds_data([event1])

        self.assertIn(event1, returnval.index)
        self.assertCountEqual(vs1_array, returnval.loc[vs1.event_type])
        self.assertNotIn(event2, returnval.index)
        self.assertNotIn(event3, returnval.index)

    @patch.object(time, 'time')
    def testGetSecondsArrayMultipleEventTypes (self, mock_time):
        mock_time = time.time()
        visualizer_state = VisualizerState("testState")
        start_time = int(time.time())
        visualizer_state._last_update_time = start_time
        event1 = "rule1"
        event2 = "rule2"
        event3 = "rule3"
        vs1 = VISUALIZER_STRUCT(event1,"idnr1", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
        vs2 = VISUALIZER_STRUCT(event2,"idnr2", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
        vs3 = VISUALIZER_STRUCT(event3,"idnr3", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
        vs1_array = [random.randint(1,10)] * SECONDS_IN_MINUTE
        vs2_array = [random.randint(1,10)] * SECONDS_IN_MINUTE
        vs3_array = [random.randint(1,10)] * SECONDS_IN_MINUTE

        """fill seconds data"""
        visualizer_state._seconds_data.loc[vs1.event_type] = vs1_array
        visualizer_state._seconds_data.loc[vs2.event_type] = vs2_array
        visualizer_state._seconds_data.loc[vs3.event_type] = vs3_array

        """fill minutes data"""
        visualizer_state._minutes_data.loc[vs1.event_type] = [5] * MINUTES_IN_HOUR
        visualizer_state._minutes_data.loc[vs2.event_type] = [5] * MINUTES_IN_HOUR
        visualizer_state._minutes_data.loc[vs3.event_type] = [5] * MINUTES_IN_HOUR
        
        returnval : pd.DataFrame = visualizer_state.get_seconds_data([event1, event2])

        self.assertIn(event1, returnval.index)
        self.assertCountEqual(vs1_array, returnval.loc[vs1.event_type])
        self.assertIn(event2, returnval.index)
        self.assertCountEqual(vs2_array, returnval.loc[vs2.event_type])
        self.assertNotIn(event3, returnval.index)

    ### test if getting a dataframe ordered by timestamp returns the correct dataframe.
    def testAuxReturnDFOrderedByTimeStamp(self):
        # # Test DataFrame as created in VisualizerState
        data = {'event_type': ['event1', 'event2', 'event3'] }
        for i in range(60):
            data[str(i)] = [i, i+1, i+2]
        df = pd.DataFrame(data).set_index('event_type')

        # # Expected DataFrame
        expected_data = {'event_type': ['event1', 'event2', 'event3'] }
        for i in range(31, 60) : expected_data[str(i)] = [i, i+1, i+2] 
        for i in range(31) : expected_data[str(i)] = [i, i+1, i+2] 
        
        expected_df = pd.DataFrame(expected_data).set_index('event_type')

        timestamp = 30
        visualizer_state = VisualizerState("testState")
        result = visualizer_state._aux_return_df_order_by_timestamp(dataframe = df, timestamp = timestamp)

        pd.testing.assert_frame_equal(expected_df, result)


    def testGetTime(self):
        visualizer_state = VisualizerState("testState")
        time1 = time.time()
        visualizer_state._last_update_time = time1

        #assert
        self.assertAlmostEqual(visualizer_state.get_time(), time1)

    def testGetEventsByTypeSingleEvent(self):
        event1 = "event1"
        visualizer_state = VisualizerState("testState")
        visualizer_state._events_pr_type_in_state[event1] = 1
        visualizer_struct = VISUALIZER_STRUCT(event1, "idnr1", "", "Monitor", str(time.time()), str(time.time()), "random message", "OptionalInfo")

        #arrange
        visualizer_state._queue[event1] = visualizer_struct

        #act
        result = visualizer_state.get_event_id(event1)

        #assert
        self.assertEqual(result, visualizer_struct)

        


