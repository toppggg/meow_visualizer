import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
import dash
from threading import Thread, Lock
import pandas as pd
import datetime as dt

from visualizer.i_visualizer_query_data import IVisualizerQueryData
from visualizer.GUI.Idataframe_strategy.i_dataframe_strategy import IGUIDataframeStrategy
from visualizer.GUI.Idataframe_strategy.get_seconds_strategy import GetSecondsStrategy
from visualizer.GUI.Idataframe_strategy.get_minutes_strategy import GetMinutesStrategy
from visualizer.GUI.Idataframe_strategy.get_hours_strategy import GetHoursStrategy


class GUI () :
    _gui_states : list[str]
    _visualizer : IVisualizerQueryData
    _plot_thread : Thread
    _state : str
    _all_states : list[str]
    _gui_strategy : IGUIDataframeStrategy
    _time_options = ['Seconds', 'Minutes', 'Hours']
    _event_types : list[str]
    _unique_event_type : str
    _unique_id : str
    def __init__(self, visualizer : IVisualizerQueryData, state_name : str ) :
        self._visualizer = visualizer
        self._state = state_name
        self._event_types = ["all"]
        self._gui_strategy = GetSecondsStrategy(self._visualizer)
        self._unique_event_type = "all"
        self._all_states = self._visualizer.get_all_states()
        self._gui_states = ["show-graph", "show-state-events", "show-debug", "show-unique-id"]
        self._plot_thread = Thread(target=self.plot)

        self._plot_thread.start() #dont add things after the threat is started, might result in unexpected behaviour

    def event_type_stats(self) -> list[str] :
        stats = []
        average_time_dict = {}
        if self._unique_event_type == "all" :
                average_time_dict = self._visualizer.get_event_average_time_in_state(self._state)
        else :
            average_time_dict = self._visualizer.get_event_average_time_in_state(self._state,[self._unique_event_type])


        events_in_state = self._visualizer.count_events_by_rule_in_state(self._state)
        if self._unique_event_type == "all" :
            event_types = self._event_types
        else : 
            event_types = [self._unique_event_type]
        for event_type in event_types :

            if event_type != "all" :
                try:
                    combined_info = str(event_type).ljust(25, ' ') + "|" + str(events_in_state[event_type]).rjust(25, ' ') + "|" + str(average_time_dict[event_type][0]).rjust(25, ' ') + "|" + str(round(average_time_dict[event_type][1],3)).rjust(25, ' ') + "s"
                    stats = stats + [combined_info] 
                except:
                    continue                            

        return stats
        
        

    def plot(self): 
        app = Dash()
        

        def state_graphs() :
            return html.Div([
                
                html.Div([
                html.H1(id="gui_state"),
                dcc.Dropdown(
                    id='graph_debug-dropdown',
                    options=[{'label': i, 'value': i} for i in self._gui_states],
                    value= self._gui_states[0]
                ),
                ]),
                html.A(html.Button('Refresh Data'),href='/'),
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
                    dcc.Interval(id="interval", interval=1000),
                ]),

                html.Div(id='stats', style={'whiteSpace': 'pre-wrap'})
            ])

        def state_debug():
            debugmessages = self._visualizer.get_debug_messages()
            debug_list = []
            for message in debugmessages :
                debug_list += [str(message)]
            
            return html.Div([
                html.Div([
                html.H1(id="gui_state"),
                dcc.Dropdown(
                    id='graph_debug-dropdown',
                    options=[{'label': i, 'value': i} for i in self._gui_states],
                    value= "show-debug"
                    )
                ]),
                html.A(html.Button('Refresh Data'),href='/'),
                html.Div(id='textarea', style={'whiteSpace': 'pre-line'}, children= [html.Div(i) for i in debug_list])
            ])
        
        def state_all_data():
            events_in_state = self._visualizer.get_events_in_state(self._state)
            result = []
            for event in events_in_state :
                result += [str(event)]
            
            return html.Div([
                html.Div([
                html.H1(id="gui_state"),
                dcc.Dropdown(
                    id='graph_debug-dropdown',
                    options=[{'label': i, 'value': i} for i in self._gui_states],
                    value= "show-state-events"
                    )
                ]),
                html.A(html.Button('Refresh Data'),href='/'),
                
                html.Div([
                    dcc.Dropdown(
                        id='state-data-dropdown',
                        options=[{'label': i, 'value': i} for i in self._visualizer.get_all_states()],
                        value=self._state
                    )
                ]),
                html.Div(id='text_area_state', style={'whiteSpace': 'pre-line'}, children= [html.Div(i) for i in result])
            ])
        
        def search_id():
            return html.Div([
                html.Div([
                html.H1(id="gui_state"),
                dcc.Dropdown(
                    id='graph_debug-dropdown',
                    options=[{'label': i, 'value': i} for i in self._gui_states],
                    value= "show-unique-id"
                    )
                ]),
                html.A(html.Button('Refresh Data'),href='/'),
                html.H2(id="search for event id"),
                html.Div([
                        dcc.Textarea( 
                        id='text_field',
                        value='input eventID',
                        style={'width': '100%', 'height': 20}
                    ),
                    html.Button('Submit', id='textarea-state-example-button', n_clicks=0),
                    html.Div(id='textarea', style={'whiteSpace': 'pre-line'})        
                ]),
            ])
        
        @app.callback(
            Output('text_area_state',"children" ),
            Input('state-data-dropdown', 'value')
        )
        def update_events_in_state(value):
            self._state = value
            events_in_state = self._visualizer.get_events_in_state(self._state)
            
            result = []
            for event in events_in_state :
                result += [html.Div(str(event))]
            return result
            
        @app.callback(
            Output('graph_debug-dropdown', 'value'),
            Input('graph_debug-dropdown', 'value')
        )    
        def update_dropdown(value):
            # this will change the value of self._state when the dropdown selection changes
            # ["show-graph", "show-debug"]
            match value :
                case 'show-graph' :
                    app.layout = state_graphs()
                case 'show-debug' :
                    app.layout = state_debug()
                case 'show-unique-id' :
                    app.layout = search_id()
                case 'show-state-events' :
                    app.layout = state_all_data()
                case _ :
                    pass
            return value


        @app.callback(
            Output("textarea", "children"),
            Input('textarea-state-example-button', 'n_clicks'),
            State("text_field", "value")
        )
        def update_text_field (n_clicks, value) : 
            result = str(self._visualizer.get_event_id(value))
            return result
                

        @app.callback(
            Output("fig", "figure"),
            Input("interval", "n_intervals")
        )
        def update_figure(n_intervals):
            if self._unique_event_type == "all" :
                df = self._gui_strategy.get_data(self._state, [])
            else :
                df = self._gui_strategy.get_data(self._state, [self._unique_event_type])
            if df is not None :
                
                fig = px.bar(df, labels={
                    'variable' : 'Event Type', 
                    'value' : 'events'
                })
                return fig

        @app.callback(
            Output("stats", "children"),
            Input("interval", "n_intervals")
        )
        def update_stats(n_intervals):
            return  [html.Div("Event_type".ljust(25, ' ') +"| currently in state".ljust(26, ' ') 
                + "| events completed ".ljust(26, ' ') 
                + "| average time in state (for completed events)", style={'whiteSpace': 'pre-wrap', 'font-family':'monospace'} )] \
                + [html.Div("-"*123, style={'whiteSpace': 'pre-wrap', 'font-family':'monospace'})]\
                + [html.Div(i, style={'whiteSpace': 'pre-wrap', 'font-family':'monospace'}) for i in self.event_type_stats()]

        @app.callback(
            [Output('state-dropdown', 'options'),
            Output('event_type-dropdown', 'value')],
            Input('state-dropdown', 'value'),
            Input('event_type-dropdown', 'value'),
            Input("interval", "n_intervals")
        )
        def update_dropdown(state_value, event_type_value, n_intervals):
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
                    self._gui_strategy = GetSecondsStrategy(self._visualizer)
                case 'Minutes' :
                    self._gui_strategy = GetMinutesStrategy(self._visualizer)
                case 'Hours' :
                    self._gui_strategy = GetHoursStrategy(self._visualizer)
                case _ :
                    pass
            return value

        @app.callback(
            Output('event_type-dropdown', 'options'), 
            Input('event_type-dropdown', 'value')
        )
        def update_dropdown(value):
            self._unique_event_type = value
            self._event_types = ["all"] + list(self._visualizer.get_event_average_time_in_state(self._state).keys())
            return [{'label': i, 'value': i} for i in self._event_types]
        
        app.layout = state_graphs()
        app.run()


        @app.callback(
            Output('state-data-dropdown', 'options'),
            Output('textarea', 'options'),
            Input('state-data-dropdown', 'value')
        )
        def update_dropdown(state_value):
            # this will change the value of self._state when the dropdown selection changes
            self._state = state_value
            self._all_states = self._visualizer.get_all_states()
            return  [{'label': i, 'value': i} for i in self._all_states], [{'label': i, 'value': i} for i in self._gui_states]
        