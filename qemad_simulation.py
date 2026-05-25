"""Quantum Electro-Magnetic Antigravity Drive (QEMAD) Simulation Framework

This module simulates an advanced anti-gravity control pipeline with
synthetic environmental physics data, robust preprocessing, machine learning
optimization, and deployment hooks for dynamic hover stabilization.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# ---------------------------------------------------------------------------
# Configuration and runtime constants
# ---------------------------------------------------------------------------

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

RANDOM_SEED = 42
N_SAMPLES = 2000
FEATURE_COLUMNS = [
    "electromagnetic_field_intensity",
    "quantum_spin_coherence",
    "particle_density",
    "local_gravitational_force",
]
TARGET_COLUMN = "electromagnetic_frequency"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class QEMADModel:
    regressor: RandomForestRegressor
    scaler: StandardScaler
    trained: bool = False


# ---------------------------------------------------------------------------
# Physics engine: synthetic dataset generation
# ---------------------------------------------------------------------------


def generate_synthetic_qemad_data(n_samples: int = N_SAMPLES, random_seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Generate a synthetic quantum electromagnetic dataset for anti-gravity control."""
    rng = np.random.default_rng(random_seed)

    electromagnetic_field_intensity = rng.uniform(0.1, 15.0, size=n_samples)
    quantum_spin_coherence = rng.uniform(20.0, 100.0, size=n_samples)
    particle_density = rng.uniform(0.5, 25.0, size=n_samples)
    local_gravitational_force = rng.choice([9.81, 3.71, 1.62, 0.0], size=n_samples, p=[0.55, 0.20, 0.15, 0.10])

    # Use a physical-inspired formula to simulate the required anti-gravity frequency.
    # Higher coherence and field intensity reduce the frequency requirement.
    gravity_penalty = local_gravitational_force * (1 + 0.03 * particle_density)
    frequency_signal = (
        0.7 * electromagnetic_field_intensity
        + 0.2 * (100 - quantum_spin_coherence)
        + 0.25 * particle_density
        + gravity_penalty
    )

    # Add non-linear resonance effects and measurement noise.
    electromagnetic_frequency = (
        frequency_signal
        + 5.0 * np.sin(electromagnetic_field_intensity / 3.2)
        - 0.4 * np.log1p(quantum_spin_coherence)
        + rng.normal(scale=1.5, size=n_samples)
    )

    data = pd.DataFrame(
        {
            "electromagnetic_field_intensity": electromagnetic_field_intensity,
            "quantum_spin_coherence": quantum_spin_coherence,
            "particle_density": particle_density,
            "local_gravitational_force": local_gravitational_force,
            "target_acceleration": np.zeros(n_samples),
            "electromagnetic_frequency": electromagnetic_frequency,
        }
    )

    return data


