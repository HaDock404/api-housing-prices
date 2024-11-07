from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load('/app/models/modele_lr.pkl')
scaler = joblib.load('/app/models/scaler.pkl')


class PredictionRequest(BaseModel):
    features: list


@app.get("/")
def hello():
    """
    Default route to welcome users and direct them to documentation.

    Returns:
        dict: A welcome message.
    """

    return {"message": "Hi, add /docs to the URL to use the API."}


@app.post("/predict")
async def predict(request: PredictionRequest):
    """
    Endpoint for predicting the price of a house based on characteristics \
        provided by the user.

    Arguments:
        request (PredictionRequest): Query containing the characteristics of \
            the house to predict.
                                     It must include the following information:
                                     - number of rooms
                                     - number of bathrooms
                                     - number of stories
                                     - closed to mainroad: no = 0, yes = 1
                                     - guest room: no = 0, yes = 1
                                     - basement: no = 0, yes = 1
                                     - hot water heating: no = 0, yes = 1
                                     - air conditioning: no = 0, yes = 1
                                     - number of parking
                                     - prefered area of the city: \
                                        no = 0, yes = 1
                                     - furnishing status : unfurnished = 0 \
                                        semi furnished = 1, furnihed = 2
                                     - other relevant characteristics
                                     - surface of the house m2

    Example:
        {
            "features": [
                4, 2, 3, 1, 0, 0, 0, 1, 2, 1, 2, 690
            ]
        }

    Return:
        dict: A dictionary with the estimated price, in the form \
            {"predicted_price": value}.
    """
    data_input = np.array(request.features).reshape(1, -1)
    data_input = scaler.transform(data_input)
    prediction = model.predict(data_input)

    return {"predicted_price": prediction[0]}
