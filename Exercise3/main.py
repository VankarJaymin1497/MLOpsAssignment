import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Load the saved model
model = joblib.load("model/model.pkl")

class PredictionRequest(BaseModel):
    features: dict

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        # Convert the features dict to a DataFrame
        df = pd.DataFrame([request.features])
        
        # Make prediction
        prediction = model.predict(df)
        result = "Malignant" if prediction[0] == 1 else "Benign"
        return {"prediction": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
