import dash
from dash import dcc, html, Input, Output, clientside_callback, ClientsideFunction
import plotly.graph_objs as go
import requests
import dash_bootstrap_components as dbc
import os

from dash_controller import GraphUpdater, DashboardController, DataModel

from pages.dash_views import HomePage, Page1, Page2, GraphPage

from widgets.my_components import DragWidgetPage



class DashboardApp:
    def __init__(self):
        

        self.data_model = DataModel()
        self.controller = DashboardController(self.data_model)
        self.pages = {
            "/": HomePage(self.controller),
            "/page-1": Page1(),
            "/page-2": Page2(),
            "/graph-page": GraphPage(self.controller),
            "/drag-widget": DragWidgetPage(),
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
                        dbc.NavItem(dbc.NavLink("Drag Widget", href="/drag-widget")),
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
        self.app.title = "DASH BOARD INTERATIVO 2024"
        self.graphs = {
            "leads_mes_graph": GraphUpdater(
                "leads_mes_graph", "Leads por Mês Ano", "Mês", "Leads"
            ),
            "valor_membro_graph": GraphUpdater(
                "valor_membro_graph", "Valor Venda por Tipo Membro", "", ""
            ),
        }

        self.layout()
        self.configurar_callbacks()
        self.callbacks()

    def layout(self):
        self.app.layout = HomePage(self.controller).material_app()

    def callbacks(self):
        @self.app.callback(
            Output("leads_mes_graph", "figure"), Input("leads_mes_graph", "id")
        )
        def update_leads_mes_graph(_):
            # Supondo que `get_leads_data()` é uma função que retorna dados
            data = self.data_model.get_leads_data()
            meses = [item["mes"] for item in data]
            leads = [item["leads"] for item in data]
            return self.graphs["leads_mes_graph"].update_graph(meses, leads)

        @self.app.callback(
            Output("valor_membro_graph", "figure"), Input("valor_membro_graph", "id")
        )
        def update_valor_membro_graph(_):
            # Supondo que `get_valor_membro_data()` é uma função que retorna dados
            data = self.data_model.get_valor_membro_data()
            labels = [item["tipo_membro"] for item in data]
            values = [item["valor_venda"] for item in data]
            return self.graphs["valor_membro_graph"].update_graph(
                labels, values, graph_type="pie"
            )
        
        self.app.clientside_callback(
            ClientsideFunction(namespace="clientside", function_name="make_draggable"),
            Output("drag-container", "data-drag"),
            Input("drag-container", "id")
        )
        
    def configurar_callbacks(self):
        self.app.config.external_stylesheets.append("https://epsi95.github.io/dash-draggable-css-scipt/dragula.css")
        self.app.config.external_scripts.extend([
            "https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js",
            "https://epsi95.github.io/dash-draggable-css-scipt/script.js"
        ])

    def run(self):
        self.app.run_server(
            debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080))
        )




dashboard = DashboardApp()

app = dashboard.app
server = app.server

dashboard.run()
