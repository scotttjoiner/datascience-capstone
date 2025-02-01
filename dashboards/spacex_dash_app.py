# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        
        html.H1(
            'SpaceX Launch Records Dashboard', 
            style={
                'textAlign': 'center', 
                'color': '#503D36', 
                'font-size': 40
            }
        ),
                                
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id = 'site-dropdown',
            value = 'ALL',
            placeholder = 'Select Launch Site',
            searchable = True,
            options = [
                {'label': 'All Sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
            ]
        ),
        
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(
            dcc.Graph(id='success-pie-chart')
        ),
        
        html.Br(),
        html.P("Payload range (Kg):"),

        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id='payload-slider',
            min = 0,
            max = 10000,
            step = 1000,
            value = [0,10000]
        ),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(
            dcc.Graph(id='success-payload-scatter-chart')
        ),
                                
    ]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def success_chart_display(site):

    if site == 'ALL':

         return px.pie(
            spacex_df[spacex_df['class'] == 1],
            values = 'class',
            names =  'Launch Site',
            title = f'Successful Launches by Site'
        )

    else:

        data_count = spacex_df[spacex_df['Launch Site'] == site]['class'].value_counts().reset_index()
        data_count.columns = ['class', 'count']
        data_count['class'] = data_count['class'].map({0: 'Failure', 1: 'Success'})  

        return px.pie(
            data_count,
            values = 'count',
            names = 'class',
            title = f'Launches Rates for {site}'
        )


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    [
        Output(component_id='success-payload-scatter-chart', component_property='figure')
    ],
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def scatter_chart_display(site, range):
    
    data = spacex_df if site == 'ALL' else spacex_df[spacex_df['Launch Site'] == site]
    range_data = data.query(f"{range[0]} <= `Payload Mass (kg)` <= {range[1]}")
    
    return [px.scatter(
        range_data,
        x = 'Payload Mass (kg)',
        y = 'class',
        color = 'Booster Version Category',
        size='Payload Mass (kg)', 
        title = f'Correlation between Payload and Mass for Site: {site}',

        labels={'class': 'Launch Outcome', 'Payload Mass (kg)': 'Payload Mass (kg)'},
        category_orders={'class': [0, 1]},  
        size_max=20,  
        opacity=0.7,  
        template='plotly_white' 
    )]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
