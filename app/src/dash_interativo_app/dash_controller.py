import plotly.graph_objs as go
from dash import dcc, html, Input, Output


class DataModel:
    def __init__(self):
        self.df = None

    def load_data(self, contents, filename):
        # Logic to load data from CSV or Excel file
        # This is a placeholder implementation
        self.df = pd.read_csv(filename)
        return True

    def get_leads_data(self):
        # Placeholder implementation
        return [
        {"mes": "Jul-19", "leads": 8852},
        {"mes": "Ago-19", "leads": 8357},
        {"mes": "Set-19", "leads": 8657},
        {"mes": "Out-19", "leads": 11084},
        {"mes": "Nov-19", "leads": 12489},
        {"mes": "Dez-19", "leads": 996},
        ]

    def get_valor_membro_data(self):
        # Placeholder implementation
        return [
        {"tipo_membro": "Black", "valor_venda": 15.27},
        {"tipo_membro": "Platinum", "valor_venda": 31.35},
        {"tipo_membro": "Gold", "valor_venda": 53.26},
        ]


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


# controllers.py
class DashboardController:
    def __init__(self, data_model):
        self.data_model = data_model

    def create_chart(self, selected_chart):
        if self.data_model.df is None or self.data_model.df.empty:
            return {}
        
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
        else:
            return {}

        fig.update_layout(
            title=f"{selected_chart} of AI Systems by Domain",
            xaxis_title="Year",
            yaxis_title="Annual Number of AI Systems",
            legend_title="Entity",
        )
        return fig

    def generate_insights(self, selected_chart):
        return f"This {selected_chart} shows the trends in the number of AI systems across different domains over time. You can see that..."