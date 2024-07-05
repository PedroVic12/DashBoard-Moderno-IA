# app.py
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


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

        @self.app.callback(
            Output("page-content", "children"), [Input("url", "pathname")]
        )
        def display_page(pathname):
            if pathname in self.pages:
                return self.pages[pathname].render()
            else:
                return "404 - Page not found"

        @self.app.callback(
            Output("data-table", "children"),
            [Input("upload-data", "contents"), Input("upload-data", "filename")],
        )
        def update_table(contents, filename):
            return self.controller.update_table(contents, filename)

        @self.app.callback(
            Output("interactive-graph", "figure"),
            [Input("chart-type", "value")],
        )
        def create_chart(selected_chart):
            return self.controller.create_chart(selected_chart)

        @self.app.callback(
            Output("insights", "children"), [Input("chart-type", "value")]
        )
        def generate_insights(selected_chart):
            return self.controller.generate_insights(selected_chart)


def main():
    app = DashboardApp()
    app.app.run_server(debug=True)


if __name__ == "__main__":
    main()
