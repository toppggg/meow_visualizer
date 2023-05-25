from visualizer.i_visualizer_query_data import IVisualizerQueryData
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from threading import Thread
import pandas as pd
import datetime as dt


class GUI () :
    
    _visualizer : IVisualizerQueryData
    _plot_thread : Thread
    _state : str
    
    def __init__(self, visualizer : IVisualizerQueryData, state_name : str) :
        self._visualizer = visualizer
        self._state = state_name
        self._plot_thread = Thread(target=self.plot).start()

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
            # print(self._visualizer.get_seconds_data(self._state))


            df = self._visualizer.get_seconds_data(self._state)
            # # fig = px.bar(df.T)
            # df = pd.DataFrame()  # your dataframe here
            # time_this_round = int(df.T.index.values.tolist()[-1])
            # print()
            # xs = [""]*60
            # for i in range (0,60):
            #     xs[i] = dt.datetime.fromtimestamp(i).strftime('%H:%M:%S')
            
            # # df_alt = pd.DataFrame(data = df.T.values, columns=df.T.columns, index=xs)  

            # column_names = str(df.columns.values.tolist())
            # # rearrange the columns
            # # columns_ordered = [str(i) for i in range(32, 60)] + [str(i) for i in range(0, 32)]

            # # df = df[columns_ordered]
            # df_long = df.T.reset_index().melt(id_vars='index', value_vars=xs)
            # # df_long = df.reset_index().melt(x ='variable', id_vars='index', value_vars=column_names)
            # # fig = px.bar(df_long, x='variable', y='value', color='index')
            # # fig = px.bar(df.T, x = df.T.)
            # print(df.head())

            # print("Transposing")
            # df = df.T
            # print(df.head())
            # # # df.T.row
            # fig = px.bar(df_long)
            fig = df.plot.bar()

        app.run()