import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from threading import Thread
import pandas as pd

from visualizer.i_visualizer_query_data import IVisualizerQueryData
from visualizer.GUI.Idataframe_strategy.i_dataframe_strategy import IGUIDataframeStrategy
from visualizer.GUI.Idataframe_strategy.get_seconds_strategy import GetSecondsStrategy
from visualizer.GUI.Idataframe_strategy.get_minutes_strategy import GetMinutesStrategy
from visualizer.GUI.Idataframe_strategy.get_hours_strategy import GetHoursStrategy


class GUI () :
    
    _visualizer : IVisualizerQueryData
    _plot_thread : Thread
    _state : str
    _all_states : list[str]
    _gui_state : IGUIDataframeStrategy
    _time_options = ['Seconds', 'Minutes', 'Hours']
    _event_types : list[str]
    _unique_event_type : str

    def __init__(self, visualizer : IVisualizerQueryData, state_name : str ) :
        self._visualizer = visualizer
        self._state = state_name
        self._event_types = ["all"]
        self._gui_state = GetSecondsStrategy(self._visualizer)
        self._unique_event_type = "all"
        self._all_states = self._visualizer.get_all_states()
        self._plot_thread = Thread(target=self.plot).start()

    def plot(self) : 
        app = Dash()
        app.layout = html.Div([
            html.Div([
            html.H2(id="count-up1"),
            dcc.Dropdown(
                id='state-dropdown',
                options=[{'label': i, 'value': i} for i in self._visualizer.get_all_states()],
                value=self._state
            ),
            dcc.Dropdown(
                id='strategy-dropdown',
                options=[{'label': i, 'value': i} for i in self._time_options],
                value='Seconds'
            ),
            dcc.Dropdown(
                id='event_type-dropdown',
                options=[{'label': i, 'value': i} for i in self._event_types],
                value=self._unique_event_type
            ),
            ]),
            html.Div([
                html.H1(id="count-up"),
                dcc.Graph(id="fig"),
                dcc.Interval(id="interval", interval=1000 ),
            ]),
        ])
            

        @app.callback(
            Output("fig", "figure"),
            Input("interval", "n_intervals")
        )
        def update_figure(n_intervals):

            # print(self._gui_state)
            if self._unique_event_type == "all" :
                df = self._gui_state.get_data(self._state, [])
            else :
                df = self._gui_state.get_data(self._state, [self._unique_event_type])
            # self._event_types = ['all']+ df.columns.tolist()
            # print(self._event_types)
            if df is not None :
                # return px.bar(pd.DataFrame())
                fig = px.bar(df)
                return fig
        

        @app.callback(
            [Output('state-dropdown', 'options'),
            Output('event_type-dropdown', 'value')],
            Input('state-dropdown', 'value'),
            Input('event_type-dropdown', 'value')
        )
        def update_dropdown(state_value, event_type_value):
            # this will change the value of self._state when the dropdown selection changes
            self._state = state_value
            self._all_states = self._visualizer.get_all_states()
            state_keys = self._visualizer.get_event_average_time_in_state(self._state).keys()
            updated_event_type = "all"
            if event_type_value in state_keys :
                updated_event_type = event_type_value
            return  [{'label': i, 'value': i} for i in self._all_states], updated_event_type
            

        @app.callback(
        Output('strategy-dropdown', 'value'),
        Input('strategy-dropdown', 'value')
        )
        def update_dropdown(value):
            # this will change the value of self._state when the dropdown selection changes
            match value :
                case 'Seconds' :
                    self._gui_state = GetSecondsStrategy(self._visualizer)
                case 'Minutes' :
                    self._gui_state = GetMinutesStrategy(self._visualizer)
                case _ :
                    pass
            return value

        @app.callback(
            Output('event_type-dropdown', 'options'), 
            Input('event_type-dropdown', 'value')
        )
        def update_dropdown(value):
            self._unique_event_type = value
            print(value)
            self._event_types = ["all"] + list(self._visualizer.get_event_average_time_in_state(self._state).keys())
            return [{'label': i, 'value': i} for i in self._event_types]

        app.run()