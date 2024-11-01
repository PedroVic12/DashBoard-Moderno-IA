import dash
from dash import html, dcc, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
from django.core.wsgi import get_wsgi_application
import os
import django
from dash.dependencies import Input, Output, State
import base64
import io
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_ag_grid as dag

# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seu_projeto.settings")
django.setup()
application = get_wsgi_application()

# Importe seus modelos Django aqui
# from seu_app.models import SeuModelo

class DashController:
    def __init__(self):
        self.df = pd.DataFrame()

    def get_data(self):
        # Implemente a lógica para obter dados do Django
        # Exemplo: return pd.DataFrame(list(SeuModelo.objects.all().values()))
        return pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

    def post_data(self, data):
        # Implemente a lógica para salvar dados no Django
        # Exemplo: SeuModelo.objects.create(**data)
        pass

    def process_file(self, contents, filename):
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                self.df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            elif 'xlsx' in filename:
                self.df = pd.read_excel(io.BytesIO(decoded))
            else:
                return None
            return self.df.to_dict('records')
        except Exception as e:
            print(e)
            return None

class DashView:
    def __init__(self, controller):
        self.controller = controller
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):
        self.app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("Dashboard", className="text-center mb-4"),
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Arraste e solte ou ',
                            html.A('Selecione um Arquivo')
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        multiple=False
                    ),
                    html.Div(id='output-data-upload'),
                    dbc.Row([
                        dbc.Col(dmc.Card(children=[
                            dmc.CardSection(
                                dmc.Image(src="/assets/image1.png", height=160)
                            ),
                            dmc.Group(
                                [
                                    dmc.Text("Card 1", weight=500),
                                    dmc.Badge("Em andamento", color="blue", variant="light"),
                                ],
                                position="apart",
                                mt="md",
                                mb="xs",
                            ),
                            dmc.Text(
                                "This is the content of Card 1. You can put any information here.",
                                size="sm",
                                color="dimmed",
                            ),
                            dmc.Button(
                                "Ação do Card 1",
                                variant="light",
                                color="blue",
                                fullWidth=True,
                                mt="md",
                                radius="md",
                            ),
                        ], withBorder=True, shadow="sm", radius="md", style={"height": "100%"}), width=3),
                        dbc.Col(dmc.Card(children=[
                            dmc.CardSection(
                                dmc.Image(src="/assets/image2.png", height=160)
                            ),
                            dmc.Group(
                                [
                                    dmc.Text("Card 2", weight=500),
                                    dmc.Badge("Concluído", color="green", variant="light"),
                                ],
                                position="apart",
                                mt="md",
                                mb="xs",
                            ),
                            dmc.Text(
                                "This is the content of Card 2. You can put any information here.",
                                size="sm",
                                color="dimmed",
                            ),
                            dmc.Button(
                                "Ação do Card 2",
                                variant="light",
                                color="green",
                                fullWidth=True,
                                mt="md",
                                radius="md",
                            ),
                        ], withBorder=True, shadow="sm", radius="md", style={"height": "100%"}), width=3),
                        dbc.Col(dmc.Card(children=[
                            dmc.CardSection(
                                dmc.Image(src="/assets/image3.png", height=160)
                            ),
                            dmc.Group(
                                [
                                    dmc.Text("Card 3", weight=500),
                                    dmc.Badge("Pendente", color="yellow", variant="light"),
                                ],
                                position="apart",
                                mt="md",
                                mb="xs",
                            ),
                            dmc.Text(
                                "This is the content of Card 3. You can put any information here.",
                                size="sm",
                                color="dimmed",
                            ),
                            dmc.Button(
                                "Ação do Card 3",
                                variant="light",
                                color="yellow",
                                fullWidth=True,
                                mt="md",
                                radius="md",
                            ),
                        ], withBorder=True, shadow="sm", radius="md", style={"height": "100%"}), width=3),
                        dbc.Col(dmc.Card(children=[
                            dmc.CardSection(
                                dmc.Image(src="/assets/image4.png", height=160)
                            ),
                            dmc.Group(
                                [
                                    dmc.Text("Card 4", weight=500),
                                    dmc.Badge("Crítico", color="red", variant="light"),
                                ],
                                position="apart",
                                mt="md",
                                mb="xs",
                            ),
                            dmc.Text(
                                "This is the content of Card 4. You can put any information here.",
                                size="sm",
                                color="dimmed",
                            ),
                            dmc.Button(
                                "Ação do Card 4",
                                variant="light",
                                color="red",
                                fullWidth=True,
                                mt="md",
                                radius="md",
                            ),
                        ], withBorder=True, shadow="sm", radius="md", style={"height": "100%"}), width=3),
                    ], className="mb-4"),
                    dbc.Row([
                        dbc.Col([
                            dag.AgGrid(
                                id='grid',
                                columnDefs=[
                                    {"headerName": "Make", "field": "make"},
                                    {"headerName": "Model", "field": "model"},
                                    {"headerName": "Price", "field": "price"}
                                ],
                                rowData=[
                                    {"make": "Toyota", "model": "Celica", "price": 35000},
                                    {"make": "Ford", "model": "Mondeo", "price": 32000},
                                    {"make": "Porsche", "model": "Boxter", "price": 72000}
                                ],
                                dashGridOptions={"pagination": True, "paginationPageSize": 10},
                                style={"height": 400, "width": '100%'}
                            )
                        ], width=12)
                    ], className="mb-4"),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='example-graph')
                        ], width=12)
                    ])
                ])
            ])
        ], fluid=True)

    def setup_callbacks(self):
        @self.app.callback(
            Output('output-data-upload', 'children'),
            Output('grid', 'rowData'),
            Output('example-graph', 'figure'),
            Input('upload-data', 'contents'),
            State('upload-data', 'filename')
        )
        def update_output(contents, filename):
            if contents is None:
                raise PreventUpdate
            
            df = self.controller.process_file(contents, filename)
            if df is None:
                return html.Div(['Houve um erro ao processar este arquivo.']), [], {}

            # Atualiza a tabela
            table = dag.AgGrid(
                columnDefs=[{"headerName": col, "field": col} for col in df[0].keys()],
                rowData=df,
                dashGridOptions={"pagination": True, "paginationPageSize": 10},
                style={"height": 400, "width": '100%'}
            )

            # Cria o gráfico
            fig = px.scatter(df, x=df[0].keys()[0], y=df[0].keys()[1], title='Gráfico de Dispersão')

            return table, df, fig

    def run_server(self, debug=True, port=8050):
        self.app.run_server(debug=debug, port=port)

class DashPaginator:
    def __init__(self, page_size=10):
        self.page_size = page_size
        self.current_page = 1

    def paginate(self, data):
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        return data[start:end]

    def get_total_pages(self, data):
        return -(-len(data) // self.page_size)  # Ceiling division

    def next_page(self):
        self.current_page += 1

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    def go_to_page(self, page):
        self.current_page = page

class DashApp:
    def __init__(self):
        self.controller = DashController()
        self.view = DashView(self.controller)
        self.paginator = DashPaginator()

    def run(self):
        self.view.run_server()

if __name__ == '__main__':
    app = DashApp()
    app.run()
