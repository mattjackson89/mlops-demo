import os
import mlflow
from fastapi import FastAPI, File, UploadFile
import numpy as np
import logging
from PIL import Image
from io import BytesIO

app = FastAPI()
model = mlflow.keras.load_model("models/latest")

logging.basicConfig(format="%(levelname)s:%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S", level="INFO")

@app.get("/")
def welcome():
    """Say hello."""
    return {"message:": "Welcome to the MLOps Demo!"}

@app.get("/models/")
def get_models():
    """Return a list of all avaliable models."""
    versions = [v for v in os.listdir("./models/") if v not in ["latest", "latest.txt"]]
    return {"avaliable_models": versions}

@app.get("/deployed_version/")
def get_deployed_version():
    """Returns the deployed model version according to latest.txt."""

    with open("models/latest.txt", "r") as df:
        version = df.read().strip()
    
    return {"version": version}

@app.post("/predict/")
def predict_rings(image: UploadFile = File(...)):
    """Upload an image and make a prediction."""

    # Load and reshape the image for prediction
    # Expecting (-1, 300, 300, 3)
    image_data = np.array(Image.open(BytesIO(image.file.read())))
    image_data = np.reshape(image_data, (-1, 300, 300, 3))

    # Make a prediction
    pred = model.predict(image_data)
    n_rings_pred = pred.argmax() + 1 # This should be dealt with better, it's ok for now. 
    
    return {"n_rings_pred": int(n_rings_pred)}

