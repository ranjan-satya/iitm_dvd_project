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
color_map = {race: color for race, color in zip(race_dist['Race'], px.colors.qualitative.Pastel)}

# Create donut chart for race distribution with pastel colors
donut_fig_race = px.pie(race_dist, values='Count', names='Race', hole=.4,
                        title="Race Distribution", color_discrete_map=color_map)

# Create the horizontal bar chart for Systemic Racism vs. Election Relevance
grouped_data_systemic_racism = data.groupby(['How often do you vote?', 'Election Relevance']).size().reset_index(name='Count')
grouped_data_systemic_racism['Percentage'] = grouped_data_systemic_racism['Count'] / grouped_data_systemic_racism.groupby('How often do you vote?')['Count'].transform('sum') * 100

# Define a color map for 'Election Relevance'
color_map = {
    'Things will pretty much be the same': 'rgb(141,160,203)',
    'Who wins the election really matters': 'rgb(246, 207, 113)'  # Olive
}

# Create a new column for text color based on 'Election Relevance'
grouped_data_systemic_racism['Text Color'] = grouped_data_systemic_racism['Election Relevance'].apply(
    lambda x: 'white' if x == 'Things will pretty much be the same' else '#4a4a4a'
)

# Create horizontal bar chart with manual colors
horizontal_bar_chart_racism = px.bar(
    grouped_data_systemic_racism,
    x='Percentage',
    y='How often do you vote?',
    color='Election Relevance',
    title='How often do you vote? vs. Election Relevance',
    orientation='h',
    text=None,  # Set text to None to avoid default labels
    color_discrete_map=color_map  # Use the color map here
)

# Remove y-axis title for horizontal bar charts
horizontal_bar_chart_racism.update_layout(
    yaxis_title=None,
    title={
        'y': 0.95,  # Adjust the vertical position of the title
        'x': 0.5,  # Set the horizontal position to 0.5 for centering
        'xanchor': 'center',
        'yanchor': 'top'
    },
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to black
    paper_bgcolor='rgba(255, 255, 255, 0)',  # Set paper background color to black
    font=dict(color='black', family='DM Sans, sans-serif', size=16),  # Set text color to black
)

# Update text color based on the new 'Text Color' column
for index, row in grouped_data_systemic_racism.iterrows():
    if row['Election Relevance'] == 'Things will pretty much be the same':
        horizontal_bar_chart_racism.add_annotation(
            x=row['Percentage'],
            y=row['How often do you vote?'],
            text=f"{row['Percentage']:.1f}%",
            showarrow=False,
            font=dict(color=row['Text Color']),
            xanchor='right',
            xshift=-5
        )
    else:
        horizontal_bar_chart_racism.add_annotation(
            x=100,
            y=row['How often do you vote?'],
            text=f"{row['Percentage']:.1f}%",
            showarrow=False,
            font=dict(color=row['Text Color']),
            xanchor='right',
            xshift=-5
        )


# Filter out '-Confident' values from the last two columns
filtered_data = data[~data.iloc[:, -2:].apply(lambda x: x.str.contains('-Confident')).any(axis=1)]

# Define a manual color map for the races
color_map_for_pie = {
    'Confident': '#BAB0AC',
    'Not Confident': '#4C78A8',
}

# Extract the color sequence as a list
color_sequence = list(color_map_for_pie.values()) 

# Pie chart for the second-to-last column
pie_chart_1 = px.pie(filtered_data, names=filtered_data.columns[-2],
                    title=f'{filtered_data.columns[-2]} Distribution',
                    color_discrete_sequence=color_sequence)

pie_chart_1.update_layout(title={
                                'y': 0.95,  # Adjust the vertical position of the title
                                'x': 0.5,  # Set the horizontal position to 0.5 for centering
                                'xanchor': 'center',
                                'yanchor': 'top'
                            },
                        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to black
                        paper_bgcolor='rgba(255, 255, 255, 0)',  # Set paper background color to black
                        font=dict(color='black', family='DM Sans, sans-serif', size=16),  # Set text color to white
        )

