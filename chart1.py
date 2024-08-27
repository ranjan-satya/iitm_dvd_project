import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load the dataset
data = pd.read_excel('Preprocessed Data.xlsx')

# Rename columns for easier handling
data = data.rename(columns={
    'Do company leadership care about its workers?': 'Leadership Perception',
    'Racial sensitivity is important.': 'Racial Sensitivity',
    'Does who win the election really matter?': 'Election Relevance',
    'Most eligible members don’t vote in every union elections. In general, which of the following categories do you think best describes you?': 'Voting Category',
    'Voter_category': 'How often do you vote?'
})

# Prepare data for race distribution
race_dist = data['Race'].value_counts().reset_index(name='Count')
race_dist = race_dist.rename(columns={'index': 'Race'})

# Create a color map for the races using pastel colors
# color_map = {race: color for race, color in zip(race_dist['Race'], px.colors.qualitative.Pastel)}

# Define a manual color map for the races
color_map = {
    'White': 'rgb(141,160,203)',
    'Black': 'rgb(141,211,199)',
    'Hispanic': '#FF9DA6',
    'Mixed': '#F7E1A0'
}

# Create donut chart for race distribution with pastel colors
donut_fig_race = px.pie(race_dist, values='Count', names='Race', hole=.4,
                        title="Race Distribution", color='Race' ,color_discrete_map=color_map)

donut_fig_race.update_layout(
    title={
        'y': 0.95,  # Adjust the vertical position of the title
        'x': 0.5,  # Set the horizontal position to 0.5 for centering
        'xanchor': 'center',
        'yanchor': 'top'
    },
    plot_bgcolor='rgba(255, 255, 255, 0)',  # Set plot background color to black
    paper_bgcolor='rgba(255, 255, 255, 0)',  # Set paper background color to black
    font=dict(color='black', family='DM Sans, sans-serif', size=16),  # Set text color to white
)
donut_fig_race.update_annotations(font=dict(size=25))

# Prepare data for voting behavior distribution by race
def create_voting_behavior_chart(selected_race=None):
    if selected_race:
        filtered_data = data[data['Race'] == selected_race]
        color = color_map[selected_race]
    else:
        filtered_data = data
        color = '#bfbfbf'  # Default color if no race is selected

    voting_behavior_dist = filtered_data['Voting Category'].value_counts().reset_index(name='Count')
    voting_behavior_dist = voting_behavior_dist.rename(columns={'index': 'Voting Category'})

    # Calculate percentages
    total_count = voting_behavior_dist['Count'].sum()
    voting_behavior_dist['Percentage'] = (voting_behavior_dist['Count'] / total_count) * 100

    voting_behavior_fig = px.bar(
        voting_behavior_dist,
        x='Count',
        y='Voting Category',
        orientation='h',
        title=f'Voting Behavior{" for " + selected_race if selected_race else ""}',
        text=voting_behavior_dist['Percentage'].apply(lambda x: f"{int(x)}%"), 
        color_discrete_sequence=[color]
    )

    voting_behavior_fig.update_layout(
        title={
            'y': 0.95,  # Adjust the vertical position of the title
            'x': 0.5,  # Set the horizontal position to 0.5 for centering
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis=dict(
            zerolinecolor='rgba(101, 101, 101, 0.4)',  # Set the zero line color
            anchor='y',  # Anchor to y-axis
            gridcolor='rgba(178, 178, 178, 0.4)',  # Set the grid line color to grey
        ),
        yaxis=dict(
            anchor='x',  # Anchor to x-axis
            gridcolor='rgba(178, 178, 178, 0.4)',  # Set the grid line color to grey
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to black
        paper_bgcolor='rgba(255, 255, 255, 0)',  # Set paper background color to black
        font=dict(color='black', family='DM Sans, sans-serif', size=16),  # Set text color to black
    )
    voting_behavior_fig.update_annotations(font=dict(size=25))
    return voting_behavior_fig
# # Initialize the Dash app
# app = dash.Dash(__name__)

# Layout of the dashboard
layout = html.Div([
    html.H1("Race and Voting Behavior" , className='content-title'),

    # Donut Chart for Race Distribution and Dynamic Bar Chart for Voting Behavior
    html.Div([
        html.Div([
            dcc.Graph(id='donut-chart', figure=donut_fig_race, style={'width': '100%', 'height': '100%'})  # Increased height
        ], style={'display': 'inline-block', 
                'width': '33%', 
                'height': '600px',
                'margin-right':'7%', 
                'border-radius': '20px',  # Set the border radius
                'overflow': 'hidden',  # Ensure content is clipped to the border radius
                'background-color': 'rgba(255, 255, 255, 0.4)',  # Set background color for better visibility
                }),
        html.Div([
            dcc.Graph(id='voting-behavior-chart', style={'width': '100%', 'height': '600px'})  # Matched height with donut chart
        ], style={'display': 'inline-block', 'width': '60%'})
    ], style={'display': 'flex', 'justify-content': 'center'}),
], style={'padding': '10px', 'font-family': 'Arial', 'overflow': 'hidden'})  # Adjust padding and prevent scrolling

# Callback to update the bar chart based on donut chart selection
def register_callbacks(app):
    @app.callback(
        Output('voting-behavior-chart', 'figure'),
        Input('donut-chart', 'clickData')
    )
    def update_voting_behavior_chart(click_data):
        if click_data:
            selected_race = click_data['points'][0]['label']
            return create_voting_behavior_chart(selected_race)
        else:
            return create_voting_behavior_chart()

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)
