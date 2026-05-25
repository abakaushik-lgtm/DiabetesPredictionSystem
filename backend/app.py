"""Backend API for the Diabetes Prediction System using FastAPI."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from fastapi import FastAPI, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from pydantic import BaseModel, Field
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

FEATURE_COLUMNS = [
    "electromagnetic_field_intensity",
    "quantum_spin_coherence",
    "particle_density",
    "local_gravitational_force",
    "age",
]
TARGET_COLUMN = "electromagnetic_frequency"
RANDOM_SEED = 42


@dataclass
class DiabetesModel:
    regressor: RandomForestRegressor
    scaler: StandardScaler
    trained: bool = False


class PredictionInput(BaseModel):
    electromagnetic_field_intensity: float = Field(..., ge=0.0, le=20.0)
    quantum_spin_coherence: float = Field(..., ge=10.0, le=100.0)
    particle_density: float = Field(..., ge=0.1, le=35.0)
    local_gravitational_force: float = Field(..., ge=0.0, le=20.0)
    age: float = Field(..., ge=1.0, le=120.0)


app = FastAPI(title="Diabetes Prediction System API")
model: DiabetesModel | None = None
summary_data: Dict[str, float] | None = None
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
VALID_USERS = {"admin": "password123"}


def generate_synthetic_data(n_samples: int = 2000, random_seed: int = RANDOM_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(random_seed)
    electromagnetic_field_intensity = rng.uniform(0.1, 15.0, size=n_samples)
    quantum_spin_coherence = rng.uniform(20.0, 100.0, size=n_samples)
    particle_density = rng.uniform(0.5, 25.0, size=n_samples)
    local_gravitational_force = rng.choice(
        [9.81, 3.71, 1.62, 0.0], size=n_samples, p=[0.55, 0.20, 0.15, 0.10]
    )
    age = rng.uniform(1.0, 120.0, size=n_samples)

    gravity_penalty = local_gravitational_force * (1 + 0.03 * particle_density)
    frequency_signal = (
        0.7 * electromagnetic_field_intensity
        + 0.2 * (100 - quantum_spin_coherence)
        + 0.25 * particle_density
        + gravity_penalty
        + 0.05 * age
    )

    electromagnetic_frequency = (
        frequency_signal
        + 5.0 * np.sin(electromagnetic_field_intensity / 3.2)
        - 0.4 * np.log1p(quantum_spin_coherence)
        + rng.normal(scale=1.5, size=n_samples)
    )

    return pd.DataFrame(
        {
            "electromagnetic_field_intensity": electromagnetic_field_intensity,
            "quantum_spin_coherence": quantum_spin_coherence,
            "particle_density": particle_density,
            "local_gravitational_force": local_gravitational_force,
            "age": age,
            "target_acceleration": np.zeros(n_samples),
            "electromagnetic_frequency": electromagnetic_frequency,
        }
    )


def preprocess_data(data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, StandardScaler, pd.DataFrame]:
    cleaned = data.copy()
    medians = cleaned[FEATURE_COLUMNS].median()
    cleaned[FEATURE_COLUMNS] = cleaned[FEATURE_COLUMNS].fillna(medians)

    clipping_bounds = {
        "electromagnetic_field_intensity": (0.05, 20.0),
        "quantum_spin_coherence": (10.0, 100.0),
        "particle_density": (0.1, 35.0),
        "local_gravitational_force": (0.0, 20.0),
        "age": (1.0, 120.0),
    }
    for column, (low, high) in clipping_bounds.items():
        cleaned[column] = cleaned[column].clip(lower=low, upper=high)

    features = cleaned[FEATURE_COLUMNS].values
    target = cleaned[TARGET_COLUMN].values
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    return features_scaled, target, scaler, cleaned


def build_regressor(random_seed: int = RANDOM_SEED) -> RandomForestRegressor:
    return RandomForestRegressor(
        n_estimators=100,
        max_depth=12,
        min_samples_leaf=4,
        random_state=random_seed,
        n_jobs=-1,
    )


def train_model(features: np.ndarray, target: np.ndarray, scaler: StandardScaler) -> DiabetesModel:
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=RANDOM_SEED
    )
    regressor = build_regressor()
    regressor.fit(X_train, y_train)
    return DiabetesModel(regressor=regressor, scaler=scaler, trained=True)


def predict_frequency(input_data: PredictionInput) -> float:
    if model is None or not model.trained:
        raise RuntimeError("Model is not trained.")
    features = np.array(
        [[
            input_data.electromagnetic_field_intensity,
            input_data.quantum_spin_coherence,
            input_data.particle_density,
            input_data.local_gravitational_force,
            input_data.age,
        ]]
    )
    scaled = model.scaler.transform(features)
    return float(model.regressor.predict(scaled)[0])


def deploy_anti_gravity_adjustment(gravity_value: float) -> Dict[str, float]:
    if model is None or not model.trained:
        raise RuntimeError("Model is not trained.")
    baseline_features = np.array([[7.5, 85.0, 12.0, gravity_value, 45.0]])
    baseline_scaled = model.scaler.transform(baseline_features)
    predicted_frequency = float(model.regressor.predict(baseline_scaled)[0])
    return {
        "gravity_source": gravity_value,
        "predicted_electromagnetic_frequency": predicted_frequency,
        "recommended_field_intensity": round(max(0.0, 0.7 * predicted_frequency), 3),
        "recommended_spin_coherence": round(min(100.0, 80.0 + 0.15 * (100 - gravity_value)), 3),
        "recommended_particle_density": round(max(0.1, 10.0 + 0.2 * gravity_value), 3),
    }


@app.get("/")
async def root_redirect():
    return RedirectResponse(url="/login")


@app.get("/index.html", response_class=HTMLResponse)
async def index_page() -> str:
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Index page not found")
    return index_path.read_text(encoding="utf-8")


@app.get("/style.css")
async def style_css():
    css_path = FRONTEND_DIR / "style.css"
    if not css_path.exists():
        raise HTTPException(status_code=404, detail="CSS file not found")
    return FileResponse(css_path, media_type="text/css")


@app.get("/script.js")
async def script_js():
    js_path = FRONTEND_DIR / "script.js"
    if not js_path.exists():
        raise HTTPException(status_code=404, detail="JavaScript file not found")
    return FileResponse(js_path, media_type="application/javascript")


@app.get("/login", response_class=HTMLResponse)
async def login_page() -> str:
    login_path = FRONTEND_DIR / "login.html"
    if not login_path.exists():
        raise HTTPException(status_code=404, detail="Login page not found")
    return login_path.read_text(encoding="utf-8")


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)) -> Dict[str, str]:
    if VALID_USERS.get(username) == password:
        return {"status": "success", "message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")


@app.on_event("startup")
async def startup_event() -> None:
    global model, summary_data
    data = generate_synthetic_data()
    features_scaled, target, scaler, cleaned_data = preprocess_data(data)
    model = train_model(features_scaled, target, scaler)
    summary_data = {
        "rows": float(cleaned_data.shape[0]),
        "columns": float(cleaned_data.shape[1]),
        "mean_intensity": float(cleaned_data["electromagnetic_field_intensity"].mean()),
        "mean_coherence": float(cleaned_data["quantum_spin_coherence"].mean()),
        "mean_density": float(cleaned_data["particle_density"].mean()),
    }


@app.get("/status")
async def status() -> Dict[str, str]:
    return {"status": "ready", "model_trained": "yes" if model and model.trained else "no"}


@app.get("/summary")
async def summary() -> Dict[str, float]:
    if summary_data is None:
        raise HTTPException(status_code=503, detail="Summary is not available")
    return summary_data


@app.post("/predict")
async def predict(input_data: PredictionInput) -> Dict[str, float]:
    try:
        prediction = predict_frequency(input_data)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    return {"predicted_electromagnetic_frequency": round(prediction, 4)}


@app.get("/deploy")
async def deploy(gravity: float = Query(9.81, ge=0.0, le=20.0)) -> Dict[str, float]:
    try:
        return deploy_anti_gravity_adjustment(gravity)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
