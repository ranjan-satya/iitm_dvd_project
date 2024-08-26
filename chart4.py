import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

df_satya = pd.read_csv("./Satya's Version.csv")

# Global Preprocessing
#-------------------------------------------------------------------------------
unknown_voting_status_index_list = df_satya[(df_satya['Q25_1']==-1) | (df_satya['Q25_2']==-1) | (df_satya['Q25_3']==-1) | (df_satya['Q25_4']==-1) | (df_satya['Q25_5']==-1) | (df_satya['Q25_6']==-1)].index.tolist()
df_with_known_voting_status = df_satya.drop(unknown_voting_status_index_list)

# Util Functions
#-------------------------------------------------------------------------------

def filter_data_for_perception(df_with_known_voting_status, education, race, income):
    df_filtered_for_perception = df_with_known_voting_status
    if education != 'All':
        df_filtered_for_perception = df_with_known_voting_status[df_with_known_voting_status['Education'] == education]

    if race != 'All':
        df_filtered_for_perception = df_filtered_for_perception[df_filtered_for_perception['Race'] == race]

    if income != 'All':
        df_filtered_for_perception = df_filtered_for_perception[df_filtered_for_perception['Income_cat'] == income]
    return df_filtered_for_perception

def prepare_dataframe_for_perception(df_filtered_for_perception):
    df_perception_columns = ['Perception About Union Leaders', 'Perception About Company Leaders','No. of Voters']
    ul_perception_values = [-2,-1,0,1,2]
    ul_perception_options = [5,2,3,4,1]
    cl_perception_values = [-2,-1,0,1,2]
    cl_perception_options = [5,2,3,4,1]

    df_perception = pd.DataFrame(columns=df_perception_columns)

    for ul in range(len(ul_perception_values)):
        for cl in range(len(cl_perception_values)):
            count = df_filtered_for_perception[(df_filtered_for_perception['Q12'] == cl_perception_options[cl]) &
                                    (df_filtered_for_perception['Q13'] == ul_perception_options[ul]) & 
                                    (
                                    (df_filtered_for_perception['Q25_1'] == 1) |
                                    (df_filtered_for_perception['Q25_3'] == 1) |
                                    (df_filtered_for_perception['Q25_5'] == 1) |
                                    (df_filtered_for_perception['Q25_2'] == 1) |
                                    (df_filtered_for_perception['Q25_4'] == 1) |
                                    (df_filtered_for_perception['Q25_6'] == 1)
                                    )
                                    ].shape[0]      
            df_perception.loc[len(df_perception.index)] = [ul_perception_values[ul], cl_perception_values[cl], count]
    return df_perception

def create_fig_for_perception(df_perception):
    # Create a scatter plot with a specific color for the bubbles
    fig = px.scatter(
        df_perception,
        x="Perception About Union Leaders",
        y="Perception About Company Leaders",
        size="No. of Voters",
        color="No. of Voters",
        color_continuous_scale='Portland',
        log_x=False,
        size_max=60,
        opacity=1,
    )

    # Update layout to change the axis line color and position them at (0,0)
    fig.update_layout(
        xaxis=dict(
            zeroline=True,  # Show the zero line
            zerolinecolor='rgba(101, 101, 101, 0.4)',  # Set the zero line color
            zerolinewidth=1,  # Set the zero line width
            title='Perception About Union Leaders',  # Optional: Add title to x-axis
            anchor='y',  # Anchor to y-axis
            tickvals=[-2, -1, 0, 1, 2],  # Specify the tick values
            ticktext=['-2', '-1', '0', '1', '2'],  # Specify the tick labels
            gridcolor='rgba(178, 178, 178, 0.4)',  # Set the grid line color to grey
            gridwidth=1,  # Set the grid line width
        ),
        yaxis=dict(
            zeroline=True,  # Show the zero line
            zerolinecolor='rgba(101, 101, 101, 0.4)',  # Set the zero line color
            zerolinewidth=1,  # Set the zero line width
            title='Perception About Company Leaders',  # Optional: Add title to y-axis
            anchor='x',  # Anchor to x-axis
            gridcolor='rgba(178, 178, 178, 0.4)',  # Set the grid line color to grey
            gridwidth=1,  # Set the grid line width
        ),
        height=650, 
        width=1300, 
        plot_bgcolor='rgba(255, 255, 255, 0)',  # Set plot background color to black
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to black
        font=dict(color='black', family='DM Sans, sans-serif', size=16)  # Set text color to white
    )
    return fig

# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
layout = html.Div([

    html.H1("Correlation of Voter Turnout with Perception about leaders", className="content-title"),
    html.Div(className='dropdown-wrapper-horizontal-chart', children=[
            html.Img(src='/assets/education.png', style={'height': '20px', 'margin-right': '10px', 'margin-bottom': '8px'}),
            html.Div(className='content-text', children='Education: ',
                style={'margin-right': '10px', 'padding-bottom': '5px'}),
            dcc.Dropdown(
                id='select_education',
                options=[
                    {"label": "All", "value": "All"},
                    {"label": "College", "value": "College"},
                    {"label": "High school or less", "value": "High school or less"}
                ],
                multi=False,
                value="All",
                className='dash-dropdown',
                style={
                    'width': '200px', 
                    'borderRadius': '20px',
                    'fontFamily': 'DM Sans, sans-serif',
                    'fontWeight': '400',
                    'fontSize' : '19px',
                    'background-color': 'rgba(255, 255, 255, 0.6)',
                },
            ),
            html.Img(src='/assets/ethnic.png', style={'height': '25px', 'margin-left': '30px','margin-right': '10px', 'margin-bottom': '8px'}),
            html.Div(className='content-text', children='Race: ',
                style={'margin-right': '10px', 'padding-bottom': '5px'}),
            dcc.Dropdown(
                id='select_race',
                options=[
                    {"label": "All", "value": "All"},
                    {"label": "White", "value": "White"},
                    {"label": "Black", "value": "Black"},
                    {"label": "Mixed", "value": "Mixed"},
                    {"label": "Hispanic", "value": "Hispanic"}
                ],
                multi=False,
                value="All",
                className='dash-dropdown',
                style={
                    'width': '200px', 
                    'borderRadius': '20px',
                    'fontFamily': 'DM Sans, sans-serif',
                    'fontWeight': '400',
                    'fontSize' : '19px',
                    'background-color': 'rgba(255, 255, 255, 0.6)',
                },
            ),
            html.Img(src='/assets/salary.png', style={'height': '25px', 'margin-left': '30px','margin-right': '10px', 'margin-bottom': '8px'}),
            html.Div(className='content-text', children='Income Category: ',
                style={'margin-right': '10px', 'padding-bottom': '5px'}),
            dcc.Dropdown(
                id='select_income',
                options=[
                    {"label": "All", "value": "All"},
                    {"label": "Less than $40k", "value": "Less than $40k"},
                    {"label": "$40-75k", "value": "$40-75k"},
                    {"label": "$75-125k", "value": "$75-125k"},
                    {"label": "$125k or more", "value": "$125k or more"}
                ],
                multi=False,
                value="All",
                className='dash-dropdown',
                style={
                    'width': '200px', 
                    'borderRadius': '20px',
                    'fontFamily': 'DM Sans, sans-serif',
                    'fontWeight': '400',
                    'fontSize' : '19px',
                    'background-color': 'rgba(255, 255, 255, 0.6)',
                },
            )
        ]),
    html.Div(className="graph-wrapper-vertical", children=[
        html.Div( className="graph-horizontal-center", children=[
                dcc.Graph(id='bubble_chart', figure={}, style={'height': '100%'}),
            ]
        ),
        html.Div(className="graph-insight", children=[
            html.Div(className="graph-text-block", children=[
                html.Div(className="graph-text-bullet", children="\u25CF  "),
                html.Div(className="graph-text", children="The number of people who have very good perception about Union Leaders only, exceed the number of people who have good perception about both Company Leaders and Union Leaders."),
            ]),
            html.Div(className="graph-text-block", children=[
                html.Div(className="graph-text-bullet", children="\u25CF  "),
                html.Div(className="graph-text", children="The black people who have a very good perception about the Union leaders and very bad perception about the Company Leaders are significantly higher than the vice versa."),
            ]),
            html.Div(className="graph-text-block", children=[
                html.Div(className="graph-text-bullet", children="\u25CF  "),
                html.Div(className="graph-text", children="People with high school qualification and more that 75K$ salary have a very goog perception about the Company leaders."),
            ]),
        ])
    ]),

])


# Connect the Plotly graphs with Dash Components

# Define the callback for the graph
def register_callbacks(app):
    @app.callback(
        Output(component_id='bubble_chart', component_property='figure'),
        [Input(component_id='select_education', component_property='value'),
        Input(component_id='select_race', component_property='value'),
        Input(component_id='select_income', component_property='value')]
    )
    def update_graph(education, race, income):

        df_filtered_for_perception = filter_data_for_perception(df_with_known_voting_status.copy(),education, race, income)
        df_perception = prepare_dataframe_for_perception(df_filtered_for_perception)
        
        # Plotly Express
        fig_perception = create_fig_for_perception(df_perception)

        return fig_perception


# if __name__ == '__main__':
#     app.run_server(debug=True)