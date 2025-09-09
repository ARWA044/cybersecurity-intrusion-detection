from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

def add_custom_features(df):
    df['login_success_ratio'] = df['login_attempts'] / (
        df['login_attempts'] + df['failed_logins'] + 1e-5
    )
    df['session_anomaly_score'] = df['session_duration'] * df['unusual_time_access']
    return df

def scale_features(df, feature_cols):
    scaler = StandardScaler()
    df[feature_cols] = scaler.fit_transform(df[feature_cols])
    return df

def balance_data(X, y):
    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_resample(X, y)
    return X_res, y_res
