import time
import pandas as pd

from visualizer.visualizer_struct import VISUALIZER_STRUCT
from visualizer.vars import SECONDS_IN_MINUTE, MINUTES_IN_HOUR, HOURS_IN_DAY,\
    SECONDS_IN_HOUR, SECONDS_IN_DAY


class VisualizerState:
    name : str
    _last_update_time : int
    _queue : dict[VISUALIZER_STRUCT.event_id, VISUALIZER_STRUCT]
    _average_state_time:dict[VISUALIZER_STRUCT.event_type,(int,float)] # value is number of events and average time
    _seconds_data: pd.DataFrame
    _minutes_data: pd.DataFrame

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

    def _update_seconds_array(self, update_time) -> None :
        if (update_time // SECONDS_IN_MINUTE) - (self._last_update_time // SECONDS_IN_MINUTE) > 0 : # 6067//60 - 6046//60 = 101 - 100 = 1
            #nulstil resten af arrayet
            for i in range ((self._last_update_time % SECONDS_IN_MINUTE) + 1, SECONDS_IN_MINUTE): 
                self._seconds_data[i] = 0   #set the subsequent seconds to 0, since nothing was received
            self._convert_to_minutes(update_time)
            if (update_time // SECONDS_IN_MINUTE - self._last_update_time // SECONDS_IN_MINUTE > 1 ) or (update_time % SECONDS_IN_MINUTE >= self._last_update_time % SECONDS_IN_MINUTE) : 
                for i in range (0, (self._last_update_time % SECONDS_IN_MINUTE) + 1) : # more than a min has passed, reset everything
                    self._seconds_data[i] = 0
            else :
                for i in range(0, (update_time % SECONDS_IN_MINUTE) + 1) :
                    self._seconds_data[i] = 0
        else:
            #nulstil indtil update_time
            for i in range(self._last_update_time+1, (update_time % SECONDS_IN_MINUTE) + 1) :
                    self._seconds_data[i] = 0


    def enqueue(self, visualizer_struct: VISUALIZER_STRUCT):
        assert isinstance(visualizer_struct, VISUALIZER_STRUCT) # assert that the input is of type VISUALIZER_STRUCT
        self._queue[visualizer_struct.event_id] = visualizer_struct # add struct to queue dictionary
        self._check_if_event_type_exists(visualizer_struct.event_type)
        self._update() 
        self._seconds_data.loc[visualizer_struct.event_type][(int(float(visualizer_struct.event_time)) % SECONDS_IN_MINUTE)] = \
            self._seconds_data.loc[visualizer_struct.event_type][(int(float(visualizer_struct.event_time)) % SECONDS_IN_MINUTE)] + 1 # add 1 to the current second in the dataframe
        
    #Create DataFrame if it is the first event of that type
    def _check_if_event_type_exists(self, event_type):
        if event_type not in self._seconds_data: 
            self._seconds_data.loc[event_type] = [0]*SECONDS_IN_MINUTE
        if event_type not in self._minutes_data:            
            self._minutes_data.loc[event_type] = [0]*MINUTES_IN_HOUR
        if event_type not in self._minutes_data:      
            self._hours_data.loc[event_type] = [0]*HOURS_IN_DAY
        if event_type not in self._average_state_time:
            self._average_state_time[event_type] = (0,0.0)

    # Tilføjet af Johan 19. maj 2023
    def dequeue(self, visualizer_struct:VISUALIZER_STRUCT):
        assert isinstance(visualizer_struct, VISUALIZER_STRUCT) # assert that the input is of type VISUALIZER_STRUCT
        popped_visualizer_struct = self._queue.pop(visualizer_struct.event_id) # remove struct from queue dictionary
        self._update_average_time(popped_visualizer_struct, visualizer_struct)
        

    # Tilføjet af Johan 19. maj 2023
    def _update_average_time(self, popped_visualizer_struct : VISUALIZER_STRUCT, received_visualizer_struct:VISUALIZER_STRUCT) -> None:
        
        # self._average_state_time[received_visualizer_struct.event_type][0] = self._average_state_time[received_visualizer_struct.event_type][0] + 1
        # self._average_state_time[received_visualizer_struct.event_type][1] = \
        #     self._average_state_time[popped_visualizer_struct.event_type][1] + \
        #         ((float(received_visualizer_struct.event_time) - float(popped_visualizer_struct.event_time) - self._average_state_time[popped_visualizer_struct.event_type][1]) \
        #          /(self._average_state_time[received_visualizer_struct.event_type][0] + 1))
                # running average, (old average + ((new value - old average) / (n+1)))

        #easier to read version:
        old_n = self._average_state_time[received_visualizer_struct.event_type][0] 
        old_average = self._average_state_time[popped_visualizer_struct.event_type][1]

        new_n = old_n + 1
        time_this_event = float(received_visualizer_struct.event_time) - float(popped_visualizer_struct.event_time) 
        new_average_time = old_average + ((time_this_event - old_average) / new_n)
        new_tuple = (new_n, new_average_time)
        self._average_state_time[received_visualizer_struct.event_type] = new_tuple
        # self._average_state_time[received_visualizer_struct.event_type][0] = new_n
        # self._average_state_time[received_visualizer_struct.event_type][1] = new_average_time
        
    def get_queue_data(self):
        pass

    def get_minutes_data(self, event_types : list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass

        # Tilføjet af Johan 19. maj 2023
    def get_seconds_data(self, event_types: list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        timestamp = int(time.time())
        self._update()
        time_now_seconds_part = timestamp % SECONDS_IN_MINUTE 
        dataframe_sorted = self._aux_return_df_order_by_timestamp(time_now_seconds_part, self._seconds_data)
        if event_types:
            return dataframe_sorted[event_types]
        else:
            return dataframe_sorted


    def get_hours_data(event_types:list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass
    def get_days_data(event_types:list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass
    def get_months_data(event_types:list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame :
        pass

    def get_years_data(event_types:list[VISUALIZER_STRUCT.event_type]) -> pd.DataFrame : 
        pass
    def _convert_to_minutes(self, update_time) -> None :
        update_time = update_time // SECONDS_IN_MINUTE
        last_update_time = self._last_update_time // SECONDS_IN_MINUTE
        ARRAY_SIZE = MINUTES_IN_HOUR
        
        ### this may not work, there are not test for this yet.
        for index, row in self._seconds_data.iterrows():
            self._minutes_data.loc[index][last_update_time % MINUTES_IN_HOUR] = row.sum
        
        
        if (update_time // ARRAY_SIZE) - (last_update_time // ARRAY_SIZE) > 0 : # update has passed a new min.
            #nulstil resten af arrayet
            for i in range ((last_update_time % ARRAY_SIZE) + 1, ARRAY_SIZE): 
                self._minutes_data[i] = 0   #set the subsequent seconds to 0, since nothing was received
            self._convert_to_hour(update_time)
            if (update_time // ARRAY_SIZE - last_update_time // ARRAY_SIZE > 1 ) or (update_time % ARRAY_SIZE >= last_update_time % MINUTES_IN_HOUR) : 
                for i in range (0, (last_update_time % ARRAY_SIZE) + 1) : # more than a min has passed, reset everything
                    self._minutes_data[i] = 0
            else :
                for i in range(0, (update_time % ARRAY_SIZE) + 1) :
                    self._minutes_data[i] = 0
        else:
            #nulstil indtil update_time
            for i in range(last_update_time+1, (update_time % ARRAY_SIZE) + 1) :
                    self._minutes_data[i] = 0

    def _convert_to_hour():
        #store the last 60 minutes in the hour array in static memory
        pass
    def _convert_to_day():
        pass
    def _convert_to_month():
        pass
    def _convert_to_year():
        pass

        # Tilføjet af Johan 19. maj 2023
    def _aux_return_df_order_by_timestamp(timestamp, dataframe: pd.DataFrame) -> pd.DataFrame :
        cols = dataframe.columns.tolist()
        new_cols = cols[timestamp:] + cols[:timestamp]
        return dataframe[new_cols]
