from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from model.predict import Predictor
app = FastAPI(title='AI Prioritizer')
predictor = Predictor()

class Finding(BaseModel):
    id: Optional[str]
    asset: str
    asset_criticality: str
    cvss: float
    summary: str
    description: str
    remediation: Optional[str]

class Prediction(BaseModel):
    id: Optional[str]
    score: float
    priority: str
    explanation: dict

@app.post('/predict', response_model=Prediction)
def predict(f: Finding):
    row = f.dict()
    res = predictor.predict_single(row)
    return res

@app.post('/batch_predict')
def batch_predict(items: List[Finding]):
    rows = [i.dict() for i in items]
    res = predictor.predict_batch(rows)
    return res
