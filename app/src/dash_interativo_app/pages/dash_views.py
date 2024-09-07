import plotly.graph_objs as go
from dash import dcc, html, Input, Output

class DashBoardViews:
    def __init__(self, app):
        self.app = app
        self.layout.create_layout(app)
        self.callbacks.create_callbacks(app)

    def home(self):
        return self.app.layout

    #CRIAR AS PAGINAS      HomePage, Page1, Page2, GraphPage


