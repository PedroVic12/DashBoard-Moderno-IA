import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_material_components as dmc
import pandas as pd
import base64
import io
import plotly.express as px
from dash.dependencies import Input, Output

# Instanciar o app
app = dash.Dash(__name__)

# Layout do app
upload_image = dmc.Upload(
    id="upload-image", label="Faça Upload de Imagens", multiple=True
)

upload_data = dmc.Upload(
    id="upload-data", label="Faça Upload de CSV/XLSX", multiple=False
)

data_table = dmc.DataTable(id="data-table")

line_chart = dmc.Graph(id="line-chart")
bar_chart = dmc.Graph(id="bar-chart")

layout = dmc.Dashboard(
    children=[
        dmc.NavBar(title="Dashboard de Imagens e Dados"),
        dmc.Page(
            orientation="columns",
            children=[
                dmc.Section(
                    id="upload-section",
                    orientation="columns",
                    children=[
                        upload_image,
                        upload_data,
                    ],
                ),
                dmc.Section(
                    id="data-section",
                    orientation="columns",
                    children=[
                        data_table,
                        line_chart,
                        bar_chart,
                    ],
                ),
            ],
        ),
    ]
)

app.layout = layout


@app.callback(
    Output("data-table", "data"),
    Output("line-chart", "figure"),
    Output("bar-chart", "figure"),
    Input("upload-data", "contents"),
)
def update_output(uploaded_file):
    if uploaded_file is not None:
        content_type, content_string = uploaded_file.split(",")
        decoded = base64.b64decode(content_string)
        if "csv" in uploaded_file:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xlsx" in uploaded_file:
            df = pd.read_excel(io.BytesIO(decoded))

        # Atualizar a tabela de dados
        data = df.to_dict("records")

        # Gráficos
        line_fig = px.line(
            df, x=df.columns[0], y=df.columns[1:], title="Gráfico de Linhas"
        )
        bar_fig = px.bar(
            df, x=df.columns[0], y=df.columns[1:], title="Gráfico de Barras"
        )

        return data, line_fig, bar_fig

    return [], {}, {}


@app.callback(
    Output("upload-image", "children"),
    Input("upload-image", "contents"),
)
def upload_image_callback(contents):
    if contents is not None:
        images = [base64.b64decode(c.split(",")[1]) for c in contents]
        return [
            html.Img(
                src="data:image/png;base64," + base64.b64encode(image).decode("utf-8"),
                style={"max-width": "300px"},
            )
            for image in images
        ]
    return []


if __name__ == "__main__":
    app.run_server(debug=True)
