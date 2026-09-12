import streamlit as st
import requests
from google import genai


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Live Situation Intelligence",
    page_icon="🌍",
    layout="wide"
)


# ==================================================
# API CONFIGURATION
# ==================================================

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]
TOMTOM_API_KEY = st.secrets["TOMTOM_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)


# ==================================================
# GET LOCATION FROM CITY NAME
# ==================================================

def get_location(city):

    url = "https://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q": city,
        "limit": 1,
        "appid": WEATHER_API_KEY
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

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

    except Exception as e:

        return None, str(e)


# ==================================================
# GET WEATHER
# ==================================================

def get_weather(latitude, longitude):

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

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

    except Exception as e:

        return None, str(e)


# ==================================================
# GET TOMTOM TRAFFIC
# ==================================================

def get_traffic(latitude, longitude):

    url = (
        "https://api.tomtom.com/traffic/services/"
        "4/flowSegmentData/absolute/10/json"
    )

    params = {
        "key": TOMTOM_API_KEY,
        "point": f"{latitude},{longitude}",
        "unit": "kmph"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        # Traffic unavailable
        if response.status_code != 200:
            return None, response.text

        data = response.json()

        flow = data.get("flowSegmentData", {})

        current_speed = flow.get("currentSpeed")
        free_flow_speed = flow.get("freeFlowSpeed")
        confidence = flow.get("confidence")
        road_closure = flow.get("roadClosure")

        if current_speed is None or free_flow_speed is None:
            return None, "Traffic data unavailable."

        # ------------------------------------------
        # Calculate traffic condition
        # ------------------------------------------

        if free_flow_speed > 0:

            speed_ratio = current_speed / free_flow_speed

        else:

            speed_ratio = 0

        if speed_ratio >= 0.80:

            traffic_condition = "Light Traffic"

        elif speed_ratio >= 0.50:

            traffic_condition = "Moderate Traffic"

        elif speed_ratio >= 0.30:

            traffic_condition = "Heavy Traffic"

        else:

            traffic_condition = "Severe Congestion"

        traffic = {
            "current_speed": current_speed,
            "free_flow_speed": free_flow_speed,
            "confidence": confidence,
            "road_closure": road_closure,
            "traffic_condition": traffic_condition
        }

        return traffic, None

    except Exception as e:

        return None, str(e)


# ==================================================
# AI SITUATION ANALYSIS
# ==================================================

def analyze_situation(location, weather, traffic=None):

    # ----------------------------------------------
    # Traffic information
    # ----------------------------------------------

    if traffic:

        traffic_data = f"""
TRAFFIC CONDITIONS

Current Speed:
{traffic["current_speed"]} km/h

Normal Free-Flow Speed:
{traffic["free_flow_speed"]} km/h

Traffic Condition:
{traffic["traffic_condition"]}

Traffic Confidence:
{traffic["confidence"]}

Road Closure:
{traffic["road_closure"]}
"""

    else:

        traffic_data = """
TRAFFIC CONDITIONS

Live traffic data is currently unavailable for this location.

Do NOT assume whether traffic is light, moderate, heavy,
or congested.
"""


    # ----------------------------------------------
    # Complete situation data
    # ----------------------------------------------

    situation_data = f"""
LOCATION

City:
{location["name"]}

State/Region:
{location["state"]}

Country:
{location["country"]}

Latitude:
{location["latitude"]}

Longitude:
{location["longitude"]}


CURRENT WEATHER

Temperature:
{weather["temperature"]} °C

Feels Like:
{weather["feels_like"]} °C

Humidity:
{weather["humidity"]} %

Weather Condition:
{weather["description"]}

Wind Speed:
{weather["wind_speed"]} m/s

Atmospheric Pressure:
{weather["pressure"]} hPa


{traffic_data}
"""


    # ----------------------------------------------
    # Gemini prompt
    # ----------------------------------------------

    prompt = f"""
You are an AI Live Situation Intelligence system.

Your task is to analyze the CURRENT environmental
and mobility conditions for the specific location below.

{situation_data}

IMPORTANT RULES:

1. Base your analysis ONLY on the actual data provided.
2. Do not invent weather or traffic information.
3. Do not make assumptions about unavailable traffic data.
4. Keep the analysis specific to this location.
5. Do not provide a generic weather forecast.
6. Consider the combined effect of weather and traffic
   when traffic data is available.


Analyze:

WEATHER

- Temperature
- Feels-like temperature
- Humidity
- Weather condition
- Wind speed
- Atmospheric pressure


TRAFFIC

- Current speed
- Free-flow speed
- Traffic congestion
- Road closure
- Traffic confidence


Consider possible risks such as:

- Heat stress
- Cold stress
- Heavy rain
- Storms
- Strong winds
- Poor visibility
- Road congestion
- Difficult travel conditions
- Road closures
- Unsafe outdoor conditions


Return EXACTLY these sections:


## 1. Current Situation

Explain what is currently happening at this location.


## 2. Risk Level

Choose exactly ONE:

Low
Moderate
High
Critical

Explain why this risk level was selected using
the actual weather and traffic data.


## 3. Important Concerns

Mention only concerns that are relevant to
the current conditions.


## 4. Recommended Actions

Give practical actions that people at this location
should consider.


## 5. Outdoor Activity Advice

Choose exactly ONE:

Generally Safe
Use Caution
Not Recommended


## 6. Travel Situation

Explain whether current conditions are favorable
or unfavorable for travel.

If traffic data is unavailable, clearly state that
traffic conditions could not be assessed.


Keep the response concise, practical,
and location-specific.
"""


    # ----------------------------------------------
    # Gemini request
    # ----------------------------------------------

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


# ==================================================
# APPLICATION UI
# ==================================================

st.title("🌍 AI Live Situation Intelligence")

st.write(
    "Analyze current environmental and traffic conditions "
    "for a selected location using live data and Generative AI."
)

st.divider()


# ==================================================
# LOCATION INPUT
# ==================================================

st.subheader("📍 Select Location")

city = st.text_input(
    "Enter city name",
    placeholder="Example: Lahore, Dubai, London"
)


# ==================================================
# ANALYZE BUTTON
# ==================================================

if st.button(
    "🔍 Analyze Current Situation",
    type="primary"
):

    # ----------------------------------------------
    # Validate city
    # ----------------------------------------------

    if not city.strip():

        st.warning(
            "Please enter a city name."
        )

    else:

        # ==========================================
        # LOCATION
        # ==========================================

        with st.spinner(
            "Finding location..."
        ):

            location, location_error = get_location(city)


        if location_error:

            st.error(
                location_error
            )

        else:

            # --------------------------------------
            # Location name
            # --------------------------------------

            location_name = location["name"]

            if location["state"]:

                location_name += (
                    f", {location['state']}"
                )

            location_name += (
                f", {location['country']}"
            )


            st.success(
                f"Location found: {location_name}"
            )


            st.caption(
                "Coordinates: "
                f"{location['latitude']:.4f}, "
                f"{location['longitude']:.4f}"
            )


            # ======================================
            # WEATHER
            # ======================================

            with st.spinner(
                "Getting live weather data..."
            ):

                weather, weather_error = get_weather(
                    location["latitude"],
                    location["longitude"]
                )


            if weather_error:

                st.error(
                    "Unable to retrieve weather data."
                )

                st.code(
                    weather_error
                )

            else:

                # ==================================
                # WEATHER DISPLAY
                # ==================================

                st.subheader(
                    "🌦️ Live Weather"
                )

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
                    "Current condition: "
                    f'**{weather["description"].title()}**'
                )


                # ==================================
                # TRAFFIC
                # ==================================

                with st.spinner(
                    "Checking live traffic conditions..."
                ):

                    traffic, traffic_error = get_traffic(
                        location["latitude"],
                        location["longitude"]
                    )


                st.subheader(
                    "🚦 Live Traffic"
                )


                if traffic:

                    traffic_col1, traffic_col2, traffic_col3 = (
                        st.columns(3)
                    )


                    with traffic_col1:

                        st.metric(
                            "Current Speed",
                            f'{traffic["current_speed"]} km/h'
                        )


                    with traffic_col2:

                        st.metric(
                            "Free Flow Speed",
                            f'{traffic["free_flow_speed"]} km/h'
                        )


                    with traffic_col3:

                        st.metric(
                            "Traffic",
                            traffic["traffic_condition"]
                        )


                    if traffic["road_closure"]:

                        st.warning(
                            "Road closure detected."
                        )


                else:

                    st.warning(
                        "Live traffic data is currently "
                        "unavailable for this location."
                    )


                    # Do not show technical API error
                    # to normal users.


                # ==================================
                # AI ANALYSIS
                # ==================================

                st.subheader(
                    "🧠 AI Situation Intelligence"
                )


                with st.spinner(
                    "Gemini is analyzing the current situation..."
                ):

                    try:

                        analysis = analyze_situation(
                            location,
                            weather,
                            traffic
                        )

                        st.markdown(
                            analysis
                        )

                    except Exception as e:

                        st.error(
                            "Unable to generate AI analysis."
                        )

                        st.code(
                            str(e)
                        )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "AI Live Situation Intelligence | "
    "Generative AI Hackathon Project"
)
