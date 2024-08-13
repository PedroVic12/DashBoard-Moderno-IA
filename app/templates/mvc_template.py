import base64
import io

import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_material_components as dmc
import pandas as pd
from dash import dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from components import ComponentesDash


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


class tabelaComponent:
    def __init__(self, path):
        self.path = path
        self.id = "tabela"

    def render(self):
        df = pd.read_excel(self.path)
        return html.Div(
            [
                dag.AgGrid(
                    id=self.id,
                    rowData=df.to_dict("records"),
                    columnDefs=[{"field": i} for i in df.columns],
                    dashGridOptions={
                        "animateRows": False,
                        "paginationPageSizeSelector": True,
                        "includeHiddenColumnsInQuickFilter": True,
                    },
                    defaultColDef={
                        "resizeable": False,
                        "filter": True,
                        "sortable": True,
                        "editable": True,
                        "cellDataType": False,
                        "floatingFilter": True,
                        "useValueFormatterForExport": False,
                    },
                    style={"height": "800px", "width": "100%", "overflowY": "auto"},
                ),
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
                        # "flex": 1,
                        "editable": True,
                        "floatingFilter": True,
                    },
                    style={"height": "600px", "width": "100%", "overflowY": "auto"},
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
        self.componentes = ComponentesDash()

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
            ],
        )

        @self.app.callback(
            Output("page-content", "children"), [Input("url", "pathname")]
        )
        def display_page(pathname):
            if pathname == "/page-1":
                return self.render_page_1()
            elif pathname == "/page-2":
                return self.render_page_2()
            elif pathname == "/graph-page":
                return self.render_graph_page()
            elif pathname == "/":
                return self.render_home()
            else:
                return self.render_home()

        @self.app.callback(
            Output("table-container", "children"),
            [Input("upload-data", "contents"), Input("upload-data", "filename")],
        )
        def display_output(contents, filename):
            return self.controller.update_table(contents, filename)

        @self.app.callback(
            [Output("interactive-graph", "figure"), Output("insights", "children")],
            [Input("chart-type", "value")],
        )
        def update_graph(selected_chart):
            fig = self.create_chart(selected_chart)
            insights = self.generate_insights(selected_chart)
            return fig, insights

    def render_page_1(self):
        # Variáveis
        text = dmc.Typography(text="Content...", component="p", variant="body2")
        text_2 = dmc.Typography(text="OLA MUNDO...", component="p", variant="body2")
        image_path = "/home/pedrov/Documentos/GitHub/DashBoard-Moderno-IA/assets/graficos/teste1.png"

        # Componentes
        section_1 = dmc.Section(
            id="section-1",
            orientation="columns",
            children=[text, text_2],
            cards=[{"title": "Card 1a", "size": 3}, {"title": "Card 1b"}],
        )

        diretorio = "/home/pedrov/Documentos/GitHub/Engenharia-Eletrica-UFF/Iniciação Cientifica - Eng Eletrica UFF/evolution_rce_master/src/views/tabelas"
        tabela2 = tabelaComponent(f"{diretorio}/tabela_consolidada.xlsx")

        page = dmc.Page(
            orientation="columns",
            children=[
                section_1,
            ],
        )

        # Render
        return html.Div(
            [
                html.H1("Resultados 12/07"),
                dmc.Section(
                    id="section-1",
                    orientation="columns",
                    children=[text, text_2],
                    cards=[{"title": "Card 1a", "size": 3}, {"title": "Card 1b"}],
                ),  # self.componentes.imagemDraw(image_path),
                section_1,
                html.H3("Tabela Teste Otimizacao"),
                tabela2.render(),
            ]
        )

    def render_page_2(self):
        diretorio = "/home/pedrov/Documentos/GitHub/Engenharia-Eletrica-UFF/Iniciação Cientifica - Eng Eletrica UFF/evolution_rce_master/src/views/tabelas"

        tabela1 = tabelaComponent(f"{diretorio}/tabela_resumo.xlsx")
        tabela2 = tabelaComponent(f"{diretorio}/tabela_consolidada.xlsx")
        tabela3 = tabelaComponent(f"{diretorio}/parametros_evolutivos.xlsx")
        tabela4 = tabelaComponent(f"{diretorio}/statistics_RCE.xlsx")
        tabela_valores = tabelaComponent(f"{diretorio}/rce_values.xlsx")
        # tabela_pop = tabelaComponent(f"{diretorio}/pop_final.xlsx")

        return html.Div(
            [
                html.H1("Page 2 - tabelas"),
                html.P("Tabela Evolutivos"),
                tabela3.render(),
                html.P("Tabela Resumo"),
                tabela1.render(),
                html.H3("Tabela Teste Otimizacao"),
                tabela2.render(),
                html.H3("Tabela População Final"),
                # tabela_pop.render(),
                html.H3("Tabela Valores Grafico RCE"),
                tabela_valores.render(),
                html.H3("Tabela Estatística"),
                tabela4.render(),
            ]
        )

    def render_home(self):
        return html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(self.create_card("Best Solutiom Gen", "145"), md=3),
                        dbc.Col(
                            self.create_card(
                                "Solution Fitness", "0.0024449194511966255"
                            ),
                            md=3,
                        ),
                        dbc.Col(
                            self.create_card(
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
                                        for i in self.chart_types
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

    def render_graph_page(self):
        diretorio = "/home/pedrov/Documentos/GitHub/Engenharia-Eletrica-UFF/Iniciação Cientifica - Eng Eletrica UFF/evolution_rce_master/src/views/tabelas/rce_values.xlsx"

        return html.Div(
            [
                html.H1("Graph Page"),
                dcc.Graph(id="rce-graph", style={"height": "500px"}),
                html.Div(
                    id="hidden-dataframe-path",
                    style={"display": "none"},
                    children=diretorio,
                ),
            ]
        )

    def create_rce_grafico(self):
        diretorio = "/home/pedrov/Documentos/GitHub/Engenharia-Eletrica-UFF/Iniciação Cientifica - Eng Eletrica UFF/evolution_rce_master/src/views/tabelas/rce_values.xlsx"

        df = pd.read_excel(diretorio)
        # Assegure-se de que o DataFrame contém as colunas necessárias
        if (
            df.empty
            or "Generations" not in df.columns
            or "min_fitness" not in df.columns
            or "max_fitness" not in df.columns
            or "avg_fitness" not in df.columns
        ):
            return {}

        gen = np.array(df["Generations"].dropna().values[0])
        # gen = np.array(gen)
        min_fitness = np.array(df["min_fitness"].dropna().values[0])
        avg_fitness = np.array(df["avg_fitness"].dropna().values[0])
        print(min_fitness, type(gen))

        max_fitness = np.array(df["max_fitness"].dropna().values[0])

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=gen,
                y=min_fitness,
                mode="lines+markers",
                name="Minimum Fitness",
                marker=dict(symbol="star", color="blue"),
                line=dict(color="blue"),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=gen,
                y=avg_fitness,
                mode="lines+markers",
                name="Average Fitness",
                marker=dict(symbol="cross", color="red"),
                line=dict(color="red"),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=gen,
                y=max_fitness,
                mode="lines+markers",
                name="Maximum Fitness",
                marker=dict(symbol="circle", color="green"),
                line=dict(color="green"),
            )
        )

        fig.update_layout(
            title="RCE Graph",
            xaxis_title="Generation",
            yaxis_title="Fitness",
            legend_title="Legend",
            template="plotly_white",
        )

        return fig

    # widgets
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
        return f"This {selected_chart} shows the trends in the number of AI systems across different domains over time. You can see that..."

    def create_table_component(self, path):
        df = pd.read_excel(path)
        return DataTableComponent("tabela").render(df)

    def run(self):
        self.app.run_server(debug=True)


# Iniciar o backend
if __name__ == "__main__":
    app = DashboardApp()
    app.run()
