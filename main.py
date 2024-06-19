import dash
from dash import dcc, html, Input, Output
from datetime import datetime
from src.dashboard import Dashboard

dashboard = Dashboard()

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
                    options=[{'label': location, 'value': location} for location in dashboard.locations],
                    value=[dashboard.locations[0]],  # default value
                    multi=True  # allow multiple selections
                ),
                html.Label('Wählen Sie das Datum/die Woche:', style={'fontWeight': 'bold', 'marginTop': '20px'}),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=datetime.strptime("01.04.2020", "%d.%m.%Y").date(),
                    end_date=datetime.strptime("30.04.2020", "%d.%m.%Y").date(),
                    #start_date=datetime.now().date() - timedelta(days=7),
                    #end_date=datetime.now().date(),
                    display_format='DD.MM.YYYY',
                    style={'marginTop': '10px'}
                ),
            ], style={'width': '100%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingRight': '20px'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        html.Div(id='output-container', style={'width': '100%', 'display': 'inline-block'}),
    ], style={'padding': '30px', 'border': '1px solid #ddd', 'borderRadius': '5px', 'marginTop': '20px', 'background': '#f9f9f9'}),
], style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'})

@app.callback(
    Output('output-container', 'children'),
    [Input('location-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)

def update_output(selected_locations, start_date: str|datetime, end_date: str|datetime) -> list[dcc.Graph]:
    return dashboard.get_bar_graphs(selected_locations, start_date, end_date)

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
