from data_processing import load_data, clean_data, encode_categorical
from feature_engineering import add_custom_features, scale_features, balance_data
from model_training import train_random_forest,train_xgboost
from evaluation import evaluate_model
from autoencoder_model import train_autoencoder, detect_anomalies
import pandas as pd

# Load
df = load_data("httpswww.kaggle.comdatasetsdnkumarscybersecurity-intrusion-detection-dataset.csv")

# Process
df = clean_data(df)
df = encode_categorical(df, ["protocol_type", "encryption_used", "browser_type"])
df = add_custom_features(df)

# Prepare
features = [col for col in df.columns if col != "attack_detected"]
X, y = df[features], df["attack_detected"]


id_columns = ["session_id"]  # Replace with your actual ID columns
X = X.drop(columns=id_columns, errors='ignore')


for col in X.select_dtypes(include=['object']).columns:
    X[col] = X[col].astype('category').cat.codes


X = scale_features(X, X.columns)


X, y = balance_data(X, y)


# train model

rf_model = train_random_forest(X, y)
xgb_model = train_xgboost(X, y)

rf_metrics = evaluate_model(rf_model, X, y)
xgb_metrics = evaluate_model(xgb_model, X, y)

# Autoencoder for Anomaly Detection 
autoencoder = train_autoencoder(X)
y_pred_ae, threshold = detect_anomalies(autoencoder, X)
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
autoencoder_metrics = {
    "Accuracy": accuracy_score(y, y_pred_ae),
    "Precision": precision_score(y, y_pred_ae),
    "Recall": recall_score(y, y_pred_ae),
    "F1-score": f1_score(y, y_pred_ae),
    "ROC-AUC": roc_auc_score(y, y_pred_ae)
}


table = pd.DataFrame([
    {"Model": "Random Forest", **rf_metrics},
    {"Model": "XGBoost", **xgb_metrics},
    {"Model": "Autoencoder", **autoencoder_metrics}

])
print(table)