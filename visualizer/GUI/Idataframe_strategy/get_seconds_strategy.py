import pandas as pd
import datetime as dt

from visualizer.i_visualizer_query_data import IVisualizerQueryData
from visualizer.GUI.Idataframe_strategy.i_dataframe_strategy import IGUIDataframeStrategy   

class GetSecondsStrategy(IGUIDataframeStrategy):
        _visualizer : IVisualizerQueryData
        
        def __init__(self, visualizer : IVisualizerQueryData) :
             self._visualizer = visualizer

        def get_data(self, state) -> pd.DataFrame  :
            df = self._visualizer.get_seconds_data(state)
            result = df.T 

            time_this_round = self._visualizer.get_time()
            xs = [""]*60
            for i in range (0,60):
                xs[i] = dt.datetime.fromtimestamp(time_this_round- (60 - i)).strftime('%H:%M:%S')

            result.insert(0, 'Time', xs)

            result.set_index('Time', inplace=True)
            return result