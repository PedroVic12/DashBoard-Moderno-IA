import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

class RegressionAgent:
    def __init__(self):
        self.model = LinearRegression()
        self.data = None
        self.X = None
        self.y = None
        self.r2 = None
        
    def load_data(self, file_path):
        """Load data from CSV or Excel file"""
        if file_path.endswith('.csv'):
            self.data = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            self.data = pd.read_excel(file_path)
        return list(self.data.columns)
    
    def set_variables(self, x_column, y_column):
        """Set X and y variables for regression"""
        self.X = self.data[x_column].values.reshape(-1, 1)
        self.y = self.data[y_column].values
        
    def train_model(self):
        """Train the linear regression model"""
        self.model.fit(self.X, self.y)
        self.r2 = r2_score(self.y, self.model.predict(self.X))
        
    def predict(self, x_value):
        """Make prediction for a single value"""
        return self.model.predict([[x_value]])[0]
    
    def get_equation(self):
        """Get the regression equation"""
        if hasattr(self.model, 'coef_') and hasattr(self.model, 'intercept_'):
            slope = self.model.coef_[0]
            intercept = self.model.intercept_
            return f"y = {slope:.2f}x + {intercept:.2f}"
        return None
