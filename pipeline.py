"""Shared training and inference pipeline for an experimental binary IDS."""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from imblearn.over_sampling import RandomOverSampler
from xgboost import XGBClassifier

NUMERIC = ["network_packet_size", "session_duration", "login_attempts", "failed_logins",
           "unusual_time_access", "ip_reputation_score"]
CATEGORICAL = ["protocol_type", "encryption_used", "browser_type"]
FEATURES = NUMERIC + CATEGORICAL
TARGET = "attack_detected"

def prepare_features(df):
    missing = set(FEATURES) - set(df.columns)
    if missing:
        raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
    x = df[FEATURES].copy()
    for col in NUMERIC:
        x[col] = pd.to_numeric(x[col], errors="raise")
    if not np.isfinite(x[NUMERIC].to_numpy(dtype=float)).all():
        raise ValueError("Numeric features must be finite")
    if x[CATEGORICAL].isna().any().any():
        raise ValueError("Missing categorical values")
    x[CATEGORICAL] = x[CATEGORICAL].astype(str)
    x["login_success_ratio"] = x["login_attempts"] / (x["login_attempts"] + x["failed_logins"] + 1e-5)
    x["session_anomaly_score"] = x["session_duration"] * x["unusual_time_access"]
    return x

def split_and_preprocess(df):
    x = prepare_features(df)
    y = pd.to_numeric(df[TARGET], errors="raise")
    if set(y.unique()) != {0, 1} or y.value_counts().min() < 5:
        raise ValueError("Dataset needs both binary labels with at least five rows each")
    y = y.astype(int)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y)
    prep = ColumnTransformer([
        ("num", StandardScaler(), NUMERIC + ["login_success_ratio", "session_anomaly_score"]),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL),
    ])
    return prep, prep.fit_transform(x_train), prep.transform(x_test), y_train, y_test

def metrics(y, predictions, scores):
    return {"Accuracy": accuracy_score(y, predictions),
            "Precision": precision_score(y, predictions, zero_division=0),
            "Recall": recall_score(y, predictions, zero_division=0),
            "F1-score": f1_score(y, predictions, zero_division=0),
            "ROC-AUC": roc_auc_score(y, scores)}

def train_models(df, include_autoencoder=True):
    prep, train, test, y_train, y_test = split_and_preprocess(df)
    # Duplicate minority training rows rather than interpolating one-hot categories.
    balanced, labels = RandomOverSampler(random_state=42).fit_resample(train, y_train)
    models = {"Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
              "XGBoost": XGBClassifier(random_state=42, eval_metric="logloss", n_jobs=2),
              "Logistic Regression": LogisticRegression(max_iter=1000)}
    results = {}
    for name, model in models.items():
        model.fit(balanced, labels)
        results[name] = metrics(y_test, model.predict(test), model.predict_proba(test)[:, 1])
    ae = threshold = None
    if include_autoencoder:
        from autoencoder_model import train_autoencoder
        from tensorflow.keras.utils import set_random_seed
        set_random_seed(42)
        normal = train[y_train.to_numpy() == 0]
        ae = train_autoencoder(normal, epochs=20)
        threshold = float(np.quantile(reconstruction_errors(ae, normal), 0.99))
        errors = reconstruction_errors(ae, test)
        results["Autoencoder"] = metrics(y_test, errors > threshold, errors)
    return {"preprocessor": prep, "models": models, "autoencoder": ae,
            "threshold": threshold, "metrics": results, "test_size": len(test),
            "test_labels": y_test, "test_features": test}

def reconstruction_errors(model, x):
    return np.mean((x - model.predict(x, verbose=0)) ** 2, axis=1)

def predict(bundle, df):
    x = bundle["preprocessor"].transform(prepare_features(df))
    result = {}
    for name, model in bundle["models"].items():
        result[name] = (model.predict(x), model.predict_proba(x)[:, 1])
    if bundle["autoencoder"] is not None:
        errors = reconstruction_errors(bundle["autoencoder"], x)
        result["Autoencoder"] = ((errors > bundle["threshold"]).astype(int), errors)
    return result
