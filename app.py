"""FastAPI service for the Student Result Prediction model."""
from pathlib import Path
from typing import Annotated
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "student_result_model.pkl"
FEATURES = ["attendance", "internal_marks", "assignment_marks", "previous_score"]
app = FastAPI(title="Student Result Prediction API", version="1.0.0")
_model = None

class PredictionRequest(BaseModel):
    attendance: float = Field(ge=0, le=100)
    internal_marks: float = Field(ge=0, le=100)
    assignment_marks: float = Field(ge=0, le=100)
    previous_score: float = Field(ge=0, le=100)

def load_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError("Model artifact missing.")
        _model = joblib.load(MODEL_PATH)
    return _model

@app.get("/")
def index():
    return {"service": "student-result-prediction", "status": "running"}

@app.get("/health")
def health():
    try:
        load_model()
        return {"status": "healthy"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Model unavailable: {exc}")

@app.post("/predict")
def predict(payload: PredictionRequest):
    values = payload.model_dump()
    prediction = int(load_model().predict(pd.DataFrame([values], columns=FEATURES))[0])
    return {"prediction": "PASS" if prediction == 1 else "FAIL", "prediction_code": prediction}
