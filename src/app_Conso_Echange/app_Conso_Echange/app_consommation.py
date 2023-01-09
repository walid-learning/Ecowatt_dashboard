



def conso_echange():

    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    import pandas as pd
    import numpy as np
    from dash.dependencies import Output, Input

    #-------------------------------------------------------

    data = pd.read_csv("Consommation_2016.csv")
    data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")
    data.sort_values("Date", inplace=True)


    #---------------------------------------------------
    data_echange = pd.read_csv("Echange_2016.csv")
    data_echange["Date"] = pd.to_datetime(data_echange["Date"], format="%m/%d/%Y")
    data_echange.sort_values("Date", inplace=True)

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
                                    for Type in data_echange.columns[4:]     #modifier par 3
                                ],
                                value="Ech. physiques",
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
        filtered_data_echange = data_echange.loc[mask, :]
        price_chart_figure = {
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
                    "text": "Consommation en France",
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
                    "x": filtered_data_echange["Date"],
                    "y": filtered_data_echange[type],
                    "type": "lines",
                },
            ],
            "layout": {
                "title": {"text": "Echanges avec la France", "x": 0.05, "xanchor": "left"},
                "xaxis": {"fixedrange": True},
                "yaxis": {"fixedrange": True},
                "colorway": ["#E12D39"],
            },
        }
        return price_chart_figure, volume_chart_figure
    
    app.run_server(debug=True)

if __name__ == "__main__":
    #app.run_server(debug=True)
    conso_echange()
