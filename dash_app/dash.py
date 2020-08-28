import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from dash_app.chart_creator import ChartCreator
from data.data import Data

# Import the data set
data = Data()


def init_dashboard(server):
    """
    Create the Plotly Dash dashboard

    :rtype: Plotly app server
    """
    # Create the Plotly figures
    charts = ChartCreator(data.df)
    fig_total = charts.fig_total()
    fig_active = charts.fig_active()

    # Create a Dash app
    dash_app = dash.Dash(external_stylesheets=[dbc.themes.LUX], server=server, routes_pathname_prefix='/dashapp/')

    # Create the app layout
    # Bootstrap fluid container with 1 row and 2 columns
    dash_app.layout = dbc.Container(fluid=True, children=[
        html.Br(),
        html.H1('Global Covid-19 daily cases'),
        dbc.Row([
            # Country input and summary statistics panel
            dbc.Col(md=3, children=[
                dbc.FormGroup([
                    html.H4("Select Country"),
                    dcc.Dropdown(id="country", options=[{"label": x, "value": x} for x in data.country_list],
                                 value="World")
                ]),
                html.Br(),
                html.Div(id="output-panel")
            ]),
            # Figures in 2 tabs
            dbc.Col(md=9, children=[
                dbc.Col(html.H4("Covid cases"), width={"size": 6, "offset": 3}),
                dbc.Tabs(className="nav nav-pills", children=[
                    dbc.Tab(dcc.Graph(id="fig-total", figure=fig_total), label="Total cases"),
                    dbc.Tab(dcc.Graph(id="fig-active", figure=fig_active), label="Active cases")
                ])
            ])
        ])
    ])

    # Initialize callbacks after our app is loaded
    # Pass dash_app as a parameter
    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(dash_app):
    @dash_app.callback(Output("output-panel", "children"), [Input("country", "value")])
    def render_output_panel(country):
        data.process_data(country)
        charts = ChartCreator(data.df)
        peak_day, num_max, total_cases_until_today, active_cases_today = charts.get_stats()
        panel = html.Div([
            html.H4(country, id="card_name"),
            dbc.Card(body=True, className="bg-dark text-light", children=[
                html.Br(),
                html.H6("Total cases until today:", className="card-title"),
                html.H3("{:,.0f}".format(total_cases_until_today), className="card-text text-light"),
                html.Br(),
                html.H6("Active cases today:", className="card-title"),
                html.H3("{:,.0f}".format(active_cases_today), className="card-text text-light"),
                html.Br(),
                html.H6("Peak day:", className="card-title"),
                html.H3(peak_day.strftime("%d-%m-%Y"), className="card-text text-light"),
                html.H6("with {:,.0f} cases".format(num_max), className="card-title text-light"),
                html.Br()
            ])
        ])
        return panel

    @dash_app.callback(Output("fig-total", "figure"), [Input("country", "value")])
    def plot_total_cases(country):
        data.process_data(country)
        charts = ChartCreator(data.df)
        return charts.fig_total()

    @dash_app.callback(Output("fig-active", "figure"), [Input("country", "value")])
    def plot_active_cases(country):
        data.process_data(country)
        charts = ChartCreator(data.df)
        return charts.fig_active()
