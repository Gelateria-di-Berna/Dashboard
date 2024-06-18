import pandas as pd
from datetime import datetime
from .data_loaders import hello_tess_loader as htl
from .data_loaders import abacus_loader as abal


class Dashboard():
    def __init__(self) -> None:
        self.df_ht: pd.DataFrame = htl.get_hello_tess_df()
        self.locations = self.df_ht["location"].unique()

        self.df_aba: pd.DataFrame = abal.get_abacus_df()
        
    def filter_location(self, locations: list[str], df: pd.DataFrame = None) -> pd.DataFrame:
        if not locations:
            raise ValueError("Locations list is empty. Please provide valid locations.")

        if not all(isinstance(location, str) for location in locations):
            raise TypeError("All elements in `locations` list must be strings.")

        if df is None:
            df = self.df_ht

        df_filtered: pd.DataFrame = df.loc[df["location"].isin(locations)]
        return df_filtered
    
    def filter_date(self, start_date: str | datetime, end_date: str | datetime, df: pd.DataFrame = None) -> pd.DataFrame:
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
        if 'date' not in df.columns or not pd.api.types.is_datetime64_any_dtype(df['date']):
            raise ValueError('DataFrame must contain a datetime column named date.')
    
        if 'price' not in df.columns or not pd.api.types.is_numeric_dtype(df['price']):
            raise ValueError('DataFrame must contain a numeric column named price.')
    
        df_grouped: pd.DataFrame = df.groupby(df["date"].dt.hour)["price"].mean().round(2)
        return df_grouped
