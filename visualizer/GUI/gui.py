import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from threading import Thread
import pandas as pd
import datetime as dt
import time

from visualizer.i_visualizer_query_data import IVisualizerQueryData
from visualizer.GUI.Idataframe_strategy.i_dataframe_strategy import IGUIDataframeStrategy
from visualizer.GUI.Idataframe_strategy.get_seconds_strategy import GetSecondsStrategy


class GUI () :
    
    _visualizer : IVisualizerQueryData
    _plot_thread : Thread
    _state : str
    _gui_state : IGUIDataframeStrategy
    
    def __init__(self, visualizer : IVisualizerQueryData, state_name : str ) :
        self._visualizer = visualizer
        self._state = state_name
        self._plot_thread = Thread(target=self.plot).start()

        self._gui_state = GetSecondsStrategy(self._visualizer)

    def plot(self) : 
        app = Dash()
        app.layout = html.Div([
            html.H1(id="count-up"),
            dcc.Graph(id="fig"),
            dcc.Interval(id="interval", interval=1000 ),
            ])
            

        @app.callback(
            Output("fig", "figure"),
            Input("interval", "n_intervals")
        )
        def update_figure(n_intervals):

            # print(self._gui_state)
            df = self._gui_state.get_data(self._state)

            if df is not None :
                # return px.bar(pd.DataFrame())
                fig = px.bar(df)
                return fig
        
        app.run()