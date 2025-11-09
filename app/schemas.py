from pydantic import BaseModel
from typing import Optional, Dict

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
    explanation: Dict
