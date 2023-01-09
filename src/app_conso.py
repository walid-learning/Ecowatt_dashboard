import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import mysql.connector
from dash.dependencies import Output, Input
import sys
import os
sys.path.append( os.path.dirname(os.path.abspath(__file__))[:-3] + "\\cfg")
from config import PATH, info, warning, debug, log_config

log_config('app_conso')



#---------------Connexion base de donnée -----------------
mydb = mysql.connector.connect(
host="localhost",
user="root",
database = "ecowatt",
password="Walidluxe99."
)

info('Connexion à la DB OK')

# --------------------------------- Consommation --------------------------------------------#

data = pd.read_sql("""SELECT consommation.Perimetre,CONCAT(SUBSTR(consommation.Date,4,2), "/" ,SUBSTR(consommation.Date,1,2), "/" ,SUBSTR(consommation.Date,7)) as Date, 
                        AVG(Consommation) as Consommation
                        FROM consommation inner join echanges on 
                        (consommation.Perimetre = echanges.Territoire and consommation.Date = echanges.Date
                        and consommation.Heures = echanges.Heures)
                        Group by Date
                        HAVING SUBSTR(Date,7) = 2016
                        ORDER BY Date    ;""", mydb)

data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")
info('Requête SQL de séléction')


# ----------------------------------- Echange --------------------------------------------#


data_echange = pd.read_sql("""SELECT Territoire,CONCAT(SUBSTR(Date,4,2), "/" ,SUBSTR(Date,1,2), "/" ,SUBSTR(Date,7)) as Date, AVG(Echanges) as Tous,
                             AVG(Echanges_avec_le__Royaume_Uni) as Angleterre, AVG(Echanges_avec__l_Espagne) as Espagne, AVG(Echanges_avec_l_Italie) as Italie, 
                             AVG(Echanges_avec_la__Suisse) as Suisse, AVG(Echanges_avec__l_Allemagne_et_la__Belgique) as 'Allemagne et Belgique'
                            FROM echanges
                            Group by Date
                            HAVING SUBSTR(Date,7) = 2016
                            ORDER BY Date    ;""", mydb)

data_echange["Date"] = pd.to_datetime(data_echange["Date"], format="%m/%d/%Y")
info('Requête SQL select - order by')


# ----------------------------------- Interface --------------------------------------------#
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
info('lancement du serveur Dash')

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="ECOWATT", className="header-emoji"),
                html.H1(
                    children="Comprendre l'énergie", className="header-title"
                ),
                html.P(
                    children="Analyse de la consommation et les échanges de l'energie",
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
                        html.Div(children="Echange avec :", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {"label": Type, "value": Type}
                                for Type in data_echange.columns[2:]     #modifier par 3
                            ],
                            value="Tous",
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
    [Output("volume-chart", "figure"), Output("price-chart", "figure")],
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
    filtered_data_echange = data_echange.loc[mask, :]
    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Consommation"],
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Consommation en MW en France",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    price_chart_figure = {
        "data": [
            {
                "x": filtered_data_echange["Date"],
                "y": filtered_data_echange[type],
                "type": "bar",
            },
        ],
        "layout": {
            "title": {"text": "Echanges en GWh avec la France", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return volume_chart_figure , price_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
    