# Pie chart for the last column
pie_chart_2 = px.pie(filtered_data, names=filtered_data.columns[-1],
                    title=f'{filtered_data.columns[-1]} Distribution',
                    color_discrete_sequence=color_sequence)

pie_chart_2.update_layout(title={
                                'y': 0.95,  # Adjust the vertical position of the title
                                'x': 0.5,  # Set the horizontal position to 0.5 for centering
                                'xanchor': 'center',
                                'yanchor': 'top'
                            },
                            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to black
                            paper_bgcolor='rgba(255, 255, 255, 0)',  # Set paper background color to black
                            font=dict(color='black', family='DM Sans, sans-serif', size=16),  # Set text color to white
                        )

# Create the stacked bar chart for Voting in Union Elections vs. Leadership Perception
grouped_data_voting_leadership = data.groupby(['Race', 'Leadership Perception']).size().reset_index(name='Count')
grouped_data_voting_leadership['Percentage'] = grouped_data_voting_leadership['Count'] / grouped_data_voting_leadership.groupby('Race')['Count'].transform('sum') * 100
horizontal_stacked_bar_fig = px.bar(grouped_data_voting_leadership, x='Percentage', y='Race', color='Leadership Perception',
                                    title='Race vs. Leadership Perception',
                                    orientation='h', barmode='stack', text=grouped_data_voting_leadership['Percentage'].apply(lambda x: f'{x:.1f}%'),
                                    color_discrete_sequence=px.colors.qualitative.Pastel)

# Create the horizontal bar chart for Systemic Racism vs. Election Relevance
grouped_data_systemic_racism = data.groupby(['Race', 'Election Relevance']).size().reset_index(name='Count')
grouped_data_systemic_racism['Percentage'] = grouped_data_systemic_racism['Count'] / grouped_data_systemic_racism.groupby('Race')['Count'].transform('sum') * 100
horizontal_bar_chart_racism = px.bar(grouped_data_systemic_racism, x='Percentage', y='Race', color='Election Relevance',
                                    title='Race vs. Election Relevance', orientation='h',
                                    text=grouped_data_systemic_racism['Percentage'].apply(lambda x: f'{x:.1f}%'),
                                    color_discrete_sequence=px.colors.qualitative.Pastel)

horizontal_bar_chart_racism.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to black
    paper_bgcolor='rgba(255, 255, 255, 0)',  # Set paper background color to black
    font=dict(color='black', family='DM Sans, sans-serif', size=16),  # Set text color to black
)
# # Initialize the Dash app
# app = dash.Dash(__name__)

# Layout of the dashboard
layout = html.Div([
    html.H1("Election Relevence and Mode of Voting", className='content-title'),

    # Horizontal Bar Chart: Systemic Racism vs. Election Relevance
    html.Div([
        dcc.Graph(figure=horizontal_bar_chart_racism, style={'height': '600px',
                                                            'border-radius': '20px',  # Set the border radius
                                                            'overflow': 'hidden',  # Ensure content is clipped to the border radius
                                                            'background-color': 'rgba(255, 255, 255, 0.4)',  # Set background color for better visibility
                                                            'margin-bottom': '40px',
                                                        })
    ]),


    # Pie Charts for the Last Two Columns
    # html.Div([
    #     html.Div([
    #         dcc.Graph(figure=pie_chart_1, style={'width': '100%', 'height': '330px'})
    #     ], style={'display': 'inline-block', 'width': '45%'}),
    #     html.Div([
    #         dcc.Graph(figure=pie_chart_2, style={'width': '100%', 'height': '330px'})
    #     ], style={'display': 'inline-block', 'width': '45%',})
    # ], style={'display': 'flex', 'justify-content': 'space-between'})
], style={'padding': '10px', 'font-family': 'Arial', 'overflow': 'hidden'})  # Adjust padding and prevent scrolling

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)
