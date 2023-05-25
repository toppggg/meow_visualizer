import time
import pandas as pd
import threading

from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.vars import SECONDS_IN_MINUTE, MINUTES_IN_HOUR, HOURS_IN_DAY\
    , SECONDS_IN_HOUR, SECONDS_IN_DAY


class VisualizerState:
    name : str
    _last_update_time : int
    _queue : dict[VISUALIZER_STRUCT.event_id, VISUALIZER_STRUCT]
    _average_state_time:dict[VISUALIZER_STRUCT.event_type,(int,float)] # value is number of events and average time
    _seconds_data: pd.DataFrame
    _minutes_data: pd.DataFrame
    __lock = threading.Lock()

    def __init__(self, name: str):
        self._seconds_data = pd.DataFrame(columns=[i for i in range(0,SECONDS_IN_MINUTE)])
        self._minutes_data = pd.DataFrame(columns=[i for i in range(0,MINUTES_IN_HOUR)])
        self._hours_data = pd.DataFrame(columns=[i for i in range(0,HOURS_IN_DAY)])
        self._queue = {}
        self._average_state_time = {}
        self.name = name
        self._last_update_time = int(time.time()) 
        

    def _update(self) -> None :
        update_time = int(time.time())
        if update_time - self._last_update_time > 0 :
            self._update_seconds_array(update_time)

        self._last_update_time = update_time

    def _update_seconds_array(self, update_time : int) -> None :
        if (update_time // SECONDS_IN_MINUTE) - (self._last_update_time // SECONDS_IN_MINUTE) > 0 : # 6067//60 - 6046//60 = 101 - 100 = 1
            #nulstil resten af arrayet
            for i in range ((self._last_update_time % SECONDS_IN_MINUTE) + 1, SECONDS_IN_MINUTE): 
                self._seconds_data[i] = 0   #set the subsequent seconds to 0, since nothing was received
            self._convert_to_minutes(update_time)
            if (update_time // SECONDS_IN_MINUTE - self._last_update_time // SECONDS_IN_MINUTE > 1 ) \
                or (update_time % SECONDS_IN_MINUTE >= self._last_update_time % SECONDS_IN_MINUTE) : 
                for i in range (0, (self._last_update_time % SECONDS_IN_MINUTE) + 1) : # more than a min has passed, reset everything
                    self._seconds_data[i] = 0
            else :
                for i in range(0, (update_time % SECONDS_IN_MINUTE) + 1) :
                    self._seconds_data[i] = 0
        else:
            #nulstil indtil update_time
            for i in range((self._last_update_time + 1) % SECONDS_IN_MINUTE, (update_time % SECONDS_IN_MINUTE) + 1) :
                self._seconds_data[i] = 0


    def enqueue(self, visualizer_struct: VISUALIZER_STRUCT):
        assert isinstance(visualizer_struct, VISUALIZER_STRUCT) # assert that the input is of type VISUALIZER_STRUCT
        self._queue[visualizer_struct.event_id] = visualizer_struct # add struct to queue dictionary
        self._check_if_event_type_exists(visualizer_struct.event_type)
        self._update()
        if self._last_update_time // SECONDS_IN_MINUTE > int(float(visualizer_struct.event_time)) // SECONDS_IN_MINUTE:
            self._back_dated_event(visualizer_struct)
        else:
            with self.__lock:
                self._seconds_data.loc[visualizer_struct.event_type, (int(float(visualizer_struct.event_time)) % SECONDS_IN_MINUTE)] += 1


    #Create DataFrame if it is the first event of that type
    def _check_if_event_type_exists(self, event_type):
        if event_type not in self._seconds_data.index  :  

            self._seconds_data.loc[event_type] = [0]*SECONDS_IN_MINUTE
        if event_type not in self._minutes_data.index:            
            self._minutes_data.loc[event_type] = [0]*MINUTES_IN_HOUR
        if event_type not in self._minutes_data.index:      
            self._hours_data.loc[event_type] = [0]*HOURS_IN_DAY
        if event_type not in self._average_state_time:
            self._average_state_time[event_type] = (0,0.0)

    ### remove visualizer_struct from queue
    def dequeue(self, visualizer_struct:VISUALIZER_STRUCT):
        assert isinstance(visualizer_struct, VISUALIZER_STRUCT) # assert that the input is of type VISUALIZER_STRUCT
        self._check_if_event_type_exists(visualizer_struct.event_type) # check if event_type exists in the average_state_time dictionary
        with self.__lock:
            try:
                popped_visualizer_struct = self._queue.pop(visualizer_struct.event_id) # remove struct from queue dictionary
                self._update_average_time(popped_visualizer_struct, visualizer_struct)
            except KeyError:
                pass # Defensive vs code by contract, if the key does not exist. So far defensive. Could return a debug message here.
        

    ### update average time for event_type
    def _update_average_time(self, popped_visualizer_struct : VISUALIZER_STRUCT, received_visualizer_struct:VISUALIZER_STRUCT) -> None:
        
        old_n = self._average_state_time[received_visualizer_struct.event_type][0] 
        old_average = self._average_state_time[popped_visualizer_struct.event_type][1]

        new_n = old_n + 1
        time_this_event = float(received_visualizer_struct.event_time) - float(popped_visualizer_struct.event_time) 
        new_average_time = old_average + ((time_this_event - old_average) / new_n)
        new_tuple = (new_n, new_average_time)

        self._average_state_time[received_visualizer_struct.event_type] = new_tuple
        
    def get_queue_data(self):
        return self._queue
    
    def get_average_time(self, event_types : list[VISUALIZER_STRUCT.event_type]) -> dict[VISUALIZER_STRUCT.event_type, (int,float)] : 
        result = {}
        for event_type in event_types:
            try:
                dict_value = self._average_state_time[event_type]
                result[event_type] = dict_value
            except KeyError:
                continue
        return result

    def get_minutes_data(self, event_types : list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass

        # Tilføjet af Johan 19. maj 2023
    def get_seconds_data(self, event_types : list[VISUALIZER_STRUCT.event_type] = []) -> pd.DataFrame :
        timestamp = int(time.time())
        self._update()
        time_now_seconds_part = timestamp % SECONDS_IN_MINUTE 
        dataframe_sorted = self._aux_return_df_order_by_timestamp(time_now_seconds_part, self._seconds_data)
        if event_types:
            return dataframe_sorted.loc[event_types]
        else:
            return dataframe_sorted


    def get_hours_data(self, event_types:list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass # TODO: implement, 
    def get_days_data(self, event_types:list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass
    def get_months_data(self, event_types:list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass

    def get_years_data(self, event_types:list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame : 
        pass
    def _convert_to_minutes(self, update_time) -> None :
        update_time = update_time // SECONDS_IN_MINUTE
        last_update_time = self._last_update_time // SECONDS_IN_MINUTE
        ARRAY_SIZE = MINUTES_IN_HOUR
        
        ### this may not work, there are not test for this yet.
        for index, row in self._seconds_data.iterrows():
            self._minutes_data.loc[index][last_update_time % MINUTES_IN_HOUR] = row.sum()
        
        if (update_time // ARRAY_SIZE) - (last_update_time // ARRAY_SIZE) > 0 : # update has passed a new min.
            #nulstil resten af arrayet
            for i in range ((last_update_time % ARRAY_SIZE) + 1, ARRAY_SIZE): 
                self._minutes_data[i] = 0   #set the subsequent seconds to 0, since nothing was received
            self._convert_to_hour(update_time)
            if (update_time // ARRAY_SIZE - last_update_time // ARRAY_SIZE > 1 ) or \
                (update_time % ARRAY_SIZE >= last_update_time % MINUTES_IN_HOUR) : 
                for i in range (0, (last_update_time % ARRAY_SIZE) + 1) : # more than a min has passed, reset everything
                    self._minutes_data[i] = 0
            else :
                for i in range(0, (update_time % ARRAY_SIZE) + 1) :
                    self._minutes_data[i] = 0
        else:
            #nulstil indtil update_time
            for i in range(last_update_time+1, (update_time % ARRAY_SIZE) + 1) :
                    self._minutes_data[i] = 0

    def _convert_to_hour(self,update_time) -> None:
        #store the last 60 minutes in the hour array in static memory
        #otherwise identical to the _convert_to_minutes function just with arraysize = MINUTES_IN_HOUR (= 24), 
        #and then it should call the _convert_to_day function
        pass
    def _convert_to_day():
        pass
        #identical to the _convert_to_minutes function just with 
    def _convert_to_month():
        pass
    def _convert_to_year():
        pass

        ### Sort the dataframe so that time.time() is the last element in the array, and the first element is the oldest
    def _aux_return_df_order_by_timestamp(self, timestamp, dataframe: pd.DataFrame) -> pd.DataFrame :
        cols = dataframe.columns.tolist()
        new_cols = cols[timestamp + 1:] + cols[:timestamp + 1]
        return dataframe[new_cols]
    
    def get_event_id(self,event_id) -> VISUALIZER_STRUCT :
        if event_id in self._queue:
            return self._queue[event_id]
        
    def _back_dated_event(self, visualizer_struct: VISUALIZER_STRUCT) -> None:
        update_time = self._last_update_time
        event_time = visualizer_struct.event_time
        if event_time // SECONDS_IN_DAY - update_time // SECONDS_IN_DAY > 1:
            pass #Add to day array and potentially to hours array.
        elif event_time // SECONDS_IN_HOUR - update_time // SECONDS_IN_HOUR > 1: 
            pass # Add to Hour array and potential minutes array
        else:
            with self.__lock:
                self._minutes_data.loc[visualizer_struct.event_type, ((int(float(visualizer_struct.event_time)) // SECONDS_IN_MINUTE) % MINUTES_IN_HOUR)] += 1
                if update_time - event_time <= SECONDS_IN_MINUTE:
                    self._seconds_data.loc[visualizer_struct.event_type, (int(float(visualizer_struct.event_time)) % SECONDS_IN_MINUTE)] += 1