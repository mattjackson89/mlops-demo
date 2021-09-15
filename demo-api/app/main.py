import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def welcome():
    return {"Hello": "World"}

@app.get("/models")
def get_models():
    return os.listdir("./models/")

# Make prediction
# Get model version 