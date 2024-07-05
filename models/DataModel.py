# models.py
import pandas as pd
import io
import base64


class DataModel:
    def __init__(self):
        self.df = pd.DataFrame()

    def load_data(self, contents, filename):
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        try:
            if "csv" in filename:
                self.df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            elif "xls" in filename:
                self.df = pd.read_excel(io.BytesIO(decoded))
            else:
                return False
        except Exception as error:
            print(error)
            return False
        return True
