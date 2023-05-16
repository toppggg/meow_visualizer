import time
from visualizer_struct import VISUALIZER_STRUCT
import pandas as pd


class VisualizerState:
    name : str
    _last_update_time : int
    _queue : dict(VISUALIZER_STRUCT.event_id,VISUALIZER_STRUCT)
    
    _average_state_time:dict[VISUALIZER_STRUCT.event_type,float]
    
    # col_lst = ['event_type'] + [str(i) for i in range(0,60)] # Alternativ til at tilføje index i dataframe creation.
    __col_lst = [str(i) for i in range(0,60)]
    _seconds_array: pd.DataFrame(columns=__col_lst, index= 'event_type')
    _minutes_array: pd.DataFrame(columns=__col_lst)

    def __init__(name: str):
        pass

    def enqueue(visualizer_struct):
        pass
    def dequeue(visualizer_struct):
        pass
    def get_queue_data():
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