# components.py
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd


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


class CardComponent:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def render(self):
        return dbc.Card(
            dbc.CardBody(
                [
                    html.H4(self.title, className="card-title"),
                    html.P(self.content, className="card-text"),
                ]
            )
        )
