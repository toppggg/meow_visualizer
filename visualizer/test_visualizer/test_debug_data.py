import unittest

from visualizer.debug_data import DebugData
from visualizer.visualizer_struct import VISUALIZER_STRUCT


class DebugDataTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()


    def testInit(self):
        debug = DebugData()

        self.assertIsInstance(debug._debug_messages, list)

    ### Test if Add_Debug_struct add Visualizer struct to debug messages ###
    def testAddDebugStruct(self) : 
        debug = DebugData()
        vs = VISUALIZER_STRUCT(debug_message="Useful Debug message")

        self.assertNotIn(vs, debug._debug_messages)

        debug.add_debug_struct(vs)

        self.assertIn(vs, debug._debug_messages)
    
    ### Test if get_debug_messages returns a list of structs  ###
    def testGetDebugMessage(self) : 
        
        debug = DebugData()
        vs = VISUALIZER_STRUCT(debug_message="Useful Debug message")

        debug._debug_messages= debug._debug_messages + [vs]

        self.assertIn(vs, debug._debug_messages)

        message = debug.get_debug_messages()

        self.assertIn(vs , message)    

    ### Test if get_debug_messages returns an empty list if none exist ###
    def testGetDebugMessageEmpty(self) : 
        
        debug = DebugData()
        message = debug.get_debug_messages()
        self.assertEqual([] , message)
