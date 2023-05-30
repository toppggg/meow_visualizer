import pandas as pd
import datetime as dt

from visualizer.i_visualizer_query_data import IVisualizerQueryData
from visualizer.GUI.Idataframe_strategy.i_dataframe_strategy import IGUIDataframeStrategy   
from visualizer.vars import SECONDS_IN_MINUTE

class GetSecondsStrategy(IGUIDataframeStrategy):
        _visualizer : IVisualizerQueryData

        def __init__(self, visualizer: IVisualizerQueryData) -> None:
            self._visualizer = visualizer

        def get_data(self, state, event_type : list[str]  = []) -> pd.DataFrame  :
            df = self._visualizer.get_seconds_data(state, event_type)
            result = df.T

            time_this_round = self._visualizer.get_time()
            xs = [""] * SECONDS_IN_MINUTE
            for i in range (0, SECONDS_IN_MINUTE):
                xs[i] = dt.datetime.fromtimestamp(time_this_round- (SECONDS_IN_MINUTE - i)).strftime('%H:%M:%S')

            result['Time'] = xs
            result.set_index('Time', inplace=True)
            
            # result  = self.setAverage(result, state, event_type)

            return result

