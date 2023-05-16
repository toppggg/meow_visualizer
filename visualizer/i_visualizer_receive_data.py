from visualizer_struct import VISUALIZER_STRUCT
from multiprocessing.connection import Connection

class IVisualizerReceiveData() :
    receive_channel : Connection

    def _add_event(self, visualizer_struct: VISUALIZER_STRUCT) -> None :
        """what happens in the visualizer when an event is received  """

    def _update(self) -> None :
        """"How often should the visualizer update, and what should happen.""" # This could be doing backup from volatile to static memory.

