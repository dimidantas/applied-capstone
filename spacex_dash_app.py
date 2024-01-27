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
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                id='site-dropdown',
                                options=[
                                {'label': 'All Sites', 'value': 'ALL'},
        # Assuming spacex_df is your DataFrame and it contains a column with launch site names
        # Add an option for each launch site in the DataFrame
                                * [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]
                                    ],
                                value='ALL',
                                placeholder="Select a Launch Site here",
                                searchable=True
),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                id='payload-slider',
                                min=0,            # Slider starting point at 0 kg
                                max=10000,        # Slider ending point at 10000 kg
                                step=1000,        # Slider interval set at 1000 kg
                                value=[min_payload, max_payload],  # Current selected range from min_payload to max_payload
                                marks={i: '{} Kg'.format(i) for i in range(0, 10001, 1000)}  # Optional: to add marks at each step
),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_graph(selected_site):
    if selected_site == 'ALL':
        # Use all rows in the DataFrame to create a pie chart for total success launches
        fig = px.pie(spacex_df, values='class', names='Launch Site', 
                     title='Total Success Launches by Site')
    else:
        # Filter DataFrame for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Create a pie chart for success and failed counts for the selected site
        fig = px.pie(filtered_df, names='class', 
                     title=f'Success and Failed Counts for {selected_site}')

    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Callback function
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter(selected_site, payload_range):
    # Filter based on payload range
    df_filtered = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_range[0], payload_range[1])]

    if selected_site == 'ALL':
        # Use all sites
        fig = px.scatter(df_filtered, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title='Payload vs. Outcome for All Sites')
    else:
        # Filter for the selected site
        df_site_filtered = df_filtered[df_filtered['Launch Site'] == selected_site]
        fig = px.scatter(df_site_filtered, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title=f'Payload vs. Outcome for {selected_site}')

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
