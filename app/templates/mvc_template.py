import base64
import io

import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_material_components as dmc
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, State


# Modelo
class DataModel:
    def __init__(self):
        self.df = pd.DataFrame()

    def load_data(self, contents, filename):
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        try:
            if "csv" in filename:
                self.df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            elif "xls" in filename:
                self.df = pd.read_excel(io.BytesIO(decoded))
            else:
                return False
        except Exception as error:
            print(error)
            return False
        return True


# Visão
class FileUploadComponent:
    def __init__(self, id):
        self.id = id

    def render(self):
        return html.Div(
            [
                dcc.Upload(
                    id=self.id,
                    children=html.Div(
                        ["Arraste e solte ou ", html.A("selecione os arquivos")]
                    ),
                    style={
                        "width": "100%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "margin": "10px",
                    },
                    multiple=False,  # Permitir apenas um arquivo por vez
                ),
                html.Div(id=f"{self.id}-output"),
            ]
        )


class DataTableComponent:
    def __init__(self, id):
        self.id = id

    def render(self, df=None):
        if df is None:
            df = pd.DataFrame()
        return html.Div(
            [
                dag.AgGrid(
                    id=self.id,
                    rowData=df.to_dict("records"),
                    columnDefs=[{"field": i} for i in df.columns],
                    defaultColDef={
                        "filter": True,
                        "sortable": True,
                        "flex": 1,
                        "editable": True,
                        "floatingFilter": True,
                    },
                ),
            ]
        )


# Controlador
class DashboardController:
    def __init__(self, data_model):
        self.data_model = data_model
        self.file_upload_component = FileUploadComponent("upload-data")
        self.data_table_component = DataTableComponent("data-table")

    def update_table(self, contents, filename):
        if contents is not None:
            if self.data_model.load_data(contents, filename):
                return self.data_table_component.render(self.data_model.df)
            else:
                return html.Div("Erro ao carregar o arquivo. Verifique o formato.")
        else:
            return html.Div(
                "Nenhum arquivo selecionado. Arraste e solte ou selecione um arquivo CSV ou Excel."
            )


# Aplicação Dash
class DashboardApp:
    def __init__(self):
        self.data_model = DataModel()
        self.controller = DashboardController(self.data_model)
        self.chart_types = ["Bar Chart", "Line Chart", "Scatter Chart"]

        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

        self.app.layout = dmc.Dashboard(
            children=[
                dmc.NavBar(title="Interactive Data Visualization"),
                dmc.Page(
                    children=[
                        dmc.Section(
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            self.create_card("Card 1", "Content 1"),
                                            md=3,
                                        ),
                                        dbc.Col(
                                            self.create_card("Card 2", "Content 2"),
                                            md=3,
                                        ),
                                        dbc.Col(
                                            self.create_card("Card 3", "Content 3"),
                                            md=3,
                                        ),
                                        dbc.Col(
                                            self.create_card("Card 4", "Content 4"),
                                            md=3,
                                        ),
                                    ],
                                    className="mb-4",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                self.file_upload_component.render(),
                                                html.Div(
                                                    id="table-container",
                                                    children=[
                                                        self.data_table_component.render()
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
                                                        for i in self.chart_types
                                                    ],
                                                    value="Bar Chart",
                                                ),
                                                dcc.Graph(id="interactive-graph"),
                                                html.Div(id="insights"),
                                            ],
                                            md=6,
                                        ),
                                    ]
                                ),
                            ],
                            cards=[
                                {"title": "Card 1a"},
                                {"title": "Card 1b"},
                            ],
                        )
                    ]
                ),
            ]
        )

        @self.app.callback(
            Output("table-container", "children"),
            [
                Input("upload-data", "contents"),
                Input("upload-data", "filename"),
            ],
        )
        def display_output(contents, filename):
            return self.controller.update_table(contents, filename)

        @self.app.callback(
            [
                dash.Output("interactive-graph", "figure"),
                dash.Output("insights", "children"),
            ],
            [dash.Input("chart-type", "value")],
        )
        def update_graph(selected_chart):
            fig = self.create_chart(selected_chart)
            insights = self.generate_insights(selected_chart)
            return fig, insights

    def create_card(self, title, content):
        return dbc.Card(
            dbc.CardBody(
                [
                    html.H4(title, className="card-title"),
                    html.P(content, className="card-text"),
                ]
            )
        )

    def create_chart(self, selected_chart):
        if self.data_model.df.empty:
            return {}
        fig = None
        if selected_chart == "Bar Chart":
            fig = px.bar(
                self.data_model.df,
                x=self.data_model.df.columns[0],
                y=self.data_model.df.columns[1],
                color=self.data_model.df.columns[2],
            )
        elif selected_chart == "Line Chart":
            fig = px.line(
                self.data_model.df,
                x=self.data_model.df.columns[0],
                y=self.data_model.df.columns[1],
                color=self.data_model.df.columns[2],
            )
        elif selected_chart == "Scatter Chart":
            fig = px.scatter(
                self.data_model.df,
                x=self.data_model.df.columns[0],
                y=self.data_model.df.columns[1],
                color=self.data_model.df.columns[2],
            )

        fig.update_layout(
            title=f"{selected_chart} of AI Systems by Domain",
            xaxis_title="Year",
            yaxis_title="Annual Number of AI Systems",
            legend_title="Entity",
        )
        return fig

    def generate_insights(self, selected_chart):
        # Aqui você pode implementar lógica para gerar insights
        # baseados no tipo de gráfico selecionado.
        return f"This {selected_chart} shows the trends in the number of AI systems across different domains over time. You can see that..."

    def run(self):
        self.app.run_server(debug=True)


# Iniciar o backend
if __name__ == "__main__":
    app = DashboardApp()
    app.run()