import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import requests

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Input(id="input-data", type="text", placeholder="Adicionar nova linha"),
        html.Button("Adicionar", id="button-add", n_clicks=0),
        dcc.Store(id="store-data"),
        html.Div(id="output-container"),
        html.Div(id="image-gallery"),
    ]
)


@app.callback(
    Output("output-container", "children"),
    Input("button-add", "n_clicks"),
    Input("input-data", "value"),
)
def update_output(n_clicks, input_value):
    if n_clicks > 0 and input_value:
        # Adicionar lógica de adicionar nova imagem, se necessário
        return f"Adicionado: {input_value}"
    return "Nenhum dado adicionado."


if __name__ == "__main__":
    app.run_server(debug=True)
