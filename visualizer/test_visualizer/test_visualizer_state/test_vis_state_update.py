import unittest
from unittest.mock import patch

from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.visualizer_state import VisualizerState
import time
import pandas as pd

from meow_base.recipes.jupyter_notebook_recipe import JupyterNotebookRecipe
from meow_base.tests.shared import BAREBONES_NOTEBOOK

class EventQueueDataTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

    @patch('time.sleep', return_value=None)
    def TestUpdateResetsSecondsToZero(self, patched_time_sleep):
        visualizer_state = VisualizerState("testState")
        start_time = int(time.time())
        visualizer_state._last_update_time = start_time
        vs = VISUALIZER_STRUCT("rule1","idnr1", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
        visualizer_state._seconds_data.loc[vs.event_type] = [5] * 60
        
        for i in range(0,60):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type][i], 5)
        
        time.sleep(5)
        visualizer_state._update()

        time_after_update = visualizer_state._last_update_time

        for i in range(start_time + 1,time_after_update):
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type][i % 60], 0)
            self.assertEqual(visualizer_state._seconds_data.loc[vs.event_type][0 % 60], 1)
        