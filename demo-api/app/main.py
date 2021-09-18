import os
import mlflow
from fastapi import FastAPI

app = FastAPI()
model = mlflow.keras.load_model("models/latest")

@app.get("/")
def welcome():
    return {"Hello": "World"}

@app.get("/models")
def get_models():
    return os.listdir("./models/")

@app.get("/check_latest")
def get_models():
    return str(model.layers)

# Make prediction
# Get model version 