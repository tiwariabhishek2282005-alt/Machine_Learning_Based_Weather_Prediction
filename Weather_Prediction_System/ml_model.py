import pandas as pd
import os
import joblib
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

MODEL_PATH = "model.pkl"

def train_model():
    file_path = os.path.join(os.path.dirname(__file__), "ahmedabad_weather_timeseries_10000.csv")
    data = pd.read_csv(file_path)

    data["Datetime"] = pd.to_datetime(data["Datetime"])
    data = data.sort_values("Datetime")

    # ---------- LAG FEATURES ----------
    data["temp_lag1"] = data["Temperature"].shift(1)
    data["humidity_lag1"] = data["Humidity"].shift(1)
    data["wind_lag1"] = data["Wind"].shift(1)
    data["pressure_lag1"] = data["Pressure"].shift(1)
    data["visibility_lag1"] = data["Visibility"].shift(1)
    data["uv_lag1"] = data["UV"].shift(1)
    data["aqi_lag1"] = data["AQI"].shift(1)

    from datetime import datetime

    # current time
    now = datetime.now()

    # closest time find
    data["time_diff"] = abs(data["Datetime"] - now)

    # nearest row
    closest = data.sort_values("time_diff").iloc[0:1]

    X = closest[[
        "temp_lag1",
        "humidity_lag1",
        "wind_lag1",
        "pressure_lag1",
        "visibility_lag1",
        "uv_lag1",
        "aqi_lag1"
    ]]
    # ---------- FEATURES ----------
    X = data[[
        "temp_lag1",
        "humidity_lag1",
        "wind_lag1",
        "pressure_lag1",
        "visibility_lag1",
        "uv_lag1",
        "aqi_lag1"
    ]]

    # ---------- TARGET ----------
    y = data[[
        "Temperature",
        "Humidity",
        "Wind",
        "Pressure",
        "Visibility",
        "UV",
        "AQI",
        "FeelsLike"
    ]]

    model = MultiOutputRegressor(RandomForestRegressor(n_estimators=60))
    model.fit(X, y)
    pred_train = model.predict(X)
    accuracy = r2_score(y, pred_train)

    joblib.dump((model, accuracy), MODEL_PATH)

    return model, X, accuracy


def load_model():
    if os.path.exists(MODEL_PATH):
        model, accuracy = joblib.load(MODEL_PATH)
        return model, None, accuracy
    else:
        return train_model()


def predict_weather():
    model, X, accuracy = load_model()

    if X is None:
        file_path = os.path.join(os.path.dirname(__file__), "ahmedabad_weather_timeseries_10000.csv")
        data = pd.read_csv(file_path)

        data["Datetime"] = pd.to_datetime(data["Datetime"])
        data = data.sort_values("Datetime")

        # Lag recreate
        data["temp_lag1"] = data["Temperature"].shift(1)
        data["humidity_lag1"] = data["Humidity"].shift(1)
        data["wind_lag1"] = data["Wind"].shift(1)
        data["pressure_lag1"] = data["Pressure"].shift(1)
        data["visibility_lag1"] = data["Visibility"].shift(1)
        data["uv_lag1"] = data["UV"].shift(1)
        data["aqi_lag1"] = data["AQI"].shift(1)

        data = data.dropna().tail(1)

        X = data[[
            "temp_lag1",
            "humidity_lag1",
            "wind_lag1",
            "pressure_lag1",
            "visibility_lag1",
            "uv_lag1",
            "aqi_lag1"
        ]]

    pred = model.predict(X)[0]

    # ---------- WEATHER LOGIC ----------
    if pred[1] > 0.8:
        weather = "Rainy"
    elif pred[1] > 0.6:
        weather = "Cloudy"
    else:
        weather = "Clear"

    return {
        "temperature": round(pred[0], 2),
        "humidity": round(pred[1] * 100, 2),
        "wind": round(pred[2], 2),
        "pressure": round(pred[3], 2),
        "visibility": round(pred[4], 2),
        "uv": round(pred[5], 2),
        "aqi": round(pred[6], 2),
        "weather": weather,
        "feels_like": round(pred[7], 2),
        "accuracy": round(accuracy, 2) if accuracy else 0.9
    }