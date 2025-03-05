import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator

def get_predictions(input_features: list[str], model: BaseEstimator, data: np.ndarray | pd.DataFrame):
    corrected_data = data[input_features]
    predictions = model.predict(corrected_data)
    return predictions