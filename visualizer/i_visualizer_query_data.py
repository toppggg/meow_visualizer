import pandas as pd

from visualizer.visualizer_struct import VISUALIZER_STRUCT

class IVisualizerQueryData :

    def get_seconds_data(state_name : str, event_types: list[VISUALIZER_STRUCT.event_type] = []) -> pd.DataFrame :
        """ Return dataframe with events triggered pr second for the last 60 seconds, grouped by event_type """
    def get_minutes_data(state_name : str, event_types: list[VISUALIZER_STRUCT.event_type] = []) -> pd.DataFrame :
        """ Return dataframe with events triggered pr second for the last 60 minues, grouped by event_type """
    def get_hours_data(state_name : str, event_types: list[VISUALIZER_STRUCT.event_type] = []) -> pd.DataFrame :
        """ Return dataframe with events triggered pr second for the last 24 hours, grouped by event_type """
    def get_days_data(state_name : str, event_types: list[VISUALIZER_STRUCT.event_type] = []) -> pd.DataFrame :
        """ Return dataframe with events triggered pr second for the last 28-31 days, grouped by event_type """
    def get_months_data(state_name : str, event_types: list[VISUALIZER_STRUCT.event_type] = []) -> pd.DataFrame :
        """ Return dataframe with events triggered pr second for the last 60 seconds, grouped by event_type """
    def get_years_data(state_name : str, event_types: list[VISUALIZER_STRUCT.event_type] = []) -> pd.DataFrame :
        """ Return dataframe with events triggered pr second for the last 60 seconds, grouped by event_type """
    def get_debug_messages() -> list[VISUALIZER_STRUCT] :
        """ Return a list of visualizer structs that contain debug_messages """
    def get_event_average_time_in_state(event_types :list[VISUALIZER_STRUCT.event_type] = None, state_name : str = "") -> pd.DataFrame :
        """ Return an average time of an event_type in a given Visualizer_State"""
    def get_event_average_live_time(event_types :list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        """ Return an average live time of an event_type """
    def get_all_data()-> pd.DataFrame :
        """ Return all visualizer_structs contained in all visualizer_states in Visualizser"""
    def get_event_id(event_id : VISUALIZER_STRUCT.event_id) -> VISUALIZER_STRUCT :
        """ Return event from event_id """