from typing import Optional

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def welcome():
    return {"Hello": "World"}

# Load data 
# Make prediction
# Get model version 