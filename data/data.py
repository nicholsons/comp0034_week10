import pathlib

import pandas as pd


class Data:
    """Class for retrieving and structuring the Covid global time series data of daily cases."""

    def __init__(self):
        self.cases = []  # Populated when .get_data() is called
        self.country_list = []  # Populated when .get_data() is called
        self.df = []  # Populated when .process_data(country) is called
        self.today = '' # Populated when .process_data(country) is called
        self.get_data()
        self.process_data('World')

    def get_data(self):
        DATA_PATH = pathlib.Path(__file__).parent.joinpath("CSSE_data")  # /data/CSSE_data
        self.cases = pd.read_csv(DATA_PATH.joinpath("time_series_covid19_confirmed_global.csv"))
        url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
              "/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
        # Uncomment the line below to get the latest data rather than the local csv file
        # self.cases = pd.read_csv(url)
        self.cases = self.cases.drop(['Province/State', 'Lat', 'Long'], axis=1)
        self.country_list = ["World"] + self.cases["Country/Region"].unique().tolist()

    def process_data(self, country):
        self.df = self.group_by_country(self.cases, country)
        self.df["delta_data"] = self.df["data"] - self.df["data"].shift(1)
        self.today = self.df.index[-1]

    @staticmethod
    def group_by_country(df, country):
        # Group by Country and transpose the data
        df = df.groupby("Country/Region").sum().T
        df["World"] = df.sum(axis=1)
        df = df[country]
        df.index = pd.to_datetime(df.index, infer_datetime_format=True)
        ts = pd.DataFrame(index=df.index, data=df.values, columns=["data"])
        return ts
