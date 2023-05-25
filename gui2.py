from visualizer.i_visualizer_query_data import IVisualizerQueryData
from visualizer.visualizer import Visualizer
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from threading import Thread
import pandas as pd
import datetime as dt
import time

# assuming df is your DataFrame
toState1 = "Monitor"

_visualizer = Visualizer("end")
_state = toState1

df = _visualizer.get_seconds_data(_state)

# plot the data
fig = px.bar(df, x='variable', y='value', color='index')

# display the plot
fig.show()