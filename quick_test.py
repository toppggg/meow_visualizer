import unittest
from unittest.mock import patch

from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.visualizer_state import VisualizerState
import time
import pandas as pd

from meow_base.recipes.jupyter_notebook_recipe import JupyterNotebookRecipe

visualizer_state = VisualizerState("testState")
start_time = int(time.time())
visualizer_state._last_update_time = start_time
vs = VISUALIZER_STRUCT("rule1","idnr1", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
visualizer_state._seconds_data.loc[vs.event_type] = [5] * 60
visualizer_state._minutes_data.loc[vs.event_type] = [5] * 60


time.sleep(10)
visualizer_state._update()
print(visualizer_state._seconds_data.loc[vs.event_type])