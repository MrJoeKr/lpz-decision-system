import pandas as pd

# Number of positive and negative samples in the training data
_NEG_N: int = 3633
_POS_N: int = 466

_XGBC_HYPERPARAMS: dict = {
    "objective": "binary:logistic",
    "n_estimators": 100,
    "max_depth": 6,
    "learning_rate": 0.1,
    "n_jobs": -1,
    "random_state": 42,
    # "eval_metric": "logloss",
    # Categorical features
    "enable_categorical": True,
    "scale_pos_weight": _NEG_N / _POS_N,
}


def get_xgbc_hyperparams() -> dict:
    """Return hyperparameters for XGBoostClassifier"""
    return _XGBC_HYPERPARAMS
