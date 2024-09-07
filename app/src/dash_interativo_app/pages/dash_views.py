# views.py
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, Input, Output, State
from widgets.my_components import GraphUpdater
import pandas as pd
import plotly.express as px
import io
import base64


class HomePage:
    def __init__(self, controller):
        self.controller = controller
        self.graphs = {
            "leads_mes_graph": GraphUpdater(
                "leads_mes_graph", "Leads por Mês Ano", "Mês", "Leads"
            ),
            "valor_membro_graph": GraphUpdater(
                "valor_membro_graph", "Valor Venda por Tipo Membro", "", ""
            ),
        }

    def layout(self):
        return dbc.Container([
            html.H1("Marketing DASHBOARD INTERATIVO", style={"textAlign": "center", "marginBottom": "20px"}),
            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody([html.H2("R$ 1.74 Mi"), html.P("Gastos Marketing")])), md=3),
                dbc.Col(dbc.Card(dbc.CardBody([html.H2("53,530"), html.P("Leads")])), md=3),
                dbc.Col(dbc.Card(dbc.CardBody([html.H2("33,674"), html.P("Ingressantes")])), md=3),
                dbc.Col(dbc.Card(dbc.CardBody([html.H2("R$ 4.8 Mi"), html.P("Valor Venda")])), md=3),
            ], className="mb-4"),
            dbc.Row([
                dbc.Col(self.graphs["leads_mes_graph"].get_graph(), md=6),
                dbc.Col(self.graphs["valor_membro_graph"].get_graph(), md=6),
            ]),
            html.Hr(),
            html.H2("Upload de Arquivo Excel", style={"textAlign": "center", "marginTop": "20px"}),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Arraste e solte ou ',
                    html.A('Selecione um Arquivo Excel')
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
            dbc.Col(id='output-data-upload', md=12),  # Coluna para a tabela e gráficos
        ], fluid=True)

    def parse_contents(self, contents, filename):
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'xls' in filename:
                df = pd.read_excel(io.BytesIO(decoded))
            elif 'csv' in filename:
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            else:
                return html.Div([
                    'Por favor, faça upload de um arquivo Excel (.xls ou .xlsx) ou CSV (.csv).'
                ])
        except Exception as e:
            print(e)
            return html.Div([
                'Houve um erro ao processar este arquivo.'
            ])

        return html.Div([
            html.H5(filename),
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                page_size=10,
                style_table={'overflowX': 'auto'},
            ),
            html.Div(className="mt-4"),  # Espaçamento entre a tabela e os gráficos
            dbc.Row([
                dbc.Col(dcc.Graph(figure=px.line(df, x=df.columns[0], y=df.columns[1], title='Gráfico de Linha')), md=4),
                dbc.Col(dcc.Graph(figure=px.bar(df, x=df.columns[0], y=df.columns[1], title='Gráfico de Barras')), md=4),
                dbc.Col(dcc.Graph(figure=px.scatter(df, x=df.columns[0], y=df.columns[1], title='Gráfico de Dispersão')), md=4)
            ])
        ])

    def callbacks(self, app):
        @app.callback(Output('output-data-upload', 'children'),
                      Input('upload-data', 'contents'),
                      State('upload-data', 'filename'))
        def update_output(contents, filename):
            if contents is not None:
                children = [self.parse_contents(contents, filename)]
                return children

    def material_app(self):
        return self.layout()







    
class Page1:
    def layout(self):
        return html.Div([html.H1("Page 1")])

class Page2:
    def layout(self):
        return html.Div([html.H1("Page 2")])

class GraphPage:
    def __init__(self, controller):
        self.controller = controller

    def layout(self):
        return html.Div([html.H1("Graph Page")])