def inject_sensor_glitches(data: pd.DataFrame, random_seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Inject missing values and extreme anomalies to emulate sensor glitching/noise."""
    rng = np.random.default_rng(random_seed)
    corrupted = data.copy()
    n_rows = len(corrupted)

    # Introduce random NaN values into the environmental metrics.
    for column in FEATURE_COLUMNS:
        nan_mask = rng.choice([False, True], size=n_rows, p=[0.93, 0.07])
        corrupted.loc[nan_mask, column] = np.nan

    # Introduce outliers for occasional sensor spikes.
    outlier_mask = rng.choice([False, True], size=n_rows, p=[0.96, 0.04])
    for column in FEATURE_COLUMNS:
        corrupted.loc[outlier_mask, column] *= rng.uniform(3.0, 10.0)

    # Add a few spike anomalies in target frequency to emulate physical resonance glitches.
    spike_mask = rng.choice([False, True], size=n_rows, p=[0.98, 0.02])
    corrupted.loc[spike_mask, TARGET_COLUMN] *= rng.uniform(0.5, 1.8)

    return corrupted


def preprocess_qemad_data(data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, StandardScaler, pd.DataFrame]:
    """Clean, impute, clip, and normalize the anti-gravity dataset."""
    cleaned = data.copy()

    logging.info("Starting data cleaning and preprocessing pipeline.")

    # Impute missing sensor values with robust medians.
    medians = cleaned[FEATURE_COLUMNS].median()
    cleaned[FEATURE_COLUMNS] = cleaned[FEATURE_COLUMNS].fillna(medians)

    # Clip extreme anomalies to physically plausible bounds.
    clipping_bounds = {
        "electromagnetic_field_intensity": (0.05, 20.0),
        "quantum_spin_coherence": (10.0, 100.0),
        "particle_density": (0.1, 35.0),
        "local_gravitational_force": (0.0, 20.0),
    }
    for column, (low, high) in clipping_bounds.items():
        cleaned[column] = cleaned[column].clip(lower=low, upper=high)

    features = cleaned[FEATURE_COLUMNS].values
    target = cleaned[TARGET_COLUMN].values

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    logging.info("Data preprocessing complete. Features standardized for model training.")
    return features_scaled, target, scaler, cleaned


# ---------------------------------------------------------------------------
# Model architecture: training and evaluation
# ---------------------------------------------------------------------------


def build_qemad_regressor(random_seed: int = RANDOM_SEED) -> RandomForestRegressor:
    """Construct a Random Forest Regressor for anti-gravity frequency estimation."""
    return RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        min_samples_leaf=4,
        random_state=random_seed,
        n_jobs=-1,
    )


def train_qemad_model(features: np.ndarray, target: np.ndarray, scaler: StandardScaler) -> QEMADModel:
    """Train the anti-gravity frequency predictor and return a model wrapper."""
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.20, random_state=RANDOM_SEED
    )

    regressor = build_qemad_regressor()
    regressor.fit(X_train, y_train)

    model = QEMADModel(regressor=regressor, scaler=scaler, trained=True)

    y_pred = regressor.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    logging.info("Model training complete.")
    logging.info("Validation Metrics: MSE=%.4f, R²=%.4f", mse, r2)

    return model


def evaluate_qemad_model(model: QEMADModel, features: np.ndarray, target: np.ndarray) -> Tuple[float, float]:
    """Evaluate the model on held-out data and return MSE and R^2 score."""
    predictions = model.regressor.predict(features)
    mse = mean_squared_error(target, predictions)
    r2 = r2_score(target, predictions)
    return mse, r2


def simulate_dynamic_hover_correction(model: QEMADModel, initial_force: float = 9.81, n_steps: int = 10) -> pd.DataFrame:
    """Simulate a dynamic hover loop that adjusts electromagnetic parameters over time."""
    rng = np.random.default_rng(RANDOM_SEED + 1)

    history = []
    current_acceleration = initial_force
    current_intensity = 5.0
    current_coherence = 75.0
    current_density = 8.0

    for step in range(n_steps):
        features = np.array(
            [[current_intensity, current_coherence, current_density, current_acceleration]]
        )
        features_scaled = model.scaler.transform(features)
        predicted_frequency = float(model.regressor.predict(features_scaled)[0])

        # Interpret the predicted frequency into field adjustments.
        intensity_adjustment = max(0.0, 0.25 * (predicted_frequency - current_intensity))
        coherence_adjustment = max(-5.0, min(5.0, 0.1 * (100 - current_coherence)))

        current_intensity += intensity_adjustment * 0.75
        current_coherence += coherence_adjustment
        current_density = max(0.1, current_density + rng.normal(scale=0.2))

        # Update the simulated acceleration after applying the anti-gravity field.
        current_acceleration = max(0.0, current_acceleration - 0.9 * intensity_adjustment + 0.05 * (100 - current_coherence))
        history.append(
            {
                "step": step + 1,
                "electromagnetic_field_intensity": current_intensity,
                "quantum_spin_coherence": current_coherence,
                "particle_density": current_density,
                "local_gravitational_force": initial_force,
                "predicted_electromagnetic_frequency": predicted_frequency,
                "residual_acceleration": current_acceleration,
            }
        )

    return pd.DataFrame(history)


def deploy_anti_gravity_adjustment(model: QEMADModel, gravity_value: float) -> dict:
    """Deploy a gravity-specific adjustment estimate for a target hover state."""
    if not model.trained:
        raise ValueError("Model has not been trained. Train the QEMAD model before deployment.")

    baseline_features = np.array(
        [[
            7.5,
            85.0,
            12.0,
            gravity_value,
        ]]
    )
    baseline_scaled = model.scaler.transform(baseline_features)
    predicted_frequency = float(model.regressor.predict(baseline_scaled)[0])

    return {
        "gravity_source": gravity_value,
        "predicted_electromagnetic_frequency": predicted_frequency,
        "recommended_field_intensity": round(max(0.0, 0.7 * predicted_frequency), 3),
        "recommended_spin_coherence": round(min(100.0, 80.0 + 0.15 * (100 - gravity_value)), 3),
        "recommended_particle_density": round(max(0.1, 10.0 + 0.2 * gravity_value), 3),
    }


def summarize_dataset(data: pd.DataFrame) -> None:
    """Print a brief summary of the synthetic QEMAD dataset."""
    logging.info("Dataset overview: %d rows, %d columns", data.shape[0], data.shape[1])
    logging.info("Feature means:\n%s", data[FEATURE_COLUMNS].mean().to_dict())
    logging.info("Feature std dev:\n%s", data[FEATURE_COLUMNS].std().to_dict())


# ---------------------------------------------------------------------------
# Main execution pipeline
# ---------------------------------------------------------------------------


def main() -> None:
    logging.info("Initializing QEMAD simulation pipeline.")

    data = generate_synthetic_qemad_data()
    corrupted_data = inject_sensor_glitches(data)
    summarize_dataset(corrupted_data)

    features_scaled, target, scaler, cleaned_data = preprocess_qemad_data(corrupted_data)
    model = train_qemad_model(features_scaled, target, scaler)

    test_features, test_target = features_scaled[:200], target[:200]
    mse, r2 = evaluate_qemad_model(model, test_features, test_target)
    logging.info("Final evaluation on sample test slice: MSE=%.4f, R²=%.4f", mse, r2)

    hover_simulation = simulate_dynamic_hover_correction(model=model, initial_force=9.81, n_steps=12)
    logging.info("Dynamic hover correction simulation complete.")
    logging.info("Hover simulation sample:\n%s", hover_simulation.head().to_string(index=False))

    earth_adjustment = deploy_anti_gravity_adjustment(model, gravity_value=9.81)
    mars_adjustment = deploy_anti_gravity_adjustment(model, gravity_value=3.71)

    logging.info("Deployment adjustment for Earth gravity: %s", earth_adjustment)
    logging.info("Deployment adjustment for Mars gravity: %s", mars_adjustment)
    logging.info("QEMAD simulation pipeline complete.")


if __name__ == "__main__":
    main()

    print("\nQEMAD model ready. Use deploy_anti_gravity_adjustment(model, gravity_value) for instant anti-gravity field parameters.")


if __name__ == "__main__":
    main()
