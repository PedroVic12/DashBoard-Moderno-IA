import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
import io
import json
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import os
import django
from dash.exceptions import PreventUpdate

# Configure Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
django.setup()


# Class to manage application state
class AppState:
    def __init__(self):
        self.data = pd.DataFrame()
        self.filename = ""
        self.page_size = 10
        self.current_page = 1


app_state = AppState()


# Class to manage pagination
class DashPaginator:
    def __init__(self, data, page_size):
        self.paginator = Paginator(data, page_size)

    def get_page(self, page_number):
        return self.paginator.page(page_number)

    @property
    def num_pages(self):
        return self.paginator.num_pages


# Class to manage data operations
class DataManager:
    @staticmethod
    def load_data(contents, filename):
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        try:
            if "csv" in filename:
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            elif "xlsx" in filename:
                df = pd.read_excel(io.BytesIO(decoded))
            else:
                return pd.DataFrame()
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()
        return df

    @staticmethod
    def get_data_summary(df):
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "dtypes": df.dtypes.value_counts().to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
        }

    @staticmethod
    def get_column_stats(df, column):
        if pd.api.types.is_numeric_dtype(df[column]):
            return {
                "min": df[column].min(),
                "max": df[column].max(),
                "mean": df[column].mean(),
                "median": df[column].median(),
                "std": df[column].std(),
            }
        else:
            return {
                "unique_values": df[column].nunique(),
                "top_value": df[column].value_counts().index[0],
                "top_value_count": df[column].value_counts().iloc[0],
            }


# Class to create charts
class ChartManager:
    @staticmethod
    def create_line_chart(df, x_column, y_columns):
        fig = px.line(df, x=x_column, y=y_columns, title="Line Chart")
        return fig

    @staticmethod
    def create_bar_chart(df, x_column, y_column):
        fig = px.bar(df, x=x_column, y=y_column, title="Bar Chart")
        return fig

    @staticmethod
    def create_scatter_plot(df, x_column, y_column):
        fig = px.scatter(df, x=x_column, y=y_column, title="Scatter Plot")
        return fig

    @staticmethod
    def create_histogram(df, column):
        fig = px.histogram(df, x=column, title=f"Histogram of {column}")
        return fig

    @staticmethod
    def create_box_plot(df, column):
        fig = px.box(df, y=column, title=f"Box Plot of {column}")
        return fig


# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIAL])

# App layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dmc.Header(
            height=70,
            children=[
                dmc.Container(
                    fluid=True,
                    children=[
                        dmc.Group(
                            position="apart",
                            children=[
                                dmc.Text(
                                    "Comprehensive Dashboard", size="xl", color="white"
                                ),
                                dmc.Group(
                                    children=[
                                        dmc.NavLink("Home", href="/", active=True),
                                        dmc.NavLink("Data Overview", href="/data"),
                                        dmc.NavLink("Analysis", href="/analysis"),
                                        dmc.NavLink("Advanced Stats", href="/advanced"),
                                    ],
                                ),
                            ],
                        )
                    ],
                )
            ],
            style={"backgroundColor": "#6200ee"},
        ),
        html.Div(id="page-content"),
    ]
)


# Page layouts
def create_home_layout():
    return dmc.Container(
        [
            dmc.Title(
                "Welcome to the Comprehensive Dashboard",
                order=1,
                style={"textAlign": "center", "marginTop": "2rem"},
            ),
            dmc.Text(
                "Upload your data and explore insights",
                align="center",
                size="lg",
                style={"marginTop": "1rem"},
            ),
            dmc.Space(h=20),
            dmc.Center(
                dcc.Upload(
                    id="upload-data",
                    children=dmc.Button(
                        "Upload CSV/XLSX", leftIcon=DashIconify(icon="mdi:upload")
                    ),
                    multiple=False,
                )
            ),
            dmc.Space(h=20),
            html.Div(id="output-data-upload"),
            dmc.Space(h=20),
            dmc.Accordion(
                children=[
                    dmc.AccordionItem(
                        label="How to use this dashboard",
                        children=[
                            dmc.List(
                                [
                                    dmc.ListItem(
                                        "Upload your CSV or XLSX file on the Home page"
                                    ),
                                    dmc.ListItem(
                                        "Navigate to the Data Overview page to see a summary of your data"
                                    ),
                                    dmc.ListItem(
                                        "Use the Analysis page to create various charts"
                                    ),
                                    dmc.ListItem(
                                        "Explore Advanced Stats for deeper insights into your data"
                                    ),
                                ]
                            )
                        ],
                    ),
                    dmc.AccordionItem(
                        label="About this project",
                        children=[
                            dmc.Text(
                                "This comprehensive dashboard is built using Dash and integrates with Django for backend operations. It provides various features for data analysis and visualization."
                            )
                        ],
                    ),
                ],
            ),
        ]
    )


