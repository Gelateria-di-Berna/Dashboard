import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import requests

np.random.seed(0)

# Placeholder for API keys
HELLOTESS_API_KEY = 'your_hellotess_api_key'
ABACUS_API_KEY = 'your_abacus_api_key'

# Function to get "Umsatz pro Stunde pro Standort" from HelloTess API
def get_hello_tess_data():
    #TODO implement
    # Placeholder for the actual HelloTess API request
    pass

# Function to get data from Abacus API
def get_abacus_data():
    # Placeholder for the actual Abacus API request
    #TODO implement
    pass

# Function to generate sample data for a given date range
def generate_sample_data(locations, hours):
    data = {}
    for location in locations:
        # Create a DataFrame for each location with random data
        df = pd.DataFrame({
            'Umsatz in CHF pro MA Arbeitsstunde': np.random.randint(50, 350, size=len(hours)),
            'Arbeitsstunden pro Standort pro Stundenblock': np.random.randint(1, 10, size=len(hours)),
            'Arbeitsstunden Produktion pro Tag': np.random.randint(10, 100, size=len(hours)),
            'Anz. produzierter Kübel pro Tag': np.random.randint(0, 50, size=len(hours))
        }, index=hours)
        data[location] = df
    return data

hours = [f"{hour}:00" for hour in range(12, 24)]
locations = [
    'GdB Mattenhof (BE)',
    'GdB Brupbacherplatz (ZH)',
    "GdB Breitenrain (BE)",
    "GdB Gerolds Garten (ZH)",
    "GdB Kleinbasel ()", #TODO add missing canton
    "GdB Langgasse (BE)",
    "GdB Marzili (BE)",
    "GdB Mattenhof (BE)",
    "Roschibachplatz ()", #TODO add missing canton
    "Zollstrasse (ZH)"
    ]

#TODO remove this once data loading has been implemented
data = generate_sample_data(locations, hours)

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Define the app layout with improved styling
app.layout = html.Div(children=[
    html.Div([
        html.H1('GdB Laboratorio Cockpit', style={'textAlign': 'center'}),
        html.Div([
            html.Div([
                html.Label('Wählen Sie Standorte:', style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='location-dropdown',
                    options=[{'label': location, 'value': location} for location in locations],
                    value=[locations[0]],  # default value
                    multi=True  # allow multiple selections
                ),
                html.Label('Wählen Sie das Datum/die Woche:', style={'fontWeight': 'bold', 'marginTop': '20px'}),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=datetime.now().date() - timedelta(days=7),
                    end_date=datetime.now().date(),
                    display_format='DD.MM.YYYY',
                    style={'marginTop': '10px'}
                ),
            ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingRight': '20px'}),
            
            html.Div(id='output-container', style={'width': '70%', 'display': 'inline-block'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between'}),
    ], style={'padding': '30px', 'border': '1px solid #ddd', 'borderRadius': '5px', 'marginTop': '20px', 'background': '#f9f9f9'}),
], style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'})

@app.callback(
    Output('output-container', 'children'),
    [Input('location-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)

def update_output(selected_locations, start_date, end_date):
    graphs = []
    # Getting data for each location
    for location in selected_locations:
        # Call the API functions to get data
        hello_tess_data = get_hello_tess_data()
        abacus_data = get_abacus_data()
        location_data = data[location]
        
        graphs.append(dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=hours,
                        y=location_data['Umsatz in CHF pro MA Arbeitsstunde'],
                        name=f'Umsatz in CHF pro MA Arbeitsstunde',
                        marker_color='rgba(251, 231, 239, 1)',
                        text=location_data['Umsatz in CHF pro MA Arbeitsstunde'],
                        textposition='auto',
                    )
                ],
                layout=go.Layout(
                    title=f'{location} ({start_date} bis {end_date})',
                    xaxis=dict(title='Uhrzeit', showgrid=False),
                    yaxis=dict(title='Umsatz in CHF pro MA Arbeitsstunde', showgrid=False),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=40, r=40, t=40, b=40),
                )
            ),
            style={'height': 300}
        ))
    return graphs

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
