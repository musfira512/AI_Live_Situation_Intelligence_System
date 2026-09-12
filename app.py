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
# GET LOCATION FROM CITY NAME
# --------------------------------------------------

def get_location(city):

    url = "https://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q": city,
        "limit": 1,
        "appid": WEATHER_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None, "Unable to find the location."

    data = response.json()

    if not data:
        return None, "City not found. Please enter a valid city."

    location = {
        "name": data[0]["name"],
        "country": data[0].get("country", ""),
        "state": data[0].get("state", ""),
        "latitude": data[0]["lat"],
        "longitude": data[0]["lon"]
    }

    return location, None


# --------------------------------------------------
# GET WEATHER
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
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
        "pressure": data["main"]["pressure"]
    }

    return weather, None


# --------------------------------------------------
# AI ANALYSIS
# --------------------------------------------------

def analyze_situation(location, weather):

    situation_data = f"""
LOCATION
City: {location["name"]}
State/Region: {location["state"]}
Country: {location["country"]}
Latitude: {location["latitude"]}
Longitude: {location["longitude"]}

CURRENT WEATHER
Temperature: {weather["temperature"]} °C
Feels Like: {weather["feels_like"]} °C
Humidity: {weather["humidity"]} %
Weather Condition: {weather["description"]}
Wind Speed: {weather["wind_speed"]} m/s
Atmospheric Pressure: {weather["pressure"]} hPa
"""

    prompt = f"""
You are an AI Live Situation Intelligence system.

Analyze the CURRENT weather conditions for the specific location below.

{situation_data}

Your analysis MUST be based on the actual weather values provided above.

Do not give a generic weather response.

Consider:
- Temperature
- Feels-like temperature
- Humidity
- Weather condition
- Wind speed
- Atmospheric pressure
- Possible heat stress, cold stress, rain, storms, strong winds, poor visibility, or other relevant risks

Return the following sections:

1. Current Situation
Explain what is happening at this specific location.

2. Risk Level
Choose exactly one:
Low
Moderate
High
Critical

The risk level must be justified using the actual weather conditions.

3. Important Concerns
Mention only concerns that are relevant to the current conditions.

4. Recommended Actions
Give practical actions that a person at this location should consider.

5. Outdoor Activity Advice
Tell the user whether outdoor activity is:
- Generally Safe
- Use Caution
- Not Recommended

Keep the answer concise and location-specific.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


# --------------------------------------------------
# APPLICATION UI
# --------------------------------------------------

st.title("🌍 AI Live Situation Intelligence")

st.write(
    "Enter a city to analyze its current weather conditions "
    "and receive AI-powered risk assessment and recommendations."
)

st.divider()


# --------------------------------------------------
# CITY INPUT
# --------------------------------------------------

st.subheader("📍 Select Location")

city = st.text_input(
    "Enter city name",
    placeholder="Example: Lahore, Dubai, London"
)


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if st.button("🔍 Analyze Current Situation", type="primary"):

    if not city.strip():

        st.warning("Please enter a city name.")

    else:

        # ------------------------------------------
        # FIND LOCATION
        # ------------------------------------------

        with st.spinner("Finding location..."):

            location, location_error = get_location(city)

        if location_error:

            st.error(location_error)

        else:

            # --------------------------------------
            # DISPLAY LOCATION
            # --------------------------------------

            location_name = location["name"]

            if location["state"]:
                location_name += f", {location['state']}"

            location_name += f", {location['country']}"

            st.success(f"Location found: {location_name}")

            st.caption(
                f"Coordinates: "
                f"{location['latitude']:.4f}, "
                f"{location['longitude']:.4f}"
            )


            # --------------------------------------
            # GET WEATHER
            # --------------------------------------

            with st.spinner("Getting live weather data..."):

                weather, weather_error = get_weather(
                    location["latitude"],
                    location["longitude"]
                )

            if weather_error:

                st.error("Unable to retrieve weather data.")
                st.code(weather_error)

            else:

                # ----------------------------------
                # WEATHER DISPLAY
                # ----------------------------------

                st.subheader("🌦️ Live Weather")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Temperature",
                        f'{weather["temperature"]} °C'
                    )

                with col2:
                    st.metric(
                        "Feels Like",
                        f'{weather["feels_like"]} °C'
                    )

                with col3:
                    st.metric(
                        "Humidity",
                        f'{weather["humidity"]} %'
                    )

                with col4:
                    st.metric(
                        "Wind Speed",
                        f'{weather["wind_speed"]} m/s'
                    )

                st.info(
                    f"Current condition: "
                    f"**{weather['description'].title()}**"
                )


                # ----------------------------------
                # AI ANALYSIS
                # ----------------------------------

                st.subheader("🧠 AI Situation Intelligence")

                with st.spinner(
                    "Gemini is analyzing the current situation..."
                ):

                    analysis = analyze_situation(
                        location,
                        weather
                    )

                st.markdown(analysis)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI Live Situation Intelligence | "
    "Generative AI Hackathon Project"
)
