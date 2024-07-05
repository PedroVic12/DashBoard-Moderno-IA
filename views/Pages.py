# pages.py
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


class HomePage:
    def __init__(self, controller):
        self.controller = controller

    def render(self):
        return html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            self.controller.create_card("Best Solutiom Gen", "145"),
                            md=3,
                        ),
                        dbc.Col(
                            self.controller.create_card(
                                "Solution Fitness", "0.0024449194511966255"
                            ),
                            md=3,
                        ),
                        dbc.Col(
                            self.controller.create_card(
                                "Best Variables",
                                " [-0.0033434768319050307, 0.0010701636253402924, -1.768567430659968, 1.1853520986045913, -1.9004680297648529, 0.22743145797017267, 4.695880471248139, -2.8245430126024518, -1.2659481646270128, -7.298325591972182]",
                            ),
                            md=3,
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                self.controller.file_upload_component.render(),
                                html.Div(
                                    id="table-container",
                                    children=[
                                        self.controller.data_table_component.render()
                                    ],
                                ),
                            ],
                            md=6,
                        ),
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                    id="chart-type",
                                    options=[
                                        {"label": i, "value": i}
                                        for i in self.controller.chart_types
                                    ],
                                    value="Bar Chart",
                                ),
                                dcc.Graph(
                                    id="interactive-graph", style={"height": "500px"}
                                ),
                                html.Div(id="insights"),
                            ],
                            md=6,
                        ),
                    ],
                ),
            ]
        )


class Page1:
    def __init__(self):
        pass

    def render(self):
        return html.Div(
            [
                html.H1("Page 1"),
                html.P("Conteúdo da Página 1"),
            ]
        )


class Page2:
    def __init__(self):
        pass

    def render(self):
        return html.Div(
            [
                html.H1("Page 2"),
                html.P("Conteúdo da Página 2"),
            ]
        )


class GraficoPlottyRCE:
    def __init__(self, controller):
        self.controller = controller

    def render(self):
        return html.Div(
            [
                html.H1("Graph Page"),
                dcc.Graph(id="rce-graph", style={"height": "500px"}),
                html.Div(
                    id="hidden-dataframe-path",
                    style={"display": "none"},
                    children="/home/pedrov/Documentos/GitHub/Engenharia-Eletrica-UFF/Iniciação Cientifica - Eng Eletrica UFF/evolution_rce_master/src/views/tabelas/rce_values.xlsx",
                ),
            ]
        )
