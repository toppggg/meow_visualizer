import time
from visualizer.visualizer_struct import VISUALIZER_STRUCT
import pandas as pd


class VisualizerState:
    name : str
    _last_update_time : int
    _queue : dict[VISUALIZER_STRUCT.event_id, VISUALIZER_STRUCT]
    
    _average_state_time:dict[VISUALIZER_STRUCT.event_type,(int,float)] # value is number of events and average time
    
    # col_lst = ['event_type'] + [str(i) for i in range(0,60)] # Alternativ til at tilføje index i dataframe creation.
    __col_lst = [str(i) for i in range(0,60)]
    _seconds_array: pd.DataFrame
    _minutes_array: pd.DataFrame

    def __init__(self, name: str):
        self._seconds_array = pd.DataFrame(columns=[i for i in range(0,60)])
        self._minutes_array = pd.DataFrame(columns=[i for i in range(0,60)])
        self._queue = {}
        self._average_state_time = {}
        pass

    def enqueue(self, visualizer_struct):
        pass
    def dequeue(self, visualizer_struct):
        pass
    def get_queue_data(self):
        pass

    def get_minutes_data(event_types : list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass

    def get_seconds_data(event_types: list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass

    def get_hours_data(event_types:list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass
    def get_days_data(event_types:list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass
    def get_months_data(event_types:list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass

    def get_years_data(event_types:list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame : 
        pass
    def _convert_to_minutes():
        pass
    def _convert_to_hour():
        pass
    def _convert_to_day():
        pass
    def _convert_to_month():
        pass
    def _convert_to_year():
        pass