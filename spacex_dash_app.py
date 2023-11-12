# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    ],
                                    value='ALL', placeholder="Select a Launch Site:",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0,max=10000,step=1000,
                                value=[min_payload, max_payload],
                                marks={i: str(i) for i in range(0, 10001, 1000)}
                                ),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):

    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(filtered_df, values='class', 
                    names='Launch Site', 
                    title='Total Successful Launches by Site')

    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        
        if filtered_df.empty:
            fig = go.Figure()
            fig.add_annotation(text="No data available for this site",
                                xref="paper", yref="paper",
                                showarrow=False, font_size=15)

        else:
            
            fig = px.pie(filtered_df,
                        names='class', 
                        title=f'Successful Launches for Site {entered_site}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])

def get_scat_chart(entered_site, payload):

    lower_bound, upper_bound = payload

    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] > lower_bound) &
    (spacex_df['Payload Mass (kg)'] < upper_bound)]

    if entered_site == 'ALL':
        fig = px.scatter(filtered_df,
                        x=filtered_df['Payload Mass (kg)'],
                        y=filtered_df['class'],
                        color="Booster Version Category")

    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        
        if filtered_df.empty:
            fig = go.Figure()

        else:
            fig = px.scatter(filtered_df,
                x=filtered_df['Payload Mass (kg)'],
                y=filtered_df['class'],
            color="Booster Version Category")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
