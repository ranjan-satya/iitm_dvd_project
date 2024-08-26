import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc

df_satya = pd.read_csv("./Satya's Version.csv")


layout = html.Div(children=[
    html.H1("Dataset", className='content-title'),
    html.Br(),
    html.Div(
        style={'overflowX': 'auto', 'maxWidth': '1350px'},  # Enable horizontal scrolling
        children=[
            dash_table.DataTable(
                data=df_satya.to_dict('records'),
                page_size=18,
                style_cell={
                    "backgroundColor": "rgba(220, 220, 220, 0)",  # Transparent background for data cells
                    "border": "solid 1px rgba(169, 169, 169, 0.5)",  # Dark grey borders
                    "color": "rgba(0, 0, 0, 1)",  # White font color for data cells
                    "fontSize": 14,
                    "textAlign": "left",
                    "fontFamily": "DM Sans, sans-serif",
                },
                style_header={
                    "backgroundColor": "rgba(0, 0, 0, 0.4)",  # Black background for header cells
                    "fontWeight": "bold",
                    "color": "white",  # White font color for header cells
                    "padding": "10px",
                    "fontSize": 18,
                    "fontFamily": "DM Sans, sans-serif",
                },
                style_table={
                    'overflowX': 'auto',  # Enable horizontal scrolling for the table
                    'maxWidth': '1350px',  # Set maximum width for the table
                },
            )
        ]
    ),
])