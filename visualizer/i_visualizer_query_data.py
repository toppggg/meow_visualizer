import pandas as pd

from visualizer.visualizer_struct import VISUALIZER_STRUCT


class IVisualizerQueryData :

    visualizer_update_time : int 

    def get_seconds_data(state_name : str, event_types: list[VISUALIZER_STRUCT.event_type] = []) -> pd.DataFrame :
        """ Return dataframe from the state, containing  events triggered pr second for the last 60 seconds, grouped by event_type """
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
    def get_event_average_time_in_state(state_name : str = "", event_types :list[VISUALIZER_STRUCT.event_type] = []) \
        -> dict[VISUALIZER_STRUCT.event_type,(int,float)]  :
        """ Return an average time of an event_type in a given Visualizer_State"""
    def get_event_average_live_time(event_types :list[VISUALIZER_STRUCT.event_type]) -> dict[VISUALIZER_STRUCT.event_type,(int,float)] :
        """ Return an average live time of an event_type """
    def get_all_data()-> dict[str,list[VISUALIZER_STRUCT]] :
        """ Return all visualizer_structs contained in all visualizer_states in Visualizser"""
    def get_event_id(event_id : VISUALIZER_STRUCT.event_id) -> VISUALIZER_STRUCT :
        """ Return event from event_id """
    def get_time() :
        """ Return the updatetime """
    def get_all_states() -> list[str] :
        """ Return all states in visualizer """
    def count_events_by_rule_in_state(state_name : str) -> dict[VISUALIZER_STRUCT.event_type,int] :
        """ Return number of events in a state """
    def get_events_in_state (state_name : str) -> list[VISUALIZER_STRUCT] :
        """ Return all events in a state """