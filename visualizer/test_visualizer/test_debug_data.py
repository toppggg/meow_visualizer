import unittest
from visualizer.debug_data import DebugData
from visualizer.visualizer_struct import VISUALIZER_STRUCT


class DebugDataTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()


    def TestInit(self):
        debug = DebugData

        self.assertIsInstance(debug.debug_messages, list[VISUALIZER_STRUCT])

    ### Test if Add_Debug_struct add Visualizer struct to debug messages ###
    def TestAddDebugStruct(self) : 
        debug = DebugData
        vs = VISUALIZER_STRUCT(debug_message="Useful Debug message")

        self.assertNotIn(vs, debug.debug_messages)

        debug.add_debug_struct(vs)

        self.assertIn(vs, debug.debug_messages)
    
    ### Test if get_debug_messages returns a list of structs  ###
    def TestGetDebugMessage (self) : 
        
        debug = DebugData
        vs = VISUALIZER_STRUCT(debug_message="Useful Debug message")

        debug.debug_messages.insert(vs)

        self.assertIn(vs, debug.debug_messages)

        message = debug.get_debug_messages()

        self.assertIn(vs , message)    

    ### Test if get_debug_messages returns an empty list if none exist ###
    def TestGetDebugMessage (self) : 
        
        debug = DebugData
        message = debug.get_debug_messages()
        self.assertEqual([] , message)
