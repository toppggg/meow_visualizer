from dataclasses import dataclass

@dataclass
class VISUALIZER_STRUCT:
    event_type : str = ""
    event_id : str = ""
    previous_state : str = ""
    current_state : str = ""
    event_origin_time : str = ""
    event_time : str = ""
    debug_message: str = ""
    optional_info : str = ""
    