# components.py
import plotly.graph_objs as go
from dash import dcc
import dash_bootstrap_components as dbc

import random
import dash_html_components as html


class DragWidget:
    def __init__(self, num_items=4):
        self.num_items = num_items

    def custom_style(self):
        return {
            'width': '100px',
            'height': '100px',
            'margin': '10px',
            'background-color': random.choice(['red', 'green', 'blue', 'yellow', 'black'])
        }

    def layout(self):
        return html.Div([
            html.Div(style=self.custom_style()) for _ in range(self.num_items)
        ], id='drag-container', style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})

class DragWidgetPage:
    def __init__(self):
        self.drag_widget = DragWidget()

    def layout(self):
        return html.Div([
            html.H1("Drag Widget Page"),
            self.drag_widget.layout()
        ])
    

class GraphUpdater:
    def __init__(self, graph_id, title, x_label, y_label):
        self.graph_id = graph_id
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

    def get_graph(self):
        return dcc.Graph(id=self.graph_id)

    def update_graph(self, x, y, mode="lines+markers", graph_type="scatter"):
        if graph_type == "scatter":
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode=mode))
            fig.update_layout(
                title=self.title, xaxis_title=self.x_label, yaxis_title=self.y_label
            )
        elif graph_type == "pie":
            fig = go.Figure(data=[go.Pie(labels=x, values=y)])
            fig.update_layout(title=self.title)
        return fig

class CardComponent:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def render(self):
        return dbc.Card(dbc.CardBody([html.H4(self.title), html.P(self.content)]))