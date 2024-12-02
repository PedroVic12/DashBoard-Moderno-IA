import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLAgent:
    def __init__(self, role, description):
        self.role = role
        self.description = description
        self.data = None
        self.X = None
        self.y = None
        self.model = None
        self.results = None
        logger.info(f"Initialized {role} agent")
        
    def load_data(self, file_path: str) -> list:
        """Carrega dados do Excel e retorna colunas"""
        logger.info(f"{self.role}: Loading data from {file_path}")
        try:
            self.data = pd.read_excel(file_path)
            logger.info(f"Data loaded successfully. Shape: {self.data.shape}")
            return list(self.data.columns)
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def set_variables(self, x_column: str, y_column: str) -> None:
        """Define variáveis X e y"""
        logger.info(f"{self.role}: Setting X={x_column}, y={y_column}")
        try:
            self.X = self.data[x_column].values.reshape(-1, 1)
            self.y = self.data[y_column].values
            logger.info("Variables set successfully")
        except Exception as e:
            logger.error(f"Error setting variables: {str(e)}")
            raise

    def get_table_preview(self, rows=10):
        """Retorna preview da tabela"""
        return self.data.head(rows) if self.data is not None else None

    def format_results(self) -> str:
        """Formata resultados para markdown"""
        if not self.results:
            return "Aguardando treinamento do modelo..."
        return self.results

class KNNAgent(MLAgent):
    def __init__(self):
        super().__init__(
            role="KNN Regressor",
            description="Agente de regressão usando K-Nearest Neighbors"
        )
        self.model = KNeighborsRegressor(n_neighbors=5)
        
    def train_model(self) -> None:
        """Treina modelo KNN"""
        logger.info(f"{self.role}: Training model")
        try:
            self.model.fit(self.X, self.y)
            y_pred = self.model.predict(self.X)
            r2 = r2_score(self.y, y_pred)
            
            # Formatando resultados em markdown
            self.results = f"""
### Resultados do Modelo KNN

**R² Score:** {r2:.4f}

**Previsões de Exemplo:**
```
X = 10 → Y = {self.model.predict([[10]])[0]:.2f}
X = 20 → Y = {self.model.predict([[20]])[0]:.2f}
X = 30 → Y = {self.model.predict([[30]])[0]:.2f}
```
"""
            logger.info(f"Model trained successfully. R2 Score: {r2:.4f}")
            return self.results
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise

class DecisionTreeAgent(MLAgent):
    def __init__(self):
        super().__init__(
            role="Decision Tree Regressor",
            description="Agente de regressão usando Árvore de Decisão"
        )
        self.model = DecisionTreeRegressor(max_depth=5)
        
    def train_model(self) -> None:
        """Treina modelo de Árvore de Decisão"""
        logger.info(f"{self.role}: Training model")
        try:
            self.model.fit(self.X, self.y)
            y_pred = self.model.predict(self.X)
            r2 = r2_score(self.y, y_pred)
            
            # Formatando resultados em markdown
            self.results = f"""
### Resultados da Árvore de Decisão

**R² Score:** {r2:.4f}

**Previsões de Exemplo:**
```
X = 10 → Y = {self.model.predict([[10]])[0]:.2f}
X = 20 → Y = {self.model.predict([[20]])[0]:.2f}
X = 30 → Y = {self.model.predict([[30]])[0]:.2f}
```

**Importância das Features:** {self.model.feature_importances_[0]:.4f}
"""
            logger.info(f"Model trained successfully. R2 Score: {r2:.4f}")
            return self.results
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise
