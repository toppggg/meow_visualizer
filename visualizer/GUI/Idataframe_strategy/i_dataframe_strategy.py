import pandas as pd

from visualizer.i_visualizer_query_data import IVisualizerQueryData


class IGUIDataframeStrategy :
    _visualizer : IVisualizerQueryData

    def get_data(self, state : str, event_type : list[str] = []) -> pd.DataFrame :
        """ Return strategy defined dataframe from the state, containing events grouped by event_type """

    """Appends total finished count and average time to column titels"""
    def setAverage (self, df : pd.DataFrame, state, event_type : list[str]  = []) -> pd.DataFrame: 
        if event_type :
            average = self._visualizer.get_event_average_time_in_state(state_name = state, event_types = event_type)
        else : 
            average = self._visualizer.get_event_average_time_in_state(state_name = state, event_types = [])

        for key in average.keys() :
            total, time = average[key]
            str1 = str(key) + " ( " +  str(total) + " ; " + str(round(time, 3)) + "s )"
            df.rename(columns={key : str1}, inplace=True)

        return df