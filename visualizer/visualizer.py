from visualizer.visualizer_state import VisualizerState
from visualizer.debug_data import DebugData
from visualizer.i_visualizer_receive_data import IVisualizerReceiveData
from visualizer.i_visualizer_query_data import IVisualizerQueryData
from visualizer_struct import VISUALIZER_STRUCT
import pandas as pd

class Visualizer(IVisualizerReceiveData, IVisualizerQueryData) :
    _visualizer_states : dict[VisualizerState.name, VisualizerState]
    _debug_data : DebugData

    def __init__() ->None:
        pass

    def _add_event(self, visualizer_struct: VISUALIZER_STRUCT) -> None :
        pass
    def _update(self) -> None :
        pass
    def get_seconds_data(event_types: list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass
    def get_minutes_data(event_types: list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass
    def get_hours_data(event_types: list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass
    def get_days_data(event_types: list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass
    def get_months_data(event_types: list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass
    def get_years_data(event_types: list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass
    def get_debug_messages() -> list[VISUALIZER_STRUCT] :
        pass
    def get_event_average_time_in_state(event_types :list[VISUALIZER_STRUCT.event_type] = None, state_name : str = "") -> pd.DataFrame :
        pass
    def get_event_average_live_time(event_types :list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass
    def get_all_data()-> pd.DataFrame :
        pass
    def get_event_id(event_id : VISUALIZER_STRUCT.event_id) -> VISUALIZER_STRUCT :
        pass