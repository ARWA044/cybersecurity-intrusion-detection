import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.model_selection import train_test_split
import joblib
import os
from datetime import datetime, timedelta
import warnings
import tensorflow as tf

# Suppress TensorFlow warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('ERROR')

# Import existing modules
from data_processing import load_data, clean_data, encode_categorical
from feature_engineering import add_custom_features, scale_features, balance_data
from model_training import train_random_forest, train_xgboost, train_logistic_regression
from evaluation import evaluate_model
from autoencoder_model import train_autoencoder, detect_anomalies

# Page configuration
st.set_page_config(
    page_title="Cybersecurity Intrusion Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .alert-box {
        background-color: #ffebee;
        border: 1px solid #f44336;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e8;
        border: 1px solid #4caf50;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e3f2fd;
        border: 1px solid #2196f3;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🛡️ Cybersecurity Intrusion Detection System</h1>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page",
    ["🏠 Dashboard", "🔍 Test New Data", "📊 Model Performance"]
)

# Cache functions for better performance
@st.cache_data
def load_and_process_data():
    """Load and process the cybersecurity dataset"""
    try:
        df = load_data("httpswww.kaggle.comdatasetsdnkumarscybersecurity-intrusion-detection-dataset.csv")
        df = clean_data(df)
        df = encode_categorical(df, ["protocol_type", "encryption_used", "browser_type"])
        df = add_custom_features(df)
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

