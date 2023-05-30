import pandas as pd
import datetime as dt

from visualizer.i_visualizer_query_data import IVisualizerQueryData
from visualizer.GUI.Idataframe_strategy.i_dataframe_strategy import IGUIDataframeStrategy   
from visualizer.vars import HOURS_IN_DAY, SECONDS_IN_HOUR, SECONDS_IN_DAY

class GetHoursStrategy(IGUIDataframeStrategy):
        _visualizer : IVisualizerQueryData
        
        def __init__(self, visualizer : IVisualizerQueryData) :
             self._visualizer = visualizer

        def get_data(self, state, event_type : list[str] = []) -> pd.DataFrame  :
            df = self._visualizer.get_hours_data(state, event_type)
            result = df.T 

            time_this_round = self._visualizer.get_time()
            xs = [""] * HOURS_IN_DAY
            for i in range (0, HOURS_IN_DAY):
                xs[i] = dt.datetime.fromtimestamp(time_this_round - (SECONDS_IN_DAY - SECONDS_IN_HOUR * i)).strftime('%D:%H')

            # result.insert(0, 'Time', xs)
            result['Time'] = xs

            result.set_index('Time', inplace=True)

            result  = self.setAverage(result, state, event_type)

            return result