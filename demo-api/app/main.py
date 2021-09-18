import os
import mlflow
from fastapi import FastAPI, File, UploadFile
import logging
logging.basicConfig(format="%(levelname)s:%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S", level="INFO")

app = FastAPI()
model = mlflow.keras.load_model("models/latest")

@app.get("/")
def welcome():
    return "Welcome to the MLOps Demo!"

@app.get("/models/")
def get_models():
    logging.info("CHECK get_models")
    return os.listdir("./models/")

@app.post("/predict/")
def predict_rings(image: UploadFile = File(...)):
    logging.info("CHECK predict 1")
    logging.info(image.filename)
    image_data = np.array([plt.imread(image)])
    logging.info("CHECK predict 2")
    res = model.predict(image_data)
    logging.info("CHECK predict 3")
    return {"data": image_data, "result": res}