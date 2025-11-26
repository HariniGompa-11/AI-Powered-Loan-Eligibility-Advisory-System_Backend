from pydantic import BaseModel, Field, Json
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

class PredictionBase(BaseModel):
    input_json: Dict[str, Any] = Field(..., description="Input data in JSON format")
    bank_name: Optional[str] = Field("Unknown", description="Name of the bank")

class PredictionCreate(PredictionBase):
    pass

class PredictionUpdate(BaseModel):
    eligible: Optional[bool] = None
    probability: Optional[float] = None
    shap_json: Optional[Dict[str, Any]] = None
    recommendation_text: Optional[str] = None
    bank_name: Optional[str] = None

class PredictionInDBBase(PredictionBase):
    id: UUID
    user_id: UUID
    eligible: bool = Field(..., description="Whether the prediction is eligible")
    probability: float = Field(..., ge=0.0, le=1.0, description="Prediction probability score")
    shap_json: Optional[Dict[str, Any]] = Field(None, description="SHAP values in JSON format")
    recommendation_text: Optional[str] = Field(None, description="Generated recommendation text")
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {UUID: str}

class Prediction(PredictionInDBBase):
    pass

class PredictionInDB(PredictionInDBBase):
    pass
