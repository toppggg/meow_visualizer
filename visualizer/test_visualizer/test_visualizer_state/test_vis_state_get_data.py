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

        self.assertEqual(visualizer_state.name, "monitor")


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

    def testGetSecondsArray (self):
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


    def testGetSecondsArrayOneEventType (self):
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

    def testGetSecondsArrayMultipleEventTypes (self):
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





        


