from fastapi import APIRouter

router = APIRouter()

@router.post("/predict")
async def predict():
    return {"message": "Prediction endpoint"}
