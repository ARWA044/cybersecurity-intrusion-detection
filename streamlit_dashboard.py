import pandas as pd
import streamlit as st
import plotly.express as px
from pipeline import FEATURES, NUMERIC, CATEGORICAL, TARGET, train_models, predict

st.set_page_config(page_title="Cybersecurity Intrusion Detection", page_icon="🛡️", layout="wide")
st.title("🛡️ Cybersecurity Intrusion Detection")
st.caption("Experimental offline classification — not a production network monitor.")
st.info("Upload an authorized labeled CSV. No dataset is bundled; avoid uploading confidential logs.")
upload = st.file_uploader("Labeled CSV", type=["csv"])
if upload is None:
    st.stop()
if upload.size > 20 * 1024 * 1024:
    st.error("Maximum upload size is 20 MiB.")
    st.stop()
try:
    df = pd.read_csv(upload, keep_default_na=False)
except (ValueError, UnicodeError, pd.errors.ParserError):
    st.error("Invalid CSV.")
    st.stop()
st.write("Required columns:", ", ".join(FEATURES + [TARGET]))
if not set(FEATURES + [TARGET]).issubset(df.columns):
    st.error("CSV schema does not match the required columns.")
    st.stop()
import hashlib
key = hashlib.sha256(upload.getvalue()).hexdigest()
if st.session_state.get("dataset_key") != key:
    st.session_state.pop("bundle", None)
    st.session_state["dataset_key"] = key
if st.button("Train and evaluate models"):
    try:
        with st.spinner("Training on the training split only..."):
            st.session_state["bundle"] = train_models(df)
    except (ValueError, TypeError, KeyError) as exc:
        st.error(str(exc))
        st.stop()
bundle = st.session_state.get("bundle")
if bundle is None:
    st.stop()
st.subheader("Held-out evaluation")
st.caption(f"Untouched test rows: {bundle['test_size']}. Results are dataset-specific.")
table = pd.DataFrame(bundle["metrics"]).T
st.dataframe(table)
st.plotly_chart(px.bar(table.reset_index(), x="index", y="F1-score", labels={"index": "Model"}))
st.subheader("Evaluate a new observation")
with st.form("prediction"):
    row = {}
    for name in NUMERIC:
        row[name] = st.number_input(name, min_value=0.0, value=0.0)
    for name in CATEGORICAL:
        row[name] = st.selectbox(name, sorted(df[name].astype(str).unique()))
    submitted = st.form_submit_button("Predict")
if submitted:
    results = predict(bundle, pd.DataFrame([row]))
    st.dataframe(pd.DataFrame([{"Model": name, "Prediction": int(labels[0]),
        "Score": float(scores[0]), "Score type": "Reconstruction error" if name == "Autoencoder" else "Uncalibrated class probability"}
        for name, (labels, scores) in results.items()]))
    st.caption("1 = suspected attack; 0 = normal prediction. Neither establishes a confirmed incident or security guarantee.")
