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

def preprocess_data_for_ease_of_voting(df_with_known_voting_status):
    unknown_q2_1_index_list = df_with_known_voting_status[(df_with_known_voting_status['Q2_1']==-1)].index.tolist()
    unknown_q14_index_list = df_with_known_voting_status[(df_with_known_voting_status['Q14']==-1)].index.tolist()

    df_with_known_voting_status_q2_o1_q14 = df_with_known_voting_status.drop(list(set(unknown_q2_1_index_list+unknown_q14_index_list)))
    return df_with_known_voting_status_q2_o1_q14

def filter_data_for_ease_of_voting(df_with_known_voting_status_q2_o1_q14, importance):
    df_filtered_for_ease_of_voting = df_with_known_voting_status_q2_o1_q14[df_with_known_voting_status_q2_o1_q14['Q2_1'] == importance]
    return df_filtered_for_ease_of_voting

def prepare_dataframe_for_ease_of_voting(df_filtered_for_ease_of_voting):
    df_ease_of_voting_ce_columns = ['Election for Congress in 2009','Election for Congress in 2011','Election for Congress in 2014']
    df_ease_of_voting_ce_rows= ['Very difficult','Somewhat difficult','Somewhat easy','Very easy']
    df_ease_of_voting_ce = pd.DataFrame(columns=df_ease_of_voting_ce_columns)
    df_ease_of_voting_ce = df_ease_of_voting_ce.reindex(df_ease_of_voting_ce_rows) 
    df_ease_of_voting_ce.index.name = 'Ease of Voting'
    df_ease_of_voting_ce.columns.name = 'Election'

    for eov_r in range(len(df_ease_of_voting_ce_rows)):
        for eov_c in range(len(df_ease_of_voting_ce_columns)):
            count = df_filtered_for_ease_of_voting[(df_filtered_for_ease_of_voting['Q14']==len(df_ease_of_voting_ce_rows)-eov_r) & (df_filtered_for_ease_of_voting['Q25_'+str((2*len(df_ease_of_voting_ce_columns))-(2*eov_c)-1)]==1)].shape[0]
            df_ease_of_voting_ce.loc[df_ease_of_voting_ce_rows[eov_r], df_ease_of_voting_ce_columns[eov_c]] = count

    df_ease_of_voting_pe_columns = ['Presidential election in 2008','Presidential election in 2010','Presidential election in 2012']
    df_ease_of_voting_pe_rows= ['Very difficult','Somewhat difficult','Somewhat easy','Very easy']
    df_ease_of_voting_pe = pd.DataFrame(columns=df_ease_of_voting_pe_columns)
    df_ease_of_voting_pe = df_ease_of_voting_pe.reindex(df_ease_of_voting_pe_rows) 
    df_ease_of_voting_pe.index.name = 'Ease of Voting'
    df_ease_of_voting_pe.columns.name = 'Election'

    for eov_r in range(len(df_ease_of_voting_pe_rows)):
        for eov_c in range(len(df_ease_of_voting_pe_columns)):
            count = df_filtered_for_ease_of_voting[(df_filtered_for_ease_of_voting['Q14']==len(df_ease_of_voting_pe_rows)-eov_r) & (df_filtered_for_ease_of_voting['Q25_'+str((2*len(df_ease_of_voting_pe_columns))-(2*eov_c))]==1)].shape[0]
            df_ease_of_voting_pe.loc[df_ease_of_voting_pe_rows[eov_r], df_ease_of_voting_pe_columns[eov_c]] = count
    
    return df_ease_of_voting_ce, df_ease_of_voting_pe

