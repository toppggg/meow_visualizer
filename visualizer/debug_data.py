from visualizer.visualizer_struct import VISUALIZER_STRUCT

class DebugData:
    _debug_messages:list[VISUALIZER_STRUCT]


    def __init__(self) -> None:
        self._debug_messages:list[VISUALIZER_STRUCT] = []

    def add_debug_struct(self, struct :VISUALIZER_STRUCT) : 
        self._debug_messages.append(struct)

    def get_debug_messages(self) -> list[VISUALIZER_STRUCT] :
        return self._debug_messages
