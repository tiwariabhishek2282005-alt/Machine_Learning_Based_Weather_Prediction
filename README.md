# 🌦 Machine Learning Based Weather Prediction System

🚀 A modern Machine Learning-based Weather Forecast Dashboard that predicts next hour weather conditions and visualizes them in a beautiful, interactive UI. 

---

## 📌 Project Overview

This project uses historical weather data and Machine Learning algorithms to predict future weather conditions such as temperature, humidity, wind speed, pressure, visibility, UV index, and AQI.

The predictions are displayed using a highly interactive and visually appealing Streamlit dashboard.

---

## ✨ Features

* 🌡 Next Hour Weather Prediction (ML Based)
* 📊 Real-time Temperature Trend Graph
* 🌫 AQI & UV Index Monitoring
* 💨 Wind, Pressure, Humidity, Visibility Cards
* 🧠 Smart Weather Classification (Clear / Cloudy / Rainy)
* ❤️ Health Advisory System based on weather
* ⭐ User Feedback System
* 🌍 Multi-city Weather UI (MSN Inspired Design)
* 🎨 Modern Glassmorphism UI Design

---

## 🧠 Machine Learning Details

* Model Used: `RandomForestRegressor`
* Wrapper: `MultiOutputRegressor`
* Input: Previous hour (lag features)
* Output: Multiple weather parameters

### 📥 Input Features:

* Temperature (lag1)
* Humidity (lag1)
* Wind Speed (lag1)
* Pressure (lag1)
* Visibility (lag1)
* UV Index (lag1)
* AQI (lag1)

### 📤 Output Predictions:

* Temperature
* Humidity
* Wind Speed
* Pressure
* Visibility
* UV Index
* AQI
* Feels Like Temperature

---

## 📁 Project Structure

```
Weather_Prediction_System/
│
├── app.py                          # Streamlit UI
├── ml_model.py                     # ML Model Training & Prediction
├── ahmedabad_weather_timeseries_10000.csv  # Dataset
├── feedback.csv                   # User Feedback Storage
├── requirements.txt               # Dependencies
└── README.md                      # Project Documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/YOUR_USERNAME/weather-ml-dashboard.git
cd weather-ml-dashboard
```

---

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Run the App

```
streamlit run app.py
```

---

## 🌐 Live Demo

👉 Coming Soon / (Add your Streamlit link here)

---

## 📊 Dataset Information

* Synthetic time-series weather dataset
* 10,000+ rows
* Includes hourly weather data
* City: Ahmedabad

---

## 🧪 Model Performance

* Metric: **R² Score**
* Accuracy: ~0.90+ (approx)

---

## 🛠 Technologies Used

* Python 🐍
* Streamlit 🎨
* Pandas 📊
* NumPy 🔢
* Scikit-learn 🤖
* Joblib ⚙️

---

## 🚀 Future Improvements

* 🌐 Real-time API integration
* 📍 Location-based prediction
* 📱 Mobile responsive UI
* 🔔 Weather alerts notification
* 🗺 Interactive weather maps

---

## 👨‍💻 Author

**Abhishek Dutt Tiwari**

---

## ⭐ Acknowledgement

Inspired by MSN Weather UI and modern dashboard design systems.

---

## 📬 Feedback

If you like this project, feel free to give a ⭐ on GitHub!
