import unittest
from unittest.mock import patch
import time

from meow_base.recipes.jupyter_notebook_recipe import JupyterNotebookRecipe
from meow_base.tests.shared import BAREBONES_NOTEBOOK

from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.visualizer_state import VisualizerState
from visualizer.vars import SECONDS_IN_MINUTE, MINUTES_IN_HOUR, HOURS_IN_DAY,\
    SECONDS_IN_HOUR, SECONDS_IN_DAY 


class EventQueueDataTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

    @patch('time.sleep', return_value=[int(time.time()- 5),int(time.time())])
    def testUpdateResetsSecondsToZero(self, patched_time_sleep):
        visualizer_state = VisualizerState("testState")
        start_time = patched_time_sleep.return_value[0]
        visualizer_state._last_update_time = start_time
        vs = VISUALIZER_STRUCT("rule1","idnr1", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
        visualizer_state._seconds_data.loc[vs.event_type] = [5] * SECONDS_IN_MINUTE
        visualizer_state._minutes_data.loc[vs.event_type] = [5] * MINUTES_IN_HOUR
        
        for i in range(0,60):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type][i], 5)

        visualizer_state._update()

        for i in range(start_time + 1, start_time + 5):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type][i % SECONDS_IN_MINUTE], 0)

        if (start_time + 5) % SECONDS_IN_MINUTE < (start_time + 1) % SECONDS_IN_MINUTE:
            for i in range((start_time + 6) % SECONDS_IN_MINUTE, (start_time + 1) % SECONDS_IN_MINUTE):
                self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type][i], 5)
        else:
            for i in range((start_time + 6) % SECONDS_IN_MINUTE, SECONDS_IN_MINUTE):
                self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type][i], 5)
            for i in range(0, (start_time + 1) % SECONDS_IN_MINUTE):
                self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type][i], 5)

    # @patch('time.sleep', return_value=[1540166400 - 30, 1540166400 + 30])
    def testUpdateResetsSecondsToZero(self):
        visualizer_state = VisualizerState("testState")
        # start_time = patched_time_sleep.return_value[0]
        start_time = int(time.time())
        visualizer_state._last_update_time = start_time
        vs = VISUALIZER_STRUCT("rule1","idnr1", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
        visualizer_state._seconds_data.loc[vs.event_type] = [5] * SECONDS_IN_MINUTE
        visualizer_state._minutes_data.loc[vs.event_type] = [0] * MINUTES_IN_HOUR
        
        for i in range(0,SECONDS_IN_MINUTE):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type][i], 5)

        time.sleep(SECONDS_IN_MINUTE)
        visualizer_state._update()

        for i in range(0,SECONDS_IN_MINUTE):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type][i % SECONDS_IN_MINUTE], 0)
        
        self.assertCountEqual(visualizer_state._minutes_data.loc[vs.event_type], [5 * MINUTES_IN_HOUR] * 1 + [0] * (MINUTES_IN_HOUR - 1))

