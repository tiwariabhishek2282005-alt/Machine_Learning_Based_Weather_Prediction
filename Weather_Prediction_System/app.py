import streamlit as st
import pandas as pd
import numpy as np
from ml_model import predict_weather
from datetime import datetime, timedelta
import pandas as pd
import os

next_hour = datetime.now() + timedelta(hours=1)

st.set_page_config(layout="wide")

# ---------- SAFE DATA ----------
data = None

# ---------- STYLE ----------
st.markdown("""
<style>

/* BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #020617, #1e293b, #1e3a8a);
    color: white;
}

/* REMOVE HEADER */
[data-testid="stHeader"] {
    background: transparent;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(135deg, #2563eb, #1e40af);
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    font-weight: bold;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #1e40af, #2563eb);
}

/* CITY BOX */
.top-chip {
    background: rgba(255,255,255,0.10);
    padding:15px;
    border-radius:18px;
    text-align:center;
    font-size:18px;
    font-weight:bold;
    color:white;
}

/* CARD */
.card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 18px;
    backdrop-filter: blur(10px);
    color: white;
}

.center {
    text-align:center;
}


</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
from datetime import datetime

current_time = datetime.now().strftime("%I:%M %p")

st.markdown(f"""
<h4 class='center'>🕒 {current_time}</h4>
""", unsafe_allow_html=True)
st.markdown("<h1 class='center'>🌦 Weather Dashboard</h1>", unsafe_allow_html=True)
st.markdown(f"""
<h3>Next Hour Forecast: {next_hour.strftime('%I %p')}</h3>
""", unsafe_allow_html=True)

# ---------- TOP CITY BAR ----------
c1,c2,c3,c4,c5 = st.columns(5)

city_data = [
    ("Delhi", 28),
    ("Mumbai", 27),
    ("Ahmedabad", 30),
    ("Bangalore", 26),
    ("Kolkata", 29)
]

for i, col in enumerate([c1,c2,c3,c4,c5]):
    name, temp = city_data[i]

    # Ahmedabad update AFTER click
    if name == "Ahmedabad" and data is not None:
        temp = data['temperature']

    col.markdown(f"""
    <div class='top-chip'>
        {name}<br>
        {temp}°C
    </div>
    """, unsafe_allow_html=True)

# ---------- BUTTON ----------
if st.button("🚀 Predict Next Hour Weather"):
    st.session_state.show_data = True
    st.session_state.data = predict_weather()
# UI SHOW
if "data" in st.session_state:

    data = st.session_state.data

    # BACKGROUND CHANGE BASED ON WEATHER
    if data['weather'] == "Clear":
        bg = "linear-gradient(135deg, #38bdf8, #2563eb)"   # sky blue
    #elif data['weather'] == "Cloudy":
    #    bg = "linear-gradient(135deg, #6b7280, #374151)"   # grey
    else:
        bg = "linear-gradient(135deg, #0f172a, #1e3a8a)"   # rainy dark

    
    # WEATHER ICON
    if data['weather'] == "Clear":
        icon = "☀️"
    elif data['weather'] == "Cloudy":
        icon = "☁️"
    else:
        icon = "🌧"
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: {bg};
        color: white;
    }}
    
    </style>
    """, unsafe_allow_html=True)

    
    st.success("Prediction Ready ✅")

    # ---------- MAIN SECTION ----------
    col1, col2 = st.columns([2,1])

    with col1:
        
        # TEMPERATURE COLOR LOGIC
        temp = data['temperature']

        if temp < 15:
            temp_color = "#3b82f6"
        elif temp < 25:
            temp_color = "#22c55e"
        elif temp < 35:
            temp_color = "#f97316"
        else:
            temp_color = "#ef4444"

        st.markdown(f"""
        <div class='card'>
            <h1 style='font-size:70px; color:{temp_color}'>{icon} {temp}°C</h1>
            <h3>{data['weather']}</h3>
            <p>Feels like: {data['feels_like']}°C</p>
            
        </div>
        
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='card'>
            🌬 Wind: {data['wind']} km/h<br><br>
            ضغط Pressure: {data['pressure']} mb<br><br>
            👁 Visibility: {data['visibility']} km<br><br>
            <p>💧Humidity: {data['humidity']}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ---------- REAL GRAPH ----------
    st.markdown("## 📊 Temperature Trend (Real Data)")

    import os

    file_path = os.path.join(os.path.dirname(__file__), "ahmedabad_weather_timeseries_10000.csv")
    df = pd.read_csv(file_path)

    df["Datetime"] = pd.to_datetime(df["Datetime"])
    df = df.sort_values("Datetime")

    last_data = df.tail(12)

    graph_df = last_data[["Datetime", "Temperature"]]
    graph_df = graph_df.set_index("Datetime")

    st.line_chart(graph_df)

    

    # ---------- AQI + UV ----------
    st.markdown("## 🌫 Air & UV")

    e1, e2 = st.columns(2)

    # AQI COLOR LOGIC
    aqi_value = data['aqi']

    if aqi_value <= 50:
        color = "#22c55e"   # green
    elif aqi_value <= 100:
        color = "#eab308"   # yellow
    elif aqi_value <= 150:
        color = "#f97316"   # orange
    else:
        color = "#ef4444"   # red

    e1.markdown(f"""
    <div class='card center'>
        🌫 AQI<br>
        <h2 style='color:{color}'>{aqi_value}</h2>
    </div>
    """, unsafe_allow_html=True)
    e2.markdown(f"<div class='card center'>UV Index<br><h2>{data['uv']}</h2></div>", unsafe_allow_html=True)

    # ---------- HOURLY ----------
    st.markdown("## ⏱ Hourly Forecast")

    hours = ["Now","10 PM","12 AM","2 AM","4 AM","6 AM"]
    temps = np.random.randint(25, 35, size=6)

    cols = st.columns(6)

    for i, col in enumerate(cols):
        col.markdown(f"""
        <div class='card center'>
            {hours[i]}<br>
            {temps[i]}°
        </div>
        """, unsafe_allow_html=True)
        # ---------- EXTRA DETAILS ----------
    st.markdown("## 🌍 Current Conditions")

    d1, d2, d3, d4 = st.columns(4)

    d1.markdown(f"""
    <div class='card center'>
    🌬 Wind<br>
    {data['wind']} km/h
    </div>
    """, unsafe_allow_html=True)

    d2.markdown(f"""
    <div class='card center'>
    💧 Humidity<br>
    {data['humidity']}%
    </div>
    """, unsafe_allow_html=True)

    d3.markdown(f"""
    <div class='card center'>
    ضغط Pressure<br>
    {data['pressure']} mb
    </div>
    """, unsafe_allow_html=True)

    d4.markdown(f"""
    <div class='card center'>
    👁 Visibility<br>
    {data['visibility']} km
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 💬 User Feedback")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        rating = st.slider("⭐ Rate the Prediction", 1, 5, 3)
        feedback = st.text_area("📝 Your Feedback")

        if st.button("Submit Feedback"):

            new_data = pd.DataFrame({
                "rating": [rating],
                "feedback": [feedback]
            })

            # file check
            if os.path.exists("feedback.csv"):
                old = pd.read_csv("feedback.csv")
                new_data = pd.concat([old, new_data], ignore_index=True)

            new_data.to_csv("feedback.csv", index=False)

            st.success("Feedback saved! 🙌")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div style='text-align:center; color:lightgray'>
    📊 Model Accuracy: {data['accuracy']}
    </div>
    """, unsafe_allow_html=True)