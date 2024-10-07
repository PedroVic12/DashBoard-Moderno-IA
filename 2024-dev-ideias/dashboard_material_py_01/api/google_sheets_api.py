from fastapi import FastAPI
from pydantic import BaseModel
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = FastAPI()


class RowData(BaseModel):
    values: list


class GoogleSheetsAPI:
    def __init__(self, creds_file, sheet_id):
        self.sheet_id = sheet_id
        self.creds = service_account.Credentials.from_service_account_file(creds_file)
        self.service = build("sheets", "v4", credentials=self.creds)

    def add_row(self, values):
        body = {"values": [values]}
        self.service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id, range="A1", valueInputOption="RAW", body=body
        ).execute()

    def remove_row(self, row_index):
        # Implementar lógica para remover uma linha
        pass


sheets_api = GoogleSheetsAPI("credentials.json", "ID_DA_PLANILHA")


@app.post("/add-row/")
async def add_row(row_data: RowData):
    sheets_api.add_row(row_data.values)
    return {"status": "success"}


@app.delete("/remove-row/{row_index}")
async def remove_row(row_index: int):
    sheets_api.remove_row(row_index)
    return {"status": "success"}
