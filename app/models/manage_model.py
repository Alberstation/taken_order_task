# graficas y estadisticas
import numpy as np
import pandas as pd
# Modelos
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn import tree
# Despliegue
import joblib
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("predictions.log"),
        logging.StreamHandler()  # Esto es opcional, también lo muestra en consola
    ]
)
logger = logging.getLogger(__name__)


class CustomTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def convert_categorical(self, df, column, n):
      # Count occurrences of each category
      counts = df[column].value_counts()

      # Get the top n categories by count
      top_categories = counts.index[:n]

      # Convert other categories to a common value
      df[column] = df[column].apply(lambda x: x if x in top_categories else 'Other')

      return df

    def transform(self, X, y=None):
        X_copy = X.copy()


        X_copy = X_copy.drop(['ORDER_ID', 'SATURATION'], axis=1)
        X_copy = self.convert_categorical(X_copy, 'CITY', 5)
        
        # Crear una columna para el día de la semana
        X_copy['dia_semana'] = X_copy['CREATED_AT'].dt.day_name().astype(str)
        # Crear una columna para la hora agrupada en intervalos de 1 hora
        X_copy['hora_grupo'] = X_copy['CREATED_AT'].dt.floor('H').dt.hour.astype(str)

        X_copy = X_copy.drop(['CREATED_AT'], axis=1)

        return X_copy

def create_pipe():
  variable_conversion = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(),  make_column_selector( dtype_include=np.number)),
        ("cat", OneHotEncoder(handle_unknown='ignore'), make_column_selector(dtype_include=object)),
    ]
  )
  pipe = Pipeline([
    ('custom_proccesing', CustomTransformer()),
    ('column_transformer',variable_conversion),
  ])
  return pipe


class ModelPredictor:
    def __init__(self):
        self.model_load_path = "app/models/modelo_decision_tree.pkl"
        self.pipeline_path = "app/models/pipeline.pkl"
        self.model = None
        self.pipeline = None

    def load_model(self):
        logging.info(f"Cargando el modelo desde {self.model_load_path}...")
        self.model = joblib.load(self.model_load_path)
        self.pipeline = joblib.load(self.pipeline_path)

    def get_data(self, data_json):
        logging.info("Obteniendo datos para predicciones...")
        data_to_classify = pd.DataFrame(data_json)
        data_to_classify['CREATED_AT'] = pd.to_datetime(data_to_classify['CREATED_AT'], errors='coerce')
        return data_to_classify

    def preprocess_data(self, data_to_classify):
        logging.info("Preprocesando datos para predicciones...")
        transformed_data = self.pipeline.transform(data_to_classify)
        return transformed_data

    def predict(self, transformed_data):
        logging.info("Realizando predicciones...")
        return self.model.predict(transformed_data)[0]

    def run(self, data_json):
        data_to_classify = self.get_data(data_json)
        X_preprocessed = self.preprocess_data(data_to_classify)
        predictions = self.predict(X_preprocessed)
        logging.info(f"Predicciones: {predictions}")
        return predictions

