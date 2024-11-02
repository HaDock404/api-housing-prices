# api.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Charger le modèle et le scaler
# model = joblib.load('../model/modele_lr.pkl')
# scaler = joblib.load('../model/scaler.pkl')

model = joblib.load('/app/model/modele_lr.pkl')
scaler = joblib.load('/app/model/scaler.pkl')


# Définir le modèle de données pour la requête
class PredictionRequest(BaseModel):
    features: list


@app.post("/predict")
async def predict(request: PredictionRequest):
    # Convertir les caractéristiques en format compatible
    data_input = np.array(request.features).reshape(1, -1)

    # Normaliser les données
    data_input = scaler.transform(data_input)

    # Effectuer la prédiction
    prediction = model.predict(data_input)

    # Retourner la prédiction sous forme JSON
    return {"predicted_price": prediction[0]}
