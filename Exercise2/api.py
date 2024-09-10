# api.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Load the pre-trained model (ensure the model is saved from step 2)
model = joblib.load('Exercise2model.pkl')

# Input data schema for model prediction 
class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "Model API is up and running!"}

# Prediction endpoint
@app.post("/predict/")
def predict_species(iris: IrisData):
    # Convert input data to numpy array
    data = np.array([[iris.sepal_length, iris.sepal_width, iris.petal_length, iris.petal_width]])

    # Make prediction using the loaded model
    prediction = model.predict(data)

    # Map prediction to iris species
    species = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}
    result = species[int(prediction[0])]

    return {"prediction": result}