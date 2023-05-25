import pandas as pd

from visualizer.i_visualizer_query_data import IVisualizerQueryData


class IGUIDataframeStrategy :
    _visualizer : IVisualizerQueryData

    def get_data(self, state : str) -> pd.DataFrame :
        """ Return strategy defined dataframe from the state, containing events grouped by event_type """