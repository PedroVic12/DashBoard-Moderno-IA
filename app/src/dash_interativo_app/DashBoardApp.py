import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import requests
import dash_bootstrap_components as dbc
import os

from dash_controller import GraphUpdater, DashboardController, DataModel

from pages.dash_views import HomePage, Page1, Page2, GraphPage




class DashboardApp:
    def __init__(self):
        

        self.data_model = DataModel()
        self.controller = DashboardController(self.data_model)
        self.pages = {
            "/": HomePage(self.controller),
            "/page-1": Page1(),
            "/page-2": Page2(),
            "/graph-page": GraphPage(self.controller),
        }

        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

        self.app.layout = dbc.Container(
            fluid=True,
            children=[
                dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(dbc.NavLink("Home", href="/")),
                        dbc.NavItem(dbc.NavLink("Page 1", href="/page-1")),
                        dbc.NavItem(dbc.NavLink("Page 2", href="/page-2")),
                        dbc.NavItem(dbc.NavLink("Graph Page", href="/graph-page")),
                        dbc.NavItem(dbc.NavLink("Sair", href="/logout")),
                    ],
                    brand="Interactive Data Visualization",
                    brand_href="#",
                    color="dark",
                    dark=True,
                ),
                dcc.Location(id="url", refresh=False),
                html.Div(id="page-content"),
                #!Igual flutter
                #!Ele faz componentes que rodam um main app
                #! use MVC e Componentes para construir
            ],
        )
        self.app.title = "Resumo Geral de Marketing"
        self.graphs = {
            "leads_mes_graph": GraphUpdater(
                "leads_mes_graph", "Leads por Mês Ano", "Mês", "Leads"
            ),
            "valor_membro_graph": GraphUpdater(
                "valor_membro_graph", "Valor Venda por Tipo Membro", "", ""
            ),
        }

        self.layout()
        self.callbacks()

    def layout(self):
        self.app.layout = dbc.Container(
            [
                html.H1(
                    "Resumo Geral de Marketing",
                    style={"textAlign": "center", "marginBottom": "20px"},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H2("R$ 1.74 Mi"),
                                        html.P("Gastos Marketing"),
                                    ]
                                ),
                            ),
                            md=3,
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H2("53,530"),
                                        html.P("Leads"),
                                    ]
                                ),
                            ),
                            md=3,
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H2("33,674"),
                                        html.P("Ingressantes"),
                                    ]
                                ),
                            ),
                            md=3,
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H2("R$ 4.8 Mi"),
                                        html.P("Valor Venda"),
                                    ]
                                ),
                            ),
                            md=3,
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(self.graphs["leads_mes_graph"].get_graph(), md=6),
                        dbc.Col(self.graphs["valor_membro_graph"].get_graph(), md=6),
                    ]
                ),
            ],
            fluid=True,
        )

    def callbacks(self):
        @self.app.callback(
            Output("leads_mes_graph", "figure"), Input("leads_mes_graph", "id")
        )
        def update_leads_mes_graph(_):
            # Supondo que `get_leads_data()` é uma função que retorna dados
            data = get_leads_data()
            meses = [item["mes"] for item in data]
            leads = [item["leads"] for item in data]
            return self.graphs["leads_mes_graph"].update_graph(meses, leads)

        @self.app.callback(
            Output("valor_membro_graph", "figure"), Input("valor_membro_graph", "id")
        )
        def update_valor_membro_graph(_):
            # Supondo que `get_valor_membro_data()` é uma função que retorna dados
            data = get_valor_membro_data()
            labels = [item["tipo_membro"] for item in data]
            values = [item["valor_venda"] for item in data]
            return self.graphs["valor_membro_graph"].update_graph(
                labels, values, graph_type="pie"
            )

    def run(self):
        self.app.run_server(
            debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080))
        )


def get_leads_data():
    # Função fictícia que retorna dados de leads por mês
    return [
        {"mes": "Jul-19", "leads": 8852},
        {"mes": "Ago-19", "leads": 8357},
        {"mes": "Set-19", "leads": 8657},
        {"mes": "Out-19", "leads": 11084},
        {"mes": "Nov-19", "leads": 12489},
        {"mes": "Dez-19", "leads": 996},
    ]


def get_valor_membro_data():
    # Função fictícia que retorna dados de valor de venda por tipo de membro
    return [
        {"tipo_membro": "Black", "valor_venda": 15.27},
        {"tipo_membro": "Platinum", "valor_venda": 31.35},
        {"tipo_membro": "Gold", "valor_venda": 53.26},
    ]


dashboard = DashboardApp()

app = dashboard.app
server = app.server

dashboard.run()