def create_data_layout():
    return dmc.Container(
        [
            dmc.Title("Data Overview", order=2),
            dmc.Space(h=20),
            dmc.Grid(
                [
                    dmc.Col(
                        dmc.Card(
                            children=[
                                dmc.CardSection(dmc.Text("Rows", weight=500)),
                                dmc.Group(
                                    [
                                        DashIconify(icon="mdi:table-row", width=30),
                                        dmc.Text(id="card-rows", size="xl"),
                                    ],
                                    spacing="xs",
                                ),
                            ]
                        ),
                        span=3,
                    ),
                    dmc.Col(
                        dmc.Card(
                            children=[
                                dmc.CardSection(dmc.Text("Columns", weight=500)),
                                dmc.Group(
                                    [
                                        DashIconify(icon="mdi:table-column", width=30),
                                        dmc.Text(id="card-columns", size="xl"),
                                    ],
                                    spacing="xs",
                                ),
                            ]
                        ),
                        span=3,
                    ),
                    dmc.Col(
                        dmc.Card(
                            children=[
                                dmc.CardSection(dmc.Text("Data Types", weight=500)),
                                dmc.Group(
                                    [
                                        DashIconify(
                                            icon="mdi:format-list-bulleted-type",
                                            width=30,
                                        ),
                                        dmc.Text(id="card-dtypes", size="xl"),
                                    ],
                                    spacing="xs",
                                ),
                            ]
                        ),
                        span=3,
                    ),
                    dmc.Col(
                        dmc.Card(
                            children=[
                                dmc.CardSection(dmc.Text("Missing Values", weight=500)),
                                dmc.Group(
                                    [
                                        DashIconify(
                                            icon="mdi:alert-circle-outline", width=30
                                        ),
                                        dmc.Text(id="card-missing", size="xl"),
                                    ],
                                    spacing="xs",
                                ),
                            ]
                        ),
                        span=3,
                    ),
                ]
            ),
            dmc.Space(h=20),
            dmc.Paper(
                children=[
                    dash_table.DataTable(
                        id="data-table",
                        page_size=10,
                        style_table={"overflowX": "auto"},
                        style_cell={
                            "minWidth": "100px",
                            "maxWidth": "300px",
                            "whiteSpace": "normal",
                            "textAlign": "left",
                        },
                    )
                ],
                shadow="sm",
                p="md",
            ),
            dmc.Space(h=20),
            dmc.Group(
                [
                    dmc.Button(
                        "Previous Page",
                        id="previous-page",
                        leftIcon=DashIconify(icon="mdi:chevron-left"),
                    ),
                    dmc.Text(id="page-info"),
                    dmc.Button(
                        "Next Page",
                        id="next-page",
                        rightIcon=DashIconify(icon="mdi:chevron-right"),
                    ),
                ],
                position="center",
            ),
        ]
    )


