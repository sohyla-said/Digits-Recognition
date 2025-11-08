import pickle
from fastapi import FastAPI
from digits_recognition.types.server_types import Item
from digits_recognition.server.config import MODEL_PATH



model = pickle.load(open(MODEL_PATH, "rb"))

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "world"}

@app.post("/predict/")
def predict_digit(item: Item):
    prediction = model.predict([item.image_data])
    return {"predictions": int(prediction[0])}
