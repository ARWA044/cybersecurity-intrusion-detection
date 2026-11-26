# 🛡️ Cybersecurity Intrusion Detection System

Experimental offline binary intrusion classification with Python, scikit-learn, XGBoost, TensorFlow and Streamlit. This is a learning prototype, not a live IDS or a validated security product.

## Quick start

Use Python 3.12 and activate a virtual environment.

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_dashboard.py
```

Upload an authorized labeled CSV. No dataset is bundled. Required columns:

```text
network_packet_size,session_duration,login_attempts,failed_logins,unusual_time_access,ip_reputation_score,protocol_type,encryption_used,browser_type,attack_detected
```

Labels: 0 normal, 1 suspected attack ground truth. Use at least five rows of each class. Numeric fields must be finite. Obtain the dataset lawfully and document its origin and license.

Alternatively: `python main.py path/to/dataset.csv`.

## Evaluation architecture

1. Engineer deterministic features and split into stratified training and holdout partitions.
2. Fit scaling and one-hot encoding on training rows only; reuse for holdout and inference.
3. Oversample only supervised training rows with random duplication, avoiding synthetic fractional categorical values.
4. Train Random Forest, XGBoost and Logistic Regression; train an autoencoder on normal training rows only.
5. Set the autoencoder threshold from normal training reconstruction errors (99th percentile).
6. Evaluate untouched holdout rows with accuracy, precision, recall, F1 and ROC-AUC using continuous scores.

The random row split assumes independent rows; use session/group/time-based splits where appropriate. The autoencoder threshold is in-sample and needs separate calibration for stronger validation. Scores are not calibrated security probabilities. Do not upload sensitive logs to a public deployment.

## Tests

```bash
python -m pip install pytest
python -m pytest -q tests
```

CI covers preprocessing and supervised-model inference with synthetic fixtures, not full TensorFlow training or operational accuracy.

## License

[MIT](LICENSE)