def create_analysis_layout():
    return dmc.Container(
        [
            dmc.Title("Data Analysis", order=2),
            dmc.Space(h=20),
            dmc.Grid(
                [
                    dmc.Col(
                        [
                            dmc.Select(
                                id="x-axis-select",
                                label="Select X-axis",
                                placeholder="Choose a column",
                                style={"marginBottom": 10},
                            ),
                            dmc.MultiSelect(
                                id="y-axis-select",
                                label="Select Y-axis",
                                placeholder="Choose columns",
                                style={"marginBottom": 10},
                            ),
                            dmc.Select(
                                id="chart-type-select",
                                label="Select Chart Type",
                                data=[
                                    {"label": "Line Chart", "value": "line"},
                                    {"label": "Bar Chart", "value": "bar"},
                                    {"label": "Scatter Plot", "value": "scatter"},
                                    {"label": "Histogram", "value": "histogram"},
                                    {"label": "Box Plot", "value": "box"},
                                ],
                                value="line",
                                style={"marginBottom": 10},
                            ),
                            dmc.Button(
                                "Generate Chart",
                                id="generate-chart",
                                style={"marginTop": 10},
                            ),
                        ],
                        span=3,
                    ),
                    dmc.Col([dcc.Graph(id="data-chart")], span=9),
                ]
            ),
        ]
    )


def create_advanced_layout():
    return dmc.Container(
        [
            dmc.Title("Advanced Statistics", order=2),
            dmc.Space(h=20),
            dmc.Grid(
                [
                    dmc.Col(
                        [
                            dmc.Select(
                                id="column-select",
                                label="Select Column",
                                placeholder="Choose a column",
                                style={"marginBottom": 10},
                            ),
                            dmc.Button(
                                "Calculate Statistics",
                                id="calculate-stats",
                                style={"marginTop": 10},
                            ),
                        ],
                        span=3,
                    ),
                    dmc.Col([html.Div(id="stats-output")], span=9),
                ]
            ),
        ]
    )


# Callbacks
@app.callback(
    [
        Output("output-data-upload", "children"),
        Output("data-table", "data"),
        Output("data-table", "columns"),
        Output("x-axis-select", "data"),
        Output("y-axis-select", "data"),
        Output("column-select", "data"),
        Output("card-rows", "children"),
        Output("card-columns", "children"),
        Output("card-dtypes", "children"),
        Output("card-missing", "children"),
    ],
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
)
def update_output(contents, filename):
    if contents is None:
        return [dash.no_update] * 10

    df = DataManager.load_data(contents, filename)
    if df.empty:
        return [f"Error loading file {filename}"] + [dash.no_update] * 9

    app_state.data = df
    app_state.filename = filename

    paginator = DashPaginator(df, app_state.page_size)
    page = paginator.get_page(1)
    data = page.object_list.to_dict("records")
    columns = [{"name": i, "id": i} for i in df.columns]
    column_options = [{"label": i, "value": i} for i in df.columns]

    summary = DataManager.get_data_summary(df)

    return (
        f"File {filename} loaded successfully",
        data,
        columns,
        column_options,
        column_options,
        column_options,
        str(summary["rows"]),
        str(summary["columns"]),
        ", ".join([f"{k}: {v}" for k, v in summary["dtypes"].items()]),
        str(sum(summary["missing_values"].values())),
    )


@app.callback(
    Output("data-chart", "figure"),
    [Input("generate-chart", "n_clicks")],
    [
        State("x-axis-select", "value"),
        State("y-axis-select", "value"),
        State("chart-type-select", "value"),
    ],
)
def update_chart(n_clicks, x_column, y_columns, chart_type):
    if n_clicks is None:
        raise PreventUpdate

    if not x_column or not y_columns or app_state.data.empty:
        return go.Figure()

    if isinstance(y_columns, str):
        y_columns = [y_columns]

    if chart_type == "line":
        return ChartManager.create_line_chart(app_state.data, x_column, y_columns)
    elif chart_type == "bar":
        return ChartManager.create_bar_chart(app_state.data, x_column, y_columns[0])
    elif chart_type == "scatter":
        return ChartManager.create_scatter_plot(app_state.data, x_column, y_columns[0])
    elif chart_type == "histogram":
        return ChartManager.create_histogram(app_state.data, x_column)
    elif chart_type == "box":
        return ChartManager.create_box_plot(app_state.data, y_columns[0])


@app.callback(
    Output("stats-output", "children"),
    [Input("calculate-stats", "n_clicks")],
    [State("column-select", "value")],
)
def update_stats(n_clicks, column):
    if n_clicks is None or not column or app_state.data.empty:
        raise PreventUpdate

    stats = DataManager.get_column_stats(app_state.data, column)