@st.cache_data
def train_models(df):
    """Train all models and return results"""
    try:
        # Prepare features
        features = [col for col in df.columns if col != "attack_detected"]
        X, y = df[features], df["attack_detected"]
        
        # Remove ID columns
        id_columns = ["session_id"]
        X = X.drop(columns=id_columns, errors='ignore')
        
        # Handle categorical columns
        for col in X.select_dtypes(include=['object']).columns:
            X[col] = X[col].astype('category').cat.codes
        
        # Scale features
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
        
        # Balance data
        X, y = balance_data(X, y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train models
        rf_model = train_random_forest(X_train, y_train)
        xgb_model = train_xgboost(X_train, y_train)
        lr_model = train_logistic_regression(X_train, y_train)
        autoencoder = train_autoencoder(X_train, epochs=20, batch_size=32)
        
        # Evaluate models
        rf_metrics = evaluate_model(rf_model, X_test, y_test)
        xgb_metrics = evaluate_model(xgb_model, X_test, y_test)
        lr_metrics = evaluate_model(lr_model, X_test, y_test)
        
        # Autoencoder evaluation
        y_pred_ae, threshold = detect_anomalies(autoencoder, X_test)
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
        autoencoder_metrics = {
            "Accuracy": accuracy_score(y_test, y_pred_ae),
            "Precision": precision_score(y_test, y_pred_ae),
            "Recall": recall_score(y_test, y_pred_ae),
            "F1-score": f1_score(y_test, y_pred_ae),
            "ROC-AUC": roc_auc_score(y_test, y_pred_ae)
        }
        
        return {
            'models': {'rf': rf_model, 'xgb': xgb_model, 'lr': lr_model, 'autoencoder': autoencoder},
            'metrics': {'rf': rf_metrics, 'xgb': xgb_metrics, 'lr': lr_metrics, 'autoencoder': autoencoder_metrics},
            'data': {'X_test': X_test, 'y_test': y_test, 'X_train': X_train, 'y_train': y_train},
            'scaler': scaler
        }
    except Exception as e:
        st.error(f"Error training models: {str(e)}")
        return None

# Load data
if 'data' not in st.session_state:
    with st.spinner('Loading and processing data...'):
        st.session_state.data = load_and_process_data()

if st.session_state.data is not None:
    df = st.session_state.data
    
    # Train models if not already done
    if 'models' not in st.session_state:
        with st.spinner('Training models...'):
            st.session_state.models = train_models(df)

# Page content
if page == "🏠 Dashboard":
    st.header("System Overview")
    
    if st.session_state.data is not None and st.session_state.models is not None:
        # Key metrics in a simple layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Records", f"{len(df):,}")
        
        with col2:
            attack_rate = df['attack_detected'].mean() * 100
            st.metric("Attack Rate", f"{attack_rate:.1f}%")
        
        with col3:
            best_model = max(st.session_state.models['metrics'].items(), key=lambda x: x[1]['F1-score'])
            st.metric("Best Model", best_model[0].upper())
        
        # Simple attack distribution chart
        st.subheader("Attack Distribution")
        target_counts = df['attack_detected'].value_counts()
        fig = px.pie(values=target_counts.values, names=['Normal', 'Attack'], 
                     title="Normal vs Attack Distribution")
        st.plotly_chart(fig, use_container_width=True)
        
        # System status
        st.subheader("System Status")
        if attack_rate > 20:
            st.markdown('<div class="alert-box">⚠️ High attack rate detected! Consider reviewing security measures.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-box">✅ System security status is normal.</div>', unsafe_allow_html=True)
        
        # Quick model performance summary
        st.subheader("Model Performance Summary")
        metrics = st.session_state.models['metrics']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Random Forest", f"{metrics['rf']['Accuracy']:.3f}", "Accuracy")
        
        with col2:
            st.metric("XGBoost", f"{metrics['xgb']['Accuracy']:.3f}", "Accuracy")
        
        with col3:
            st.metric("Logistic Regression", f"{metrics['lr']['Accuracy']:.3f}", "Accuracy")
        
        with col4:
            st.metric("Autoencoder", f"{metrics['autoencoder']['Accuracy']:.3f}", "Accuracy")
    
    else:
        st.error("Unable to load data. Please check your data file.")

elif page == "🔍 Test New Data":
    st.header("Test New Data for Intrusions")
    
    if st.session_state.models is not None:
        st.markdown('<div class="info-box">📝 Enter network and security features below to test for potential intrusions.</div>', unsafe_allow_html=True)
        
        # Simple input form
        with st.form("detection_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Network Features**")
                network_packet_size = st.number_input("Network Packet Size", min_value=0, value=500, help="Size of network packets in bytes")
                session_duration = st.number_input("Session Duration (minutes)", min_value=0.0, value=30.0, help="How long the session lasted")
                login_attempts = st.number_input("Login Attempts", min_value=0, value=5, help="Number of login attempts")
                failed_logins = st.number_input("Failed Logins", min_value=0, value=1, help="Number of failed login attempts")
                unusual_time_access = st.slider("Unusual Time Access", 0.0, 1.0, 0.1, help="Score indicating if access time is unusual (0=normal, 1=very unusual)")
            
            with col2:
                st.write("**Security Features**")
                protocol_type = st.selectbox("Protocol Type", ["TCP", "UDP", "ICMP"], help="Network protocol used")
                encryption_used = st.selectbox("Encryption Used", ["DES", "AES", "None"], help="Type of encryption used")
                browser_type = st.selectbox("Browser Type", ["Chrome", "Firefox", "Safari", "Edge", "Unknown"], help="Browser used for access")
                ip_reputation_score = st.slider("IP Reputation Score", 0.0, 1.0, 0.5, help="Reputation score of the IP address (0=bad, 1=good)")
            
            submitted = st.form_submit_button("🔍 Detect Intrusion", use_container_width=True)
        
        if submitted:
            # Create input data
            input_data = {
                'session_id': 'TEST_001',
                'network_packet_size': network_packet_size,
                'protocol_type': protocol_type,
                'login_attempts': login_attempts,
                'session_duration': session_duration,
                'encryption_used': encryption_used,
                'ip_reputation_score': ip_reputation_score,
                'failed_logins': failed_logins,
                'browser_type': browser_type,
                'unusual_time_access': unusual_time_access,
                'attack_detected': 0
            }
            
            # Process input data
            input_df = pd.DataFrame([input_data])
            features = [col for col in input_df.columns if col != "attack_detected"]
            X_input = input_df[features]
            
            # Remove ID columns
            id_columns = ["session_id"]
            X_input = X_input.drop(columns=id_columns, errors='ignore')
            
            # Handle categorical columns
            for col in X_input.select_dtypes(include=['object']).columns:
                X_input[col] = X_input[col].astype('category').cat.codes
            
            # Add custom features
            X_input = add_custom_features(X_input)
            
            # Scale features using the same scaler from training
            scaler = st.session_state.models['scaler']
            X_input_scaled = scaler.transform(X_input)
            X_input = pd.DataFrame(X_input_scaled, columns=X_input.columns, index=X_input.index)
            
            # Make predictions
            models = st.session_state.models['models']
            
            st.subheader("Detection Results")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                rf_pred = models['rf'].predict(X_input)[0]
                rf_proba = models['rf'].predict_proba(X_input)[0]
                st.metric("Random Forest", "🚨 Attack" if rf_pred else "✅ Normal", f"{rf_proba[1]*100:.1f}%")
            
            with col2:
                xgb_pred = models['xgb'].predict(X_input)[0]
                xgb_proba = models['xgb'].predict_proba(X_input)[0]
                st.metric("XGBoost", "🚨 Attack" if xgb_pred else "✅ Normal", f"{xgb_proba[1]*100:.1f}%")
            
            with col3:
                lr_pred = models['lr'].predict(X_input)[0]
                lr_proba = models['lr'].predict_proba(X_input)[0]
                st.metric("Logistic Regression", "🚨 Attack" if lr_pred else "✅ Normal", f"{lr_proba[1]*100:.1f}%")
            
            with col4:
                ae_pred, ae_threshold = detect_anomalies(models['autoencoder'], X_input)
                X_pred = models['autoencoder'].predict(X_input)
                mse = np.mean(np.power(X_input - X_pred, 2), axis=1)[0]
                confidence = min(100, max(0, (mse / ae_threshold) * 50))
                st.metric("Autoencoder", "🚨 Attack" if ae_pred[0] else "✅ Normal", f"{confidence:.1f}%")
            
            # Overall prediction
            predictions = [rf_pred, xgb_pred, lr_pred, ae_pred[0]]
            attack_votes = sum(predictions)
            
            st.subheader("Overall Assessment")
            if attack_votes >= 2:
                st.markdown('<div class="alert-box">🚨 INTRUSION DETECTED! Multiple models indicate a potential security threat. Immediate action recommended.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-box">✅ No intrusion detected. System appears secure.</div>', unsafe_allow_html=True)
            
            # Show detailed results
            st.subheader("Detailed Analysis")
            results_df = pd.DataFrame({
                'Model': ['Random Forest', 'XGBoost', 'Logistic Regression', 'Autoencoder'],
                'Prediction': ['Attack' if p else 'Normal' for p in predictions],
                'Confidence': [f"{rf_proba[1]*100:.1f}%", f"{xgb_proba[1]*100:.1f}%", f"{lr_proba[1]*100:.1f}%", f"{confidence:.1f}%"]
            })
            st.dataframe(results_df, use_container_width=True)

elif page == "📊 Model Performance":
    st.header("Model Performance Comparison")
    
    if st.session_state.models is not None:
        models = st.session_state.models['models']
        metrics = st.session_state.models['metrics']
        
        # Simple performance table
        st.subheader("Model Accuracy Comparison")
        comparison_data = []
        for model_name, model_metrics in metrics.items():
            comparison_data.append({
                'Model': model_name.upper(),
                'Accuracy': f"{model_metrics['Accuracy']:.3f}",
                'Precision': f"{model_metrics['Precision']:.3f}",
                'Recall': f"{model_metrics['Recall']:.3f}",
                'F1-Score': f"{model_metrics['F1-score']:.3f}"
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        # Simple bar chart
        st.subheader("Model Performance Chart")
        fig = px.bar(comparison_df, x='Model', y='Accuracy', title="Model Accuracy Comparison")
        st.plotly_chart(fig, use_container_width=True)
        
        # Confusion matrix for best model
        st.subheader("Confusion Matrix (Best Model)")
        best_model_name = max(metrics.items(), key=lambda x: x[1]['F1-score'])[0]
        best_model = models[best_model_name]
        
        X_test = st.session_state.models['data']['X_test']
        y_test = st.session_state.models['data']['y_test']
        
        if best_model_name != 'autoencoder':
            y_pred = best_model.predict(X_test)
            cm = confusion_matrix(y_test, y_pred)
            
            fig = px.imshow(cm, text_auto=True, aspect="auto", 
                           title=f"{best_model_name.upper()} Confusion Matrix",
                           labels=dict(x="Predicted", y="Actual"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Autoencoder confusion matrix not available in this simplified view.")

# Footer
st.markdown("---")
st.markdown("🛡️ **Cybersecurity Intrusion Detection System** | Built with Streamlit")