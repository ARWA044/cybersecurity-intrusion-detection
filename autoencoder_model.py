from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
import numpy as np

def build_autoencoder(input_dim):
    # Encoder
    input_layer = Input(shape=(input_dim,))
    encoded = Dense(64, activation='relu')(input_layer)
    encoded = Dense(32, activation='relu')(encoded)
    encoded = Dense(16, activation='relu')(encoded)

    # Decoder
    decoded = Dense(32, activation='relu')(encoded)
    decoded = Dense(64, activation='relu')(decoded)
    decoded = Dense(input_dim, activation='linear')(decoded)

    autoencoder = Model(inputs=input_layer, outputs=decoded)
    autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    return autoencoder

def train_autoencoder(X_train, epochs=50, batch_size=32):
    autoencoder = build_autoencoder(X_train.shape[1])
    autoencoder.fit(X_train, X_train, epochs=epochs, batch_size=batch_size, shuffle=True, verbose=0)
    return autoencoder

def detect_anomalies(autoencoder, X, threshold=None):
    # Reconstruct the input
    X_pred = autoencoder.predict(X)
    mse = np.mean(np.power(X - X_pred, 2), axis=1)

    if threshold is None:
        # Set threshold as mean + 3*std deviation of reconstruction error
        threshold = np.mean(mse) + 3 * np.std(mse)

    # Flag as anomaly if reconstruction error > threshold
    y_pred = (mse > threshold).astype(int)
    return y_pred, threshold

