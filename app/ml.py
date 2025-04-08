import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from app.customerrors import WrongFeaturesError


def process_dataframe(
    data: pd.DataFrame, features: list[str]
) -> pd.DataFrame | WrongFeaturesError:
    if set(features).issubset(data.columns):
        return data[features]
    else:
        raise WrongFeaturesError("Dataframe doesn't contain all features required!")


def get_predictions(
    input_features: list[str], model: BaseEstimator, data: pd.DataFrame
) -> (
    np.ndarray | WrongFeaturesError
):  # Still have to decide if it's better to use model object or just model path
    processed_data = process_dataframe(data, input_features)
    predictions = model.predict(processed_data)
    return predictions


if __name__ == "__main__":
    import joblib

    data = pd.read_csv("test_data/processed_airquality.csv")
    with open("models/linear.joblib", "rb") as f:
        lin_model = joblib.load(f)
    features = lin_model.feature_names_in_

    print(get_predictions(input_features=features, model=lin_model, data=data))
