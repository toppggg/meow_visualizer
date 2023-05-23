from multiprocessing import Queue
from visualizer.visualizer_struct import VISUALIZER_STRUCT

class IVisualizerReceiveData() :
    receive_channel : Queue

    def _add_event(self, visualizer_struct: VISUALIZER_STRUCT) -> None :
        """what happens in the visualizer when an event is received  """

    def _update(self) -> None :
        """"How often should the visualizer update, and what should happen.""" # This could include backup from volatile to static memory.

