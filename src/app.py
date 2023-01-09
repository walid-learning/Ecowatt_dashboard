import sys
import os
import time
sys.path.append( os.path.dirname(os.path.abspath(__file__))[:-3] + "\\cfg")
from config import PATH, info, warning, debug

# def production_emissions():


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

import webbrowser


from flask import request

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

#-------------------------------------------------------

data = pd.read_csv(PATH+"\\src\\Production_2016.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")
data.sort_values("Date", inplace=True)


#---------------------------------------------------
data_emission = pd.read_csv(PATH+"\\src\\2016_emission.csv")
data_emission["Date"] = pd.to_datetime(data_emission["Date"], format="%m/%d/%Y")
data_emission.sort_values("Date", inplace=True)

#--------------------------------

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Analyse de l'énergie : Comprendre l'énergie  !"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="ECOWATT", className="header-emoji"),
                html.H1(
                    children="Comprendre l'énergie", className="header-title"
                ),
                html.P(
                    children="Analyser la production et l'emission de l'energie",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Perimetre", className="menu-title"),
                        dcc.Dropdown(
                            id="Perimetre-filter",
                            options=[
                                {"label": Perimetre, "value": Perimetre}
                                for Perimetre in np.sort(data.Perimetre.unique())
                            ],
                            value="France",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {"label": Type, "value": Type}
                                for Type in data.columns[3:]
                            ],
                            value="Fioul",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    [Output("price-chart", "figure"), Output("volume-chart", "figure")],
    [
        Input("Perimetre-filter", "value"),
        Input("type-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(Perimetre,type, start_date, end_date):
    mask = (
        (data.Perimetre == Perimetre)
        #& (data.Heures == Heure)
        & (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    filtered_data_emission = data_emission.loc[mask, :]
    #filtered_data_emission = filtered_data_emission.groupby('Date')[["Taux de Co2"]].mean()
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data[type],
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],


        "layout": {
            "title": {
                "text": "Production en France",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data_emission["Date"],
                "y": filtered_data_emission["Taux de Co2"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Emission Co2 en France", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure
    webbrowser.open("http://127.0.0.1:8050/")

    # app.run_server(debug=True)

# @app.route('/shutdown', methods=['POST'])
# def shutdown():
#     shutdown_server()
#     return 'Server shutting down...'

if __name__ == "__main__":
    #app.run_server(debug=True)
    # data_emission = pd.read_csv("2016_emission.csv")
    # data_emission["Date"] = pd.to_datetime(data_emission["Date"], format="%m/%d/%Y")
    # data_emission.sort_values("Date", inplace=True)
    # filtered_data_emission = data_emission.groupby('Date')[["Taux de Co2"]].mean()
    # print(filtered_data_emission["Taux de Co2"].values)
    # print(data_emission["Taux de Co2"])
    app.run_server(debug=True)
    
  

