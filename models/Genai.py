from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import re
import os
import io
import base64
import time
import plotly.graph_objects as go
import google.generativeai as genai
import plotly.express as px


class genaiInterpretador:

    def __init__(self):
        genai.configure(api_key=os.getenv("AIzaSyCZhKI6vWIAK0GkzXajc-PUjTBEO5zjoeA"))

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def analyze_chart(self, fig):
        fig_object = go.Figure(fig)
        fig_object.write_image(f"images/fig.png")
        time.sleep(1)

        image_path = f"images/fig.png"
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")

        response = genai.generate_text(
            model="gemini-pro",
            prompt=f"Descreva os insights do gráfico: \n\n"
            f"O gráfico é: {base64_image}",
            temperature=0.7,
        )

        return response.text

    def generativeAI(self, prompt):
        response = genai.generate_text(
            model="gemini-pro",
            prompt=prompt,
            temperature=0.7,
        )
        return response.text
