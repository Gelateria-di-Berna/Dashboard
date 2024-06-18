import pandas as pd
from datetime import datetime
from .data_loaders import hello_tess_loader as htl
from .data_loaders import abacus_loader as abal

from dash import dcc
import plotly.graph_objs as go

class Dashboard():
    """
    Class representing a Dashboard for data analysis and visualization.

    Attributes:
        df_ht (pd.DataFrame): DataFrame containing data loaded from hello_tess_loader.
        locations (numpy.ndarray): Array of unique locations from df_ht.
        df_aba (pd.DataFrame): DataFrame containing data loaded from abacus_loader.

    Methods:
        filter_location(locations: list[str], df: pd.DataFrame = None) -> pd.DataFrame:
            Filter the DataFrame by the provided list of locations.

        filter_date(start_date: str | datetime, end_date: str | datetime, df: pd.DataFrame = None) -> pd.DataFrame:
            Filter the DataFrame by the provided start and end dates.

        group_by_hour(df: pd.DataFrame) -> tuple[list[int], pd.Series]:
            Group the DataFrame by hour and calculate the mean price for each hour.
    """
    def __init__(self) -> None:
        """
        Initialize a Dashboard object by loading data from hello_tess_loader and abacus_loader.
        Sets the attribute df_ht to the DataFrame obtained from hello_tess_loader.
        Sets the attribute locations to an array of unique locations from df_ht.
        Sets the attribute df_aba to the DataFrame obtained from abacus_loader.
        """
        self.df_ht: pd.DataFrame = htl.get_hello_tess_invoice_df()
        self.locations = self.df_ht["location"].unique()

        self.df_aba: pd.DataFrame = abal.get_abacus_df()
        
    def filter_location(self, locations: list[str], df: pd.DataFrame = None) -> pd.DataFrame:
        """
        Filter the DataFrame by the provided list of locations.

        Parameters:
        - locations (list[str]): List of locations to filter the DataFrame by.
        - df (pd.DataFrame, optional): DataFrame to filter. If not provided, the DataFrame loaded from hello_tess_loader will be used.

        Returns:
        - pd.DataFrame: Filtered DataFrame containing only the rows with locations present in the provided list.

        Raises:
        - ValueError: If the locations list is empty.
        - TypeError: If any element in the locations list is not a string.
        """
        if not locations:
            raise ValueError("Locations list is empty. Please provide valid locations.")

        if not all(isinstance(location, str) for location in locations):
            raise TypeError("All elements in `locations` list must be strings.")

        if df is None:
            df = self.df_ht

        df_filtered: pd.DataFrame = df.loc[df["location"].isin(locations)]
        return df_filtered
    
    def filter_date(self, start_date: str | datetime, end_date: str | datetime, df: pd.DataFrame = None) -> pd.DataFrame:
        """
        Filter the DataFrame by the provided start and end dates.

        Parameters:
        - start_date (str | datetime): The start date to filter the DataFrame by.
        - end_date (str | datetime): The end date to filter the DataFrame by.
        - df (pd.DataFrame, optional): DataFrame to filter. If not provided, the DataFrame loaded from hello_tess_loader will be used.

        Returns:
        - pd.DataFrame: Filtered DataFrame containing only the rows with dates between start_date and end_date.

        Raises:
        - ValueError: If start_date is after end_date.
        - ValueError: If the DataFrame does not contain a datetime column named 'date'.
        """
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        elif not isinstance(start_date, datetime):
            raise ValueError(f"Start Date needs to be of type string or datetime: {start_date}, {type(start_date)}.")
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
        elif not isinstance(end_date, datetime):
            raise ValueError(f"End Date needs to be of type string or datetime: {end_date}, {type(end_date)}.")

        if df is None:
            df = self.df_ht

        if start_date > end_date:
            raise ValueError("Start date cannot be after end date.")

        start_date = start_date.date()
        end_date = end_date.date()

        df_filtered: pd.DataFrame = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)]
        return df_filtered
    
    def group_by_hour(self, df: pd.DataFrame) -> tuple[list[int], pd.Series]:
        """
        Group the DataFrame by hour and calculate the mean price for each hour.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the data to be grouped.

        Returns:
        - tuple[list[int], pd.Series]: A tuple containing a list of hours and a Series with the mean price for each hour.

        Raises:
        - ValueError: If the DataFrame does not contain a datetime column named 'date'.
        - ValueError: If the DataFrame does not contain a numeric column named 'price'.
        """
        if 'date' not in df.columns or not pd.api.types.is_datetime64_any_dtype(df['date']):
            raise ValueError('DataFrame must contain a datetime column named date.')
    
        if 'price' not in df.columns or not pd.api.types.is_numeric_dtype(df['price']):
            raise ValueError('DataFrame must contain a numeric column named price.')
    
        df_grouped: pd.DataFrame = df.groupby(df["date"].dt.hour)["price"].mean().round(2)
        return df_grouped

    def get_bar_graphs(self, selected_locations, start_date: str|datetime, end_date: str|datetime) -> list[dcc.Graph]:
        graphs = []
        # Filter for time range
        df_date_filtered = self.filter_date(start_date, end_date)
        # Getting data for each location
        for location in selected_locations:
            # Filter data for location
            df_location_filtered = self.filter_location(selected_locations, df_date_filtered)
            # Group
            df_grouped = self.group_by_hour(df_location_filtered)
            _x = df_grouped.index.tolist()
            _y = df_grouped.tolist()

            graphs.append(dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=_x,
                            y=_y,
                            name='Durchschnittlicher Umsatz in CHF',
                            marker_color='rgba(251, 231, 239, 1)',
                            text=_y,
                            textposition='auto',
                        )
                    ],
                    layout=go.Layout(
                        title=f'{location} ({start_date} bis {end_date})',
                        xaxis=dict(title='Uhrzeit', showgrid=False),
                        yaxis=dict(title='Durchschnittlicher Umsatz in CHF', showgrid=False),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=40, r=40, t=40, b=40),
                    )
                ),
                style={'height': 300}
            ))

        return graphs