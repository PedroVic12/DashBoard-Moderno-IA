# dashboard_app/dash_view.py

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def create_layout():
    layout = dbc.Container(
        [
            dbc.Row(
                [dbc.Col(html.H1("Dashboard de Imagens e Dados"), className="mb-2")]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Upload(
                            id="upload-image",
                            children=html.Button("Upload de Imagens"),
                            multiple=True,
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        dcc.Upload(
                            id="upload-data",
                            children=html.Button("Upload de CSV/XLSX"),
                            multiple=False,
                        ),
                        width=4,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div(id="output-image-upload"), width=6),
                    dbc.Col(dash.dash_table.DataTable(id="data-table"), width=6),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="line-chart"), width=6),
                    dbc.Col(dcc.Graph(id="bar-chart"), width=6),
                ]
            ),
        ]
    )
    return layout
