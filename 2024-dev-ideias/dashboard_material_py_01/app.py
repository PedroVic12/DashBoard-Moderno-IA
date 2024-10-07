import time
import smtplib
import pandas as pd
import schedule
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dash import Dash, dcc, html, Input, Output
import dash_material_components as dmc


# Classe para envio de e-mail
class EmailSender:
    def __init__(self, de, senha, para):
        self.de = de
        self.senha = senha
        self.para = para

    def send_email(self, corpo):
        mensagem = MIMEMultipart()
        mensagem["From"] = self.de
        mensagem["To"] = self.para
        mensagem["Subject"] = "Relatório Diário"

        mensagem.attach(MIMEText(corpo, "plain"))

        try:
            servidor = smtplib.SMTP("smtp.gmail.com", 587)
            servidor.starttls()
            servidor.login(self.de, self.senha)
            servidor.send_message(mensagem)
            print("Relatório enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
        finally:
            servidor.quit()


# Classe para manipulação do Google Sheets
class GoogleSheetsAPI:
    def __init__(self, creds_file, sheet_id):
        self.sheet_id = sheet_id
        self.creds = service_account.Credentials.from_service_account_file(creds_file)
        self.service = build("sheets", "v4", credentials=self.creds)

    def get_data(self):
        sheet = self.service.spreadsheets()
        result = (
            sheet.values().get(spreadsheetId=self.sheet_id, range="A1:Z100").execute()
        )
        values = result.get("values", [])
        return values


# Classe para agendar o envio de relatórios
class ReportScheduler:
    def __init__(self, email_sender, google_sheets_api):
        self.email_sender = email_sender
        self.google_sheets_api = google_sheets_api

    def enviar_relatorio(self):
        dados = self.google_sheets_api.get_data()
        corpo = "Aqui está o seu relatório diário:\n\n" + str(dados)
        self.email_sender.send_email(corpo)

    def agendar_relatorio(self):
        schedule.every().day.at("08:00").do(self.enviar_relatorio)
        while True:
            schedule.run_pending()
            time.sleep(60)


# Função para criar o dashboard
def create_dash_app(google_sheets_api):
    app = Dash(__name__)

    app.layout = dmc.Dashboard(
        children=[
            dmc.NavBar(title="Dashboard Relatório"),
            dmc.Page(
                orientation="columns",
                children=[
                    dmc.Section(
                        id="section-1",
                        orientation="columns",
                        children=[
                            dcc.Input(
                                id="input-search",
                                type="text",
                                placeholder="Pesquisar por ID",
                            ),
                            html.Button("Buscar", id="button-search", n_clicks=0),
                            html.Div(id="output-container"),
                        ],
                    )
                ],
            ),
        ]
    )

    @app.callback(
        Output("output-container", "children"),
        Input("button-search", "n_clicks"),
        Input("input-search", "value"),
    )
    def update_output(n_clicks, search_value):
        if n_clicks > 0 and search_value:
            data = google_sheets_api.get_data()
            df = pd.DataFrame(
                data[1:], columns=data[0]
            )  # Ignora a primeira linha como cabeçalho
            result = df[df["ID"] == search_value]
            return result.to_html()
        return "Nenhum resultado encontrado."

    return app


if __name__ == "__main__":
    email_sender = EmailSender(
        "seu_email@gmail.com", "sua_senha", "destinatario@example.com"
    )
    google_sheets_api = GoogleSheetsAPI("credentials.json", "ID_DA_PLANILHA")

    # Agendar o envio de relatórios
    scheduler = ReportScheduler(email_sender, google_sheets_api)
    # Iniciar o agendamento em uma thread
    import threading

    threading.Thread(target=scheduler.agendar_relatorio, daemon=True).start()

    # Iniciar o dashboard
    dash_app = create_dash_app(google_sheets_api)
    dash_app.run_server(debug=True)
