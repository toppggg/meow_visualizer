import pandas as pd
from multiprocessing import Queue
import math

from visualizer.visualizer_state import VisualizerState
from visualizer.debug_data import DebugData
from visualizer.i_visualizer_receive_data import IVisualizerReceiveData
from visualizer.i_visualizer_query_data import IVisualizerQueryData
from visualizer.visualizer_struct import VISUALIZER_STRUCT


class Visualizer(IVisualizerReceiveData, IVisualizerQueryData) :
    _visualizer_states : dict[str, VisualizerState]
    _debug_data : DebugData
    _end_state : VisualizerState

    def __init__(self, endState  : str) ->None:
        self.receive_channel = Queue()
        self._debug_data = DebugData()
        self._end_state = VisualizerState(endState)
        self._visualizer_states = {}
        self._visualizer_states[endState] = self._end_state
        
        


    ### Add event to visualizer_state, if the state does not exist, add the event to debug_struct ###
    def _add_event(self, visualizer_struct: VISUALIZER_STRUCT) -> None :
        if (visualizer_struct.current_state not in self._visualizer_states.keys()) :
            self._visualizer_states[visualizer_struct.current_state] = VisualizerState(visualizer_struct.current_state)

        visualizer_ToState = self._visualizer_states[visualizer_struct.current_state]
        visualizer_ToState.enqueue(visualizer_struct)

        if (visualizer_struct.previous_state != "") : 
            visualizer_FromState = self._visualizer_states[visualizer_struct.previous_state]   
            visualizer_FromState.dequeue(visualizer_struct)

        
    
    ### Read from pipe, check that input is actually VISUALIZER_STRUCT, and pass events to _add_event ###
    def _update(self) -> None :
        
        pass

    def get_seconds_data(self, state_name : str, event_types: list[VISUALIZER_STRUCT.event_type] = []) -> pd.DataFrame :
        try:
            visualizer_state = self._visualizer_states[state_name]
            return visualizer_state.get_seconds_data(event_types)
        except:
            return None
        
    def get_minutes_data(self, state_name : str, event_types: list[VISUALIZER_STRUCT.event_type] = []) -> pd.DataFrame :
        try:
            visualizer_state = self._visualizer_states[state_name]
            return visualizer_state.get_minutes_data(event_types)
        except:
            return None
    def get_hours_data(self, state_name : str, event_types: list[VISUALIZER_STRUCT.event_type] = []) -> pd.DataFrame :
        # Hours array not implemented, but is identical to minutes array
        pass
    def get_days_data(self, state_name : str, event_types: list[VISUALIZER_STRUCT.event_type] = []) -> pd.DataFrame :
        # days array not implemented, but is identical to minutes array
        pass
    def get_months_data(self, state_name : str, event_types: list[VISUALIZER_STRUCT.event_type] = []) -> pd.DataFrame :
        # months array not implemented, but is identical to minutes array
        pass
    def get_years_data(self, state_name : str, event_types: list[VISUALIZER_STRUCT.event_type] = []) -> pd.DataFrame :
         # years array not implemented, but is identical to minutes array
        pass
    def get_debug_messages(self) -> list[VISUALIZER_STRUCT] :
        return self._debug_data.get_debug_messages()

    def get_event_average_time_in_state(self, state_name : str, event_types :list[VISUALIZER_STRUCT.event_type] = None) \
            -> dict[VISUALIZER_STRUCT.event_type, (int,float)] :
        try:
            visualizer_state = self._visualizer_states[state_name]
            return visualizer_state.get_average_time(event_types)
        except:
            return None

    def get_event_average_live_time(self, event_types :list[VISUALIZER_STRUCT.event_type] = []) \
            ->  dict[VISUALIZER_STRUCT.event_type, (int,float)]:
        result : dict[VISUALIZER_STRUCT.event_type, (int,float)] = self._end_state.get_average_time()
        for event_type in result.keys :
            result[event_type] = (math.inf, result[event_type][1])

        for state in self._visualizer_states:
            if state.name != self._end_state.name :
                state_average_time = state.get_average_time()
                for eventType in self._end_state._queue.keys :        
                    lowest_count = (min(result[eventType][0]), state_average_time[event_type][0]) 
                    average_time = result[eventType][1] + state_average_time[event_type][1]
                    result[eventType] = (lowest_count, average_time)
            
            
            
            
        
        pass
    def get_all_data(self)-> pd.DataFrame :
        pass
    def get_event_id(self, event_id : VISUALIZER_STRUCT.event_id) -> VISUALIZER_STRUCT :
        pass