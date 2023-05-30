import pandas as pd
from multiprocessing import Queue
import math
import time
import threading

from meow_base.functionality.validation import check_type

from visualizer.visualizer_state import VisualizerState
from visualizer.debug_data import DebugData
from visualizer.i_visualizer_receive_data import IVisualizerReceiveData
from visualizer.i_visualizer_query_data import IVisualizerQueryData
from visualizer.visualizer_struct import VISUALIZER_STRUCT


class Visualizer(IVisualizerReceiveData, IVisualizerQueryData) :
    _visualizer_states : dict[str, VisualizerState]
    _debug_data : DebugData
    _end_state : VisualizerState
    __shutdown : bool = False
    __receiver : threading.Thread
    visualizer_update_time : int #time since epoch

    def __init__(self, endState  : str) ->None:
        self.receive_channel = Queue()
        self._debug_data = DebugData()
        self._end_state = VisualizerState(endState)
        self._visualizer_states = {}
        self._visualizer_states[endState] = self._end_state
        self.visualizer_update_time = int(time.time())

        self.__receiver = threading.Thread(target=self.__receiver_worker)
        self.__receiver.start()

    def __receiver_worker(self) : 
        while not self.__shutdown or not self.receive_channel.empty():
            self._update()
            time.sleep(0.5)
    
    ### Add event to visualizer_state, if the state does not exist, add the event to debug_struct ###
    def _add_event(self, visualizer_struct: VISUALIZER_STRUCT) -> None :
        if (visualizer_struct.current_state not in self._visualizer_states) :
            self._visualizer_states[visualizer_struct.current_state] = VisualizerState(visualizer_struct.current_state)

        visualizer_ToState = self._visualizer_states[visualizer_struct.current_state]
        visualizer_ToState.enqueue(visualizer_struct)

        if (visualizer_struct.previous_state != "") : #Check if previous state is not set.
            try: # Check if previous state exists
                visualizer_FromState = self._visualizer_states[visualizer_struct.previous_state]   
            except:
                visualizer_struct.debug_message = "Previous state does not exist"
                self._debug_data.add_debug_struct(visualizer_struct)
            try: # Try to remove event from previous state
                visualizer_FromState.dequeue(visualizer_struct)
            except:
                visualizer_struct.debug_message = "Event does not exist in previous state"
                self._debug_data.add_debug_struct(visualizer_struct)

        
    
    ### Read from pipe, check that input is actually VISUALIZER_STRUCT, and pass events to _add_event ###
    def _update(self) -> None :
            while not self.receive_channel.empty():
                visualizer_struct = self._get_from_pipe() # Get valid event from pipe, or None
                if visualizer_struct is not None:
                    self._add_event(visualizer_struct)
                

    def get_seconds_data(self, state_name : str, event_types: list[VISUALIZER_STRUCT.event_type] = []) -> pd.DataFrame :
        try:
            visualizer_state = self._visualizer_states[state_name]
            result = visualizer_state.get_seconds_data(event_types)
            self.visualizer_update_time = visualizer_state.get_time()
            return result
        except:
            return None
        

    def get_minutes_data(self, state_name : str, event_types: list[VISUALIZER_STRUCT.event_type] = []) -> pd.DataFrame :
        try:
            visualizer_state = self._visualizer_states[state_name]
            result = visualizer_state.get_minutes_data(event_types)
            self.visualizer_update_time = visualizer_state.get_time()
            return result
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


    def get_event_average_time_in_state(self, state_name : str, event_types :list[VISUALIZER_STRUCT.event_type] = []) \
            -> dict[VISUALIZER_STRUCT.event_type, (int,float)] :
        try:
            visualizer_state = self._visualizer_states[state_name]
            return visualizer_state.get_average_time(event_types)
        except:
            return {}
    
    def get_events_in_state(self,state_name : str) -> dict[VISUALIZER_STRUCT.event_type,int] :
        visualizer_state = self._visualizer_states[state_name]
        return visualizer_state.get_events_in_state_by_rule()



    def get_event_average_live_time(self, event_types :list[VISUALIZER_STRUCT.event_type] = []) \
            ->  dict[VISUALIZER_STRUCT.event_type, (int,float)]:
        result : dict[VISUALIZER_STRUCT.event_type, (int,float)] = self._end_state.get_average_time(event_types)
        for event_type in result :
            result[event_type] = (math.inf, result[event_type][1])

        for state in self._visualizer_states.values():
            if state.name != self._end_state.name :
                state_average_time = state.get_average_time(event_types)
                for eventType in result.keys() :        
                    lowest_count = min(result[eventType][0], state_average_time[event_type][0])
                    average_time = result[eventType][1] + state_average_time[event_type][1]
                    result[eventType] = (lowest_count, average_time)
        return result
        
    def get_all_states(self)-> list[str] :
        return list(self._visualizer_states.keys())
        
    def get_event_id(self, event_id : VISUALIZER_STRUCT.event_id) -> VISUALIZER_STRUCT :
        for state in self._visualizer_states.values():
            result = state.get_event_id(event_id)
            if result:
                return result

    def get_all_data(self,) -> dict[str,list[VISUALIZER_STRUCT]] :
        result={}
        for state in self._visualizer_states.values():
            result[state.name] = state._queue
        return result


    ### Auxiliary methods ###
    
    def _get_from_pipe(self) -> VISUALIZER_STRUCT :
        pipe_data = self.receive_channel.get()

        visualizer_struct: VISUALIZER_STRUCT
        try:
            visualizer_struct = pipe_data
            check_type(visualizer_struct,VISUALIZER_STRUCT) # Use of meow's type checker
            return visualizer_struct
        except:
            debug_struct = VISUALIZER_STRUCT(event_time = time.time())
            debug_struct.debug_message = "Input is not of type VISUALIZER_STRUCT, input found in optional_info"
            debug_struct.optional_info = str(pipe_data)
            self._debug_data.add_debug_struct(debug_struct)   
            return None 
        
    def get_time(self) -> int :
        return self.visualizer_update_time
        
    def shutdown(self) -> None :
        self.__shutdown = True
        self.__receiver.join()
        pass
        