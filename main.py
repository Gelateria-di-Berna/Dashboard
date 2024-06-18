import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
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

def update_output(selected_locations, start_date: str|datetime, end_date: str|datetime):
    graphs = []
    # Filter for time range
    df_date_filtered = dashboard.filter_date(start_date, end_date)
    # Getting data for each location
    for location in selected_locations:
        # Filter data for location
        df_location_filtered = dashboard.filter_location(selected_locations, df_date_filtered)
        # Group
        df_grouped = dashboard.group_by_hour(df_location_filtered)
        _x = df_grouped.index.tolist()
        _y = df_grouped.tolist()

        graphs.append(dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=_x,
                        y=_y,
                        name='Umsatz in CHF',
                        marker_color='rgba(251, 231, 239, 1)',
                        text=_y,
                        textposition='auto',
                    )
                ],
                layout=go.Layout(
                    title=f'{location} ({start_date} bis {end_date})',
                    xaxis=dict(title='Uhrzeit', showgrid=False),
                    yaxis=dict(title='Umsatz in CHF', showgrid=False),
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
