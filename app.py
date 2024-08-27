import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc 
from chart1 import layout as chart1_layout, register_callbacks as register_chart1_callbacks
from chart3 import layout as chart3_layout, register_callbacks as register_chart3_callbacks
from chart2 import layout as chart2_layout
from chart4 import layout as chart4_layout, register_callbacks as register_chart4_callbacks
from dataset import layout as dataset_layout

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# Define the layout
app.layout = html.Div(className='body', children=[
    # Google Web Font Loading Script
    html.Link(
        href='https://fonts.googleapis.com/css2?family=Montserrat:wght@100;200;300;400;500;600;700;800;900&display=swap',
        rel='stylesheet'
    ),
    html.Link(
        href='https://fonts.googleapis.com/css2?family=Nunito:wght@200;300;400;500;600;700&display=swap',
        rel='stylesheet'
    ),
    
    html.Link(
        href='https://fonts.googleapis.com/css2?family=Nunito:wght@200;300;400;500;600;700&display=swap',
        rel='stylesheet'
    ),

    dcc.Location(id='_pages_location', refresh=False),  # URL management
    html.Section(className='header', children=[
        html.H1(className='heading', children='CS4001 (Data Visualization Design) Project - Team VIZard')
    ]),
    
    html.Section(className='content-wrapper', children=[
        html.Div(className='content-left', children=[
            html.Section(className='index', children=[
                html.H2(className='index-title', children='Content'),
                html.Div(className='index-item', id='link-dataset', children='- Dataset'),
                html.Div(className='index-item', id='link-chart1', children='- Voting Behavior'),
                html.Div(className='index-item', id='link-chart2', children='- Racial Dynamics'),
                html.Div(className='index-item', id='link-chart3', children='- Ease of Voting'),
                html.Div(className='index-item', id='link-chart4', children="- Leaders' Perception"),
            ]),
            # html.Section(className='team-members', children=[
            #     html.H2(className='team-title', children='Team Members'),
            #     html.Div(className='team-details', children='1. Abel (21f2000265)'),
            #     html.Div(className='team-details', children='2. Harshini (21f1005191)'),
            #     html.Div(className='team-details', children='3. John Joshi (21f1005544)'),
            #     html.Div(className='team-details', children='4. Satya (21f1005375)'),
            # ]),
            html.Section(className='credit-part', children=[
                html.Img(src='/assets/Plotly-logo.png', className='plotly-logo')
            ])
        ]),
        html.Section(id='_pages_content', className='content', children=[
            dataset_layout 
        ])
    ])
])

# Define the callback to update the content based on the selected page
@callback(
    Output('_pages_content', 'children'),
    Output('link-dataset', 'style'),
    Output('link-chart1', 'style'),
    Output('link-chart2', 'style'),
    Output('link-chart3', 'style'),
    Output('link-chart4', 'style'),
    Input('link-dataset', 'n_clicks'),
    Input('link-chart1', 'n_clicks'),
    Input('link-chart2', 'n_clicks'),
    Input('link-chart3', 'n_clicks'),
    Input('link-chart4', 'n_clicks'),
)

def display_page( dataset, chart1, chart2, chart3, chart4):
    ctx = dash.callback_context

    # Default styles for all links
    default_style = {
        'color': '#000000',
        'border-bottom': '0 #fffc',
        '-webkit-text-stroke-width': '.2px',
        'border-radius': '8px',
        'padding': '4% 2%',
        'cursor': 'pointer',
        'transition': 'all .2s'
    }

    # Active styles for the clicked link
    active_style = {
        'color': '#fff',
        '-webkit-text-stroke-width': '.4px',
        'background-color': '#00000066',
        'border-bottom': '0 #fffc',
        'border-radius': '8px',
        'padding': '4% 2%',
        'cursor': 'pointer',
        'transition': 'all .2s'
    }

    if not ctx.triggered:
        # Default to Dataset page
        return (
            html.Div([
                dataset_layout 
            ]),
            active_style,  # Active style for Dataset
            *[default_style] * 4  # Default styles for all other links
        )

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Set styles based on which link was clicked
    styles = [default_style] * 5  # Default styles for all links

    if button_id == 'link-dataset':
        styles[0] = active_style
        return html.Div([
            dataset_layout  
        ]), *styles
    elif button_id == 'link-chart1':
        styles[1] = active_style
        return html.Div([
            chart1_layout  # Call the update_graph function from graph.py
        ]), *styles
    elif button_id == 'link-chart2':
        styles[2] = active_style
        return html.Div([
            chart2_layout  # Call the update_graph function from graph.py
        ]), *styles
    elif button_id == 'link-chart3':
        styles[3] = active_style
        return html.Div([
            chart3_layout  # Call the update_graph function from graph.py
        ]), *styles
    elif button_id == 'link-chart4':
        styles[4] = active_style
        return html.Div([
            chart4_layout  # Call the update_graph function from graph.py
        ]), *styles

register_chart1_callbacks(app)  # Register the callbacks
register_chart3_callbacks(app)  # Register the callbacks
register_chart4_callbacks(app)  # Register the callbacks
if __name__ == '__main__':
    app.run_server(debug=True)