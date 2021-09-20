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


app = dash.Dash(__name__)
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(
                                     id='site-dropdown',
                                     options=[
                                          {'label': 'All Sites', 'value': 'All Sites'},
                                          {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                          {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                          {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                          {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                     value='All Sites',
                                     placeholder="Select launch site",
                                     searchable=True                         
                                ),  
                                html.Br(),


                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0:'0', 2500:'2500', 5000:'5000', 7500:'7500', 10000:'10000'},
                                    value=[min_payload, max_payload]
                                ),

              
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
             Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    pie_alldata = filtered_df.groupby(['Launch Site'])['class'].count().reset_index()
    if entered_site == "All Sites":
        fig = px.pie(pie_alldata, values="class", names="Launch Site", title='Total Success Launches by Site')
        return fig
    else:   
        features = spacex_df[['Launch Site', 'class']]
        pie_site = features.loc[features['Launch Site'] == entered_site]
        pie_site_count = pie_site.groupby(['class'])['Launch Site'].count().reset_index()
        pie_site_count.rename(columns={'Launch Site':'Count'}, inplace=True)
        fig = px.pie(pie_site_count, values="Count", names="class", title='Total Success Launches for site '+entered_site) 
        return fig


    
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
             [Input(component_id='site-dropdown', component_property='value'),
             Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site, payload_slider_range):
    filtered_df = spacex_df
    low, high = payload_slider_range
    mask = ((filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high))
    if entered_site == "All Sites":
        fig = px.scatter(filtered_df[mask], x="Payload Mass (kg)", y="class", color="Booster Version Category", 
                         title='Correlation between Payload and Success for all sites')
        return fig
    else:   
        scatter_site_df = filtered_df.loc[features['Launch Site'] == entered_site]
        fig = px.scatter(scatter_site_df, x="Payload Mass (kg)", y="class", color="Booster Version Category", 
                         title='Correlation between Payload and Success for site '+entered_site) 
        return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
