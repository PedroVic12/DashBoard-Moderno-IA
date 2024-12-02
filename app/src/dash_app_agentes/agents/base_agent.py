import pandas as pd
from abc import ABC, abstractmethod
from typing import List, Tuple, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self):
        self.data = None
        self.X = None
        self.y = None
        self.model = None
        
    def load_data(self, file_path: str) -> List[str]:
        """Load data from Excel file and return column names"""
        logger.info(f"Loading data from {file_path}")
        try:
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                self.data = pd.read_excel(file_path)
            else:
                raise ValueError("Only Excel files are supported")
            
            logger.info(f"Data loaded successfully. Shape: {self.data.shape}")
            return list(self.data.columns)
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def set_variables(self, x_column: str, y_column: str) -> None:
        """Set X and y variables for model"""
        logger.info(f"Setting variables - X: {x_column}, y: {y_column}")
        try:
            self.X = self.data[x_column].values.reshape(-1, 1)
            self.y = self.data[y_column].values
            logger.info("Variables set successfully")
        except Exception as e:
            logger.error(f"Error setting variables: {str(e)}")
            raise
    
    @abstractmethod
    def train_model(self) -> Tuple[float, Any]:
        """Train the model and return accuracy score and additional info"""
        pass
    
    @abstractmethod
    def predict(self, x_value: float) -> float:
        """Make prediction for a single value"""
        pass
    
    def get_data_preview(self, rows: int = 10) -> pd.DataFrame:
        """Get a preview of the loaded data"""
        logger.info(f"Getting data preview. Rows: {rows}")
        return self.data.head(rows) if self.data is not None else None
