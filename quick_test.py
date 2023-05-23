import unittest
from unittest.mock import patch
import random
import time
import pandas as pd

from visualizer.visualizer import Visualizer
from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.visualizer_state import VisualizerState
from visualizer.vars import SECONDS_IN_MINUTE, MINUTES_IN_HOUR, HOURS_IN_DAY,\
    SECONDS_IN_HOUR, SECONDS_IN_DAY 

from meow_base.recipes.jupyter_notebook_recipe import JupyterNotebookRecipe

visualizer_state = VisualizerState("testState")
start_time = int(time.time() - 55)
visualizer_state._last_update_time = start_time
vs1 = VISUALIZER_STRUCT("rule1","idnr1", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
vs2 = VISUALIZER_STRUCT("rule2","idnr3", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
vs3 = VISUALIZER_STRUCT("rule3","idnr4", "", "Monitor", start_time, start_time, "random message", "OptionalInfo")
visualizer_state._seconds_data.loc[vs1.event_type] = [random.randint(1,10)] * SECONDS_IN_MINUTE
visualizer_state._seconds_data.loc[vs2.event_type] = [random.randint(1,10)] * SECONDS_IN_MINUTE
visualizer_state._seconds_data.loc[vs3.event_type] = [random.randint(1,10)] * SECONDS_IN_MINUTE

visualizer_state._minutes_data.loc[vs1.event_type] = [0] * SECONDS_IN_MINUTE
visualizer_state._minutes_data.loc[vs2.event_type] = [0] * SECONDS_IN_MINUTE
visualizer_state._minutes_data.loc[vs3.event_type] = [0] * SECONDS_IN_MINUTE


print(visualizer_state._seconds_data)
print(visualizer_state.get_seconds_data(["rule1","rule2"]))
# print(visualizer_state._aux_return_df_order_by_timestamp(5, visualizer_state._seconds_data))
for i in range(0,5):
    time.sleep(1)
    print(visualizer_state.get_seconds_data(["rule1","rule2"]))
# visualizer_state._update()
# print(visualizer_state._seconds_data.loc[vs.event_type])


# visualizer = Visualizer()
# tovisualizer = ToVisualizer(visualizer.receive_channel)

