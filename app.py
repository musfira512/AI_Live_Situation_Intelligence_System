import streamlit as st
import requests
from google import genai


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Live Situation Intelligence",
    page_icon="🌍",
    layout="wide"
)


# --------------------------------------------------
# API CONFIGURATION
# --------------------------------------------------

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)


# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def get_weather(latitude, longitude):

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None, response.text

    data = response.json()

    weather = {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }

    return weather, None


def analyze_situation(latitude, longitude, weather, traffic):

    situation_data = f"""
LOCATION
Latitude: {latitude}
Longitude: {longitude}

WEATHER
Temperature: {weather["temperature"]} °C
Humidity: {weather["humidity"]} %
Condition: {weather["description"]}
Wind Speed: {weather["wind_speed"]} m/s

TRAFFIC
Traffic Level: {traffic["traffic_level"]}
Average Speed: {traffic["average_speed"]} km/h
Road Condition: {traffic["road_condition"]}
Estimated Delay: {traffic["estimated_delay"]} minutes
"""

    prompt = f"""
You are an AI Live Situation Intelligence assistant.

Analyze the following real-time situation:

{situation_data}

Provide:

1. Current Situation
2. Risk Level: Low, Moderate, High, or Critical
3. Important Concerns
4. Recommended Actions

Consider both weather and traffic.

Keep the response simple, practical, and useful.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🌍 AI Live Situation Intelligence")

st.write(
    "An AI-powered system that analyzes live environmental "
    "and traffic information to provide situation awareness, "
    "risk assessment, and recommendations."
)

st.divider()


# --------------------------------------------------
# LOCATION
# --------------------------------------------------

st.subheader("📍 Location")

col1, col2 = st.columns(2)

with col1:
    latitude = st.number_input(
        "Latitude",
        value=31.5204,
        format="%.4f"
    )

with col2:
    longitude = st.number_input(
        "Longitude",
        value=74.3587,
        format="%.4f"
    )


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if st.button("🔄 Analyze Current Situation", type="primary"):

    with st.spinner("Getting live weather data..."):

        weather, error = get_weather(
            latitude,
            longitude
        )

    if error:

        st.error("Unable to retrieve weather data.")
        st.code(error)

    else:

        # --------------------------------------------------
        # TEMPORARY TRAFFIC DATA
        # --------------------------------------------------

        traffic = {
            "traffic_level": "Heavy",
            "average_speed": 18,
            "road_condition": "Congested",
            "estimated_delay": 25
        }

        # --------------------------------------------------
        # WEATHER DISPLAY
        # --------------------------------------------------

        st.subheader("🌦️ Live Weather")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Temperature",
                f'{weather["temperature"]} °C'
            )

        with col2:
            st.metric(
                "Humidity",
                f'{weather["humidity"]} %'
            )

        with col3:
            st.metric(
                "Wind Speed",
                f'{weather["wind_speed"]} m/s'
            )

        with col4:
            st.metric(
                "Condition",
                weather["description"].title()
            )

        # --------------------------------------------------
        # TRAFFIC DISPLAY
        # --------------------------------------------------

        st.subheader("🚗 Traffic Situation")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Traffic",
                traffic["traffic_level"]
            )

        with col2:
            st.metric(
                "Average Speed",
                f'{traffic["average_speed"]} km/h'
            )

        with col3:
            st.metric(
                "Road Condition",
                traffic["road_condition"]
            )

        with col4:
            st.metric(
                "Estimated Delay",
                f'{traffic["estimated_delay"]} min'
            )

        # --------------------------------------------------
        # AI ANALYSIS
        # --------------------------------------------------

        st.subheader("🧠 AI Situation Intelligence")

        with st.spinner("Gemini is analyzing the situation..."):

            analysis = analyze_situation(
                latitude,
                longitude,
                weather,
                traffic
            )

        st.markdown(analysis)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI Live Situation Intelligence | Generative AI Hackathon Project"
)
