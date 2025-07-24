import pandas as pd
import xgboost as xgb

from lib import RAW_DATA_COLUMNS as DC
from model.hyperparams import get_xgbc_hyperparams


def train(data: pd.DataFrame) -> xgb.XGBClassifier:
    """Train the model with the data at the given path.

    Parameters:
        data: pd.DataFrame
            Preprocessed data to train the model with

    Returns:
        xgb.XGBClassifier
            Trained model
    """
    x_data, y = data.drop(DC.target, axis=1), data[DC.target]
    model = xgb.XGBClassifier(**get_xgbc_hyperparams())
    model.fit(x_data, y)
    return model
