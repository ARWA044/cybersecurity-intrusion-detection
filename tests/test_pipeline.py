import numpy as np
import pandas as pd
from pipeline import split_and_preprocess, train_models, predict, NUMERIC, CATEGORICAL, TARGET

def sample():
    rng = np.random.default_rng(42)
    data = {col: rng.uniform(0, 10, 80) for col in NUMERIC}
    data.update({col: ["A", "B"] * 40 for col in CATEGORICAL})
    data[TARGET] = [0] * 60 + [1] * 20
    return pd.DataFrame(data)

def test_preprocessing_and_holdout():
    data = sample()
    prep, train, test, y_train, y_test = split_and_preprocess(data)
    assert len(train) == 60 and len(test) == 20
    assert not set(y_train.index) & set(y_test.index)
    assert train.shape[1] == test.shape[1]
    assert prep.named_transformers_["num"].n_samples_seen_ == 60

def test_unknown_category_and_single_inference():
    data = sample()
    bundle = train_models(data, include_autoencoder=False)
    row = data.iloc[[0]].copy()
    row[CATEGORICAL[0]] = "unseen"
    result = predict(bundle, row)
    assert len(result) == 3
    assert all(len(labels) == 1 and 0 <= scores[0] <= 1 for labels, scores in result.values())
    assert all(0 <= values["ROC-AUC"] <= 1 for values in bundle["metrics"].values())
