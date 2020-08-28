import plotly.express as px


class ChartCreator:
    """ Creates the figures and statistics to be used in the dashboard"""

    def __init__(self, df):
        self.df = df

    @staticmethod
    def calculate_peak(df):
        data_max = df["delta_data"].max()
        peak_day = df[df["delta_data"] == data_max].index[0]
        return peak_day, data_max

    @staticmethod
    def calculate_max(df):
        total_cases_until_today = df["data"].max()
        active_cases_today = df["delta_data"].max()
        return total_cases_until_today, active_cases_today

    def get_stats(self):
        peak_day, num_max = self.calculate_peak(self.df)
        total_cases_until_today, active_cases_today = self.calculate_max(self.df)
        return peak_day, num_max, total_cases_until_today, active_cases_today

    def fig_total(self):
        fig = px.scatter(self.df,
                         x=self.df.index,
                         y=self.df["data"],
                         labels={'data': '', 'index': 'Select date range'},
                         template="simple_white"
                         )
        # add slider
        fig.update_xaxes(rangeslider_visible=True)

        # You can also create more customised range sliders using a Plotly component in app.layout.  See
        # https://www.youtube.com/watch?v=Zvz2LpziQAs

        return fig

    def fig_active(self):
        # Bar plot showing active cases
        fig = px.bar(self.df,
                     x=self.df.index,
                     y=self.df["delta_data"],
                     labels={'delta_data': '', 'index': 'Select date range'},
                     template="simple_white"
                     )
        # add slider
        fig.update_xaxes(rangeslider_visible=True)

        return fig