def create_fig_for_ease_of_voting(df_ease_of_voting_ce, df_ease_of_voting_pe):
    # Create figures with the 'Peach' color scale
    fig_eov_ce = px.imshow(df_ease_of_voting_ce, color_continuous_scale='Peach')
    fig_eov_pe = px.imshow(df_ease_of_voting_pe, color_continuous_scale='Peach')

    # Create a subplot with 1 row and 2 columns
    fig_eov = make_subplots(rows=2, cols=1, subplot_titles=("Congress Elections", "Presidential Elections"))

    # Calculate the minimum and maximum values across both datasets
    combined_data = np.concatenate((df_ease_of_voting_ce.values.flatten(), df_ease_of_voting_pe.values.flatten()))
    zmin = np.min(combined_data)
    zmax = np.max(combined_data)

    # Add traces for Congress Elections
    for trace in fig_eov_ce.data:
        fig_eov.add_trace(
            go.Heatmap(
                z=trace.z,
                x=trace.x,
                y=trace.y,
                colorscale='Peach',
                colorbar=dict(
                    title=trace.colorbar.title,
                    tickvals=[zmin, int(zmin + (1*(zmax-zmin))/5),  int(zmin + (2*(zmax-zmin))/5),  int(zmin + (3*(zmax-zmin))/5),  int(zmin + (4*(zmax-zmin))/5),   zmax],  # Set custom tick values
                    ticktext=[str(zmin), str(int(zmin + (1*(zmax-zmin))/5)), str(int(zmin + (2*(zmax-zmin))/5)),str(int(zmin + (3*(zmax-zmin))/5)),str(int(zmin + (4*(zmax-zmin))/5)), str(zmax)]  # Set custom tick labels
                ),
                zmin=zmin,  # Set the minimum value for the color scale
                zmax=zmax,  # Set the maximum value for the color scale
                showscale=True,
                hovertemplate='X: %{x}<br>Y: %{y}<br>Value: %{z}<extra></extra>'  # Customize hover template
            ),
            row=1, col=1
        )

    # Add traces for Presidential Elections
    for trace in fig_eov_pe.data:
        fig_eov.add_trace(
            go.Heatmap(
                z=trace.z,
                x=trace.x,
                y=trace.y,
                colorscale='Peach',
                colorbar=dict(
                    title=trace.colorbar.title,
                    tickvals=[zmin, int(zmin + (1*(zmax-zmin))/5),  int(zmin + (2*(zmax-zmin))/5),  int(zmin + (3*(zmax-zmin))/5),  int(zmin + (4*(zmax-zmin))/5),   zmax],  # Set custom tick values
                    ticktext=[str(zmin), str(int(zmin + (1*(zmax-zmin))/5)), str(int(zmin + (2*(zmax-zmin))/5)),str(int(zmin + (3*(zmax-zmin))/5)),str(int(zmin + (4*(zmax-zmin))/5)), str(zmax)]  # Set custom tick labels
                ),
                zmin=zmin,  # Set the minimum value for the color scale
                zmax=zmax,  # Set the maximum value for the color scale
                showscale=True,
                hovertemplate='X: %{x}<br>Y: %{y}<br>Value: %{z}<extra></extra>'  # Customize hover template
            ),
            row=2, col=1
        )

    # Update layout for the figure
    fig_eov.update_layout(height=600, width=800, 
                        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to black
                        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to black
                        font=dict(color='white', family='Montserrat, sans-serif')  # Set text color to white
                    )
    return fig_eov

# Preprocessing
#-------------------------------------------------------------------------------
df_preprocessed_for_ease_of_voting = preprocess_data_for_ease_of_voting(df_with_known_voting_status.copy())


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
layout = html.Div([
    html.H1("Correlation of Voter Turnout with Ease of Voting", className='content-title'),

    html.Div(className='dropdown-wrapper', children=[
        html.P(className='content-text', children='To be a good member of employee community, Voting in Union Elections is',
            style={'margin-right': '10px'}),
        dcc.Dropdown(
            id='select_importance',
            options=[
                {'label': 'Very Important', 'value': 1},
                {'label': 'Somewhat Important', 'value': 2},
                {'label': 'Not so Important', 'value': 3},
                {'label': 'Not at all Important', 'value': 4}
            ],
            value=1,
            className='dash-dropdown',
            style={
                'width': '250px', 
                'borderRadius': '20px',
                'fontFamily': 'Montserrat',
                'background-color': 'rgba(255, 255, 255, 0.6)',
            },
        )
    ]),
    html.Div(className="graph-wrapper-horizontal", children=[
        dcc.Graph(id='heatmap', figure={}, style={'height': '100%'}),
        html.Div(className="graph-insight", children=[
            html.Div(className="graph-text-block", children="\u25CF  Inshight 1"),
            html.Div(className="graph-text-block", children="\u25CF  Inshight 1"),
            html.Div(className="graph-text-block", children="\u25CF  Inshight 1")
        ])
    ]),


])


# Connect the Plotly graphs with Dash Components

# Define the callback for the graph
def register_callbacks(app):
    @app.callback(
        Output(component_id='heatmap', component_property='figure'),
        [Input(component_id='select_importance', component_property='value')]
    )
    def update_graph(importance):

        df_filtered_for_ease_of_voting = filter_data_for_ease_of_voting(df_preprocessed_for_ease_of_voting, importance)
        df_ease_of_voting_ce, df_ease_of_voting_pe = prepare_dataframe_for_ease_of_voting(df_filtered_for_ease_of_voting)

        # Plotly Express
        fig_eov = create_fig_for_ease_of_voting(df_ease_of_voting_ce, df_ease_of_voting_pe)

        return fig_eov


if __name__ == '__main__':
    app.run_server(debug=True)