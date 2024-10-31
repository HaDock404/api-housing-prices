import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

MODEL_PATH = '../model/modele_lr.pkl'
SCALER_PATH = '../model/scaler.pkl'
CSV_FILE_PATH = '../analysis/data/Housing.csv'

THRESHOLDS = {
    "r2": 0.65,
    "mae": 0.9,
    "mse": 1.25
}


# Fonction pour charger et préparer les données
def load_and_prepare_data(file_path):
    data = pd.read_csv(file_path, low_memory=False)
    data['prix(million)'] = data['price'] / 1000000
    data['air(m2)'] = data['area'] / 10.764
    data.drop(columns=['price', 'area'], inplace=True)
    data.rename(columns={
        'bedrooms': 'chambres', 'bathrooms': 'sdb', 'stories': 'étages',
        'mainroad': 'route principale', 'guestroom': 'chambre ami',
        'basement': 'sous sol', 'hotwaterheating': 'chauffage au gaz',
        'airconditioning': 'climatisation', 'parking': 'parking',
        'prefarea': 'résidentiel', 'furnishingstatus': 'meublé'
    }, inplace=True)
    data.replace({"yes": "oui", "no": "non"}, inplace=True)
    return labelencoder(data)


# Fonction pour encoder les colonnes catégorielles
def labelencoder(df):
    for col in df.select_dtypes(include='object').columns:
        unique_values = df[col].unique()
        if len(unique_values) == 2:
            df[col] = df[col].map({"non": 0, "oui": 1})
        else:
            df[col] = df[col].map({"unfurnished": 0,
                                   "semi-furnished": 1,
                                   "furnished": 2})
    return df


# Fonction d'entraînement et d'évaluation du modèle
def train_and_evaluate_model(data):
    X = data.drop(columns=['prix(million)'])
    y = data['prix(million)']
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        train_size=0.75,
                                                        test_size=0.25,
                                                        random_state=100)

    # Normaliser les données
    scaler = MinMaxScaler(feature_range=(0, 1))
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Entraîner le modèle
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Calculer les métriques
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"R^2 Score: {r2}")
    print(f"Mean Absolute Error (MAE): {mae}")
    print(f"Mean Squared Error (MSE): {mse}")

    return model, scaler, mse, mae, r2


# Fonction principale pour vérifier les métriques et sauvegarder
# le modèle si les critères sont respectés
def main():
    print("Start Training ..")
    print("-----------------")
    data = load_and_prepare_data(CSV_FILE_PATH)
    model, scaler, mse, mae, r2 = train_and_evaluate_model(data)

    # Vérifier les métriques par rapport aux seuils
    if (
        r2 >= THRESHOLDS["r2"]
        and mae <= THRESHOLDS["mae"]
        and mse <= THRESHOLDS["mse"]
    ):
        joblib.dump(model, MODEL_PATH)
        joblib.dump(scaler, SCALER_PATH)
        print("---------------------------------------------")
        print("Le modèle est performant et a été enregistré.")
    else:
        print("Le modèle n'a pas atteint les seuils de\
              performance et n'a pas été enregistré.")

    print("-------------")
    print("End Training.")


if __name__ == "__main__":
    main()
