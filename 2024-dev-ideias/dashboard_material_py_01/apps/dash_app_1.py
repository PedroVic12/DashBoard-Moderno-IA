import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Input(id="input-data", type="text", placeholder="Adicionar nova linha"),
        html.Button("Adicionar", id="button-add", n_clicks=0),
        html.Button("Remover", id="button-remove", n_clicks=0),
        dcc.Store(id="store-data"),  # Para armazenar dados em memória
        html.Div(id="output-container"),
        dcc.Checklist(
            options=[{"label": "Notificar por e-mail", "value": "notify"}],
            id="toggle-email",
            value=[],
        ),
    ]
)


@app.callback(
    Output("output-container", "children"),
    Input("button-add", "n_clicks"),
    Input("input-data", "value"),
    Input("toggle-email", "value"),
)
def update_output(n_clicks, input_value, toggle_email):
    if n_clicks > 0 and input_value:
        response = requests.post(
            "http://localhost:8000/add-row/", json={"values": [input_value]}
        )
        if response.status_code == 200:
            if "notify" in toggle_email:
                requests.post("http://localhost:8000/toggle-update/")
            return f"Adicionado: {input_value}"
    return "Nenhum dado adicionado."


if __name__ == "__main__":
    app.run_server(debug=True)
