import time
from visualizer.visualizer_struct import VISUALIZER_STRUCT
import pandas as pd


class VisualizerState:
    name : str
    _last_update_time : int
    _queue : dict[VISUALIZER_STRUCT.event_id, VISUALIZER_STRUCT]
    _average_state_time:dict[VISUALIZER_STRUCT.event_type,(int,float)] # value is number of events and average time
    _seconds_data: pd.DataFrame
    _minutes_data: pd.DataFrame

    def __init__(self, name: str):
        self._seconds_data = pd.DataFrame(columns=[i for i in range(0,60)])
        self._minutes_data = pd.DataFrame(columns=[i for i in range(0,60)])
        self._hours_data = pd.DataFrame(columns=[i for i in range(0,24)])
        self._queue = {}
        self._average_state_time = {}
        self.name = name
        self._last_update_time = int(time.time()) 
        

    def _update(self) -> None :
        update_time = int(time.time())
        if update_time - self._last_update_time > 0 :
            self._update_seconds_array(update_time)
        
        self._last_update_time = update_time

    def _update_seconds_array(self, update_time) -> None :
        MAGIC_NUMBER = 60
        if (update_time // MAGIC_NUMBER) - (self._last_update_time // MAGIC_NUMBER) > 0 : # 6067//60 - 6046//60 = 101 - 100 = 1
            #nulstil resten af arrayet
            for i in range ((self._last_update_time % MAGIC_NUMBER) + 1, MAGIC_NUMBER): 
                self._seconds_data[i] = 0   #set the subsequent seconds to 0, since nothing was received
            self._update_minutes_array(update_time)
            if (update_time // MAGIC_NUMBER - self._last_update_time // MAGIC_NUMBER > 1 ) or (update_time % MAGIC_NUMBER >= self._last_update_time % 60) : 
                for i in range (0, (self._last_update_time % MAGIC_NUMBER) + 1) : # more than a min has passed, reset everything
                    self._seconds_data[i] = 0
            else :
                for i in range(0, (update_time % MAGIC_NUMBER) + 1) :
                    self._seconds_data[i] = 0
        else:
            #nulstil indtil update_time
            for i in range(self._last_update_time+1, (update_time % MAGIC_NUMBER) + 1) :
                    self._seconds_data[i] = 0

    def _update_minutes_array(self, update_time) -> None :
        update_time = update_time //60
        last_update_time = self._last_update_time//60
        ARRAY_SIZE = 60
        
        ### this may not work, there are not test for this yet.
        for index, row in self._seconds_data.iterrows():
            self._minutes_data.loc[index][last_update_time%60] = row.sum
        
        
        if (update_time // ARRAY_SIZE) - (last_update_time // ARRAY_SIZE) > 0 : # 6067//60 - 6046//60 = 101 - 100 = 1
            #nulstil resten af arrayet
            for i in range ((last_update_time % ARRAY_SIZE) + 1, ARRAY_SIZE): 
                self._minutes_data[i] = 0   #set the subsequent seconds to 0, since nothing was received
            self._update_hours_array(update_time)
            if (update_time // ARRAY_SIZE - last_update_time // ARRAY_SIZE > 1 ) or (update_time % ARRAY_SIZE >= last_update_time % 60) : 
                for i in range (0, (last_update_time % ARRAY_SIZE) + 1) : # more than a min has passed, reset everything
                    self._minutes_data[i] = 0
            else :
                for i in range(0, (update_time % ARRAY_SIZE) + 1) :
                    self._minutes_data[i] = 0
        else:
            #nulstil indtil update_time
            for i in range(last_update_time+1, (update_time % ARRAY_SIZE) + 1) :
                    self._minutes_data[i] = 0
                    
    def _update_hours_array(self, update_time) -> None :
        #store array in memory.
        pass

    def enqueue(self, visualizer_struct: VISUALIZER_STRUCT):
        assert isinstance(visualizer_struct, VISUALIZER_STRUCT) # assert that the input is of type VISUALIZER_STRUCT
        self._queue[visualizer_struct.event_id] = visualizer_struct # add struct to queue dictionary
        self._check_if_event_type_exists(visualizer_struct.event_type)
        self._update() 
        self._seconds_data.loc[visualizer_struct.event_type][(int(float(visualizer_struct.event_time)) % 60)] = \
            self._seconds_data.loc[visualizer_struct.event_type][(int(float(visualizer_struct.event_time)) % 60)] + 1 # add 1 to the current second in the dataframe
        
    #Create DataFrame if it is the first event of that type
    def _check_if_event_type_exists(self, event_type):
        if event_type not in self._seconds_data: 
            self._seconds_data.loc[event_type] = [0]*60
        if event_type not in self._minutes_data:            
            self._minutes_data.loc[event_type] = [0]*60
        if event_type not in self._minutes_data:      
            self._hours_data.loc[event_type] = [0]*24
        if event_type not in self._average_state_time:
            self._average_state_time[event_type] = (0,0.0)

    def dequeue(self, visualizer_struct:VISUALIZER_STRUCT):
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