import unittest
from visualizer_state import VisualizerState
from visualizer_struct import VISUALIZER_STRUCT
import time



class EventQueueDataTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

    def TestInit(self):
        visualizer_state = VisualizerState("monitor")

        self.assertEqual(visualizer_state.name, "monitor")


    ### Test for enqueue ###
    def testEnqueueVisualizerStructNoDebugMessage(self) :
        time = str(time.time())
        eventId = "idnr1"
        vs = VISUALIZER_STRUCT("rule1",eventId, "", "Monitor", time, time, "", "OptionalInfo")
        visualizer_state = VisualizerState("testState")

        self.assertNotIn(vs,visualizer_state._queue)

        visualizer_state.enqueue(vs)

        self.assertIn(vs,visualizer_state._queue)

    def testEnqueueVisualizerStructDebugMessage(self) :
        time = str(time.time())
        eventId = "idnr1"
        vs = VISUALIZER_STRUCT("rule1",eventId, "", "Monitor", time, time, "random message", "OptionalInfo")
        visualizer_state = VisualizerState("testState")

        self.assertNotIn(vs,visualizer_state._queue)

        visualizer_state.enqueue(vs)

        self.assertIn(vs,visualizer_state._queue)        


    def testEnqueueNoneVisualizerStructWrongType(self) :
        time = str(time.time())
        eventId = "idnr1"
        vs = ("random info", eventId, "", "Monitor", time, time, "random message", "OptionalInfo")
        visualizer_state = VisualizerState("testState")

        self.assertNotIn(vs,visualizer_state._queue)       

        with self.assertRaises(TypeError):
                visualizer_state.enqueue(vs)               

        self.assertNotIn(vs, visualizer_state._queue)       


    ### Test for dequeue ###
    
    def testDequeueVisualizerStructNoDebugMessage(self) :
        time = str(time.time())
        eventId = "idnr1"
        vs = VISUALIZER_STRUCT("rule1", eventId, "", "Monitor", time, time, "", "OptionalInfo")
        visualizer_state = VisualizerState("testState")
        visualizer_state._queue[eventId] = vs

        self.assertIn(vs,visualizer_state._queue) #arrange

        visualizer_state.dequeue(eventId) #act

        self.assertNotIn(vs,visualizer_state._queue) #assert

    def testDequeueVisualizerStructWrongType(self) :
        time = str(time.time())
        eventId = 1
        vs = ("rule1", eventId, "", "Monitor", time, time, "", "OptionalInfo")
        visualizer_state = VisualizerState("testState")
        visualizer_state._queue[eventId] = vs

        self.assertIn(vs,visualizer_state._queue) 

        with self.assertRaises(TypeError):
                visualizer_state.dequeue(eventId)

        self.assertIn(vs,visualizer_state._queue)


        
        



