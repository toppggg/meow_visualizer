from visualizer.visualizer_struct import VISUALIZER_STRUCT

class DebugData:
    debug_messages:list[VISUALIZER_STRUCT]


    def __init__(self) -> None:
        self.debug_messages : list[VISUALIZER_STRUCT] = []

    def add_debug_struct(self, struct :VISUALIZER_STRUCT) : 
        self.debug_messages.append(struct)

    def get_debug_messages(self) -> list[VISUALIZER_STRUCT] :
        return self.debug_messages
