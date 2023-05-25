import pandas as pd
import datetime as dt

from visualizer.i_visualizer_query_data import IVisualizerQueryData
from visualizer.GUI.Idataframe_strategy.i_dataframe_strategy import IGUIDataframeStrategy   
from visualizer.vars import MINUTES_IN_HOUR, SECONDS_IN_MINUTE, SECONDS_IN_HOUR

class GetMinutesStrategy(IGUIDataframeStrategy):
        _visualizer : IVisualizerQueryData
        
        def __init__(self, visualizer : IVisualizerQueryData) :
             self._visualizer = visualizer

        def get_data(self, state, event_type : list[str] = []) -> pd.DataFrame  :
            df = self._visualizer.get_minutes_data(state, event_type)
            result = df.T 

            time_this_round = self._visualizer.get_time()
            xs = [""] * MINUTES_IN_HOUR
            for i in range (1, MINUTES_IN_HOUR):
                xs[i] = dt.datetime.fromtimestamp(time_this_round- (SECONDS_IN_HOUR - SECONDS_IN_MINUTE * (i+1))).strftime('%H:%M')

            result.insert(0, 'Time', xs)

            result.set_index('Time', inplace=True)
            return result