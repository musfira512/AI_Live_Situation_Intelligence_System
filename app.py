import streamlit as st
import requests
from google import genai


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Live Situation Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM GLASSMORPHISM THEME
# =========================================================

st.markdown(
    """
    <style>

    /* -----------------------------------------------------
       GLOBAL APP
    ----------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(124, 58, 237, 0.30),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(99, 102, 241, 0.20),
                transparent 28%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(168, 85, 247, 0.18),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #080414 0%,
                #110725 45%,
                #1b0b38 100%
            );

        color: #f8f7ff;
        min-height: 100vh;
    }


    /* -----------------------------------------------------
       FORCE DARK THEME
    ----------------------------------------------------- */

    html,
    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    [data-testid="stAppViewContainer"] {
        color: #f8f7ff !important;
    }

    [data-testid="stHeader"] {
        background: rgba(0, 0, 0, 0) !important;
    }


    /* -----------------------------------------------------
       MAIN CONTENT WIDTH
    ----------------------------------------------------- */

    .block-container {
        max-width: 1000px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* -----------------------------------------------------
       HEADER
    ----------------------------------------------------- */

    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.3rem;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #d8b4fe,
                #a78bfa,
                #93c5fd
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        text-align: center;
        color: #c4b5fd;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }


    /* -----------------------------------------------------
       GLASS CARDS
    ----------------------------------------------------- */

    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 18px;
        padding: 20px 24px;
        margin-bottom: 18px;

        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);

        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
    }


    /* -----------------------------------------------------
       SECTION HEADINGS
    ----------------------------------------------------- */

    .section-title {
        color: #e9d5ff;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 12px;
    }


    /* -----------------------------------------------------
       STREAMLIT TEXT INPUTS
    ----------------------------------------------------- */

    div[data-baseweb="input"] {
        background: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="input"]:focus-within {
        border: 1px solid rgba(167, 139, 250, 0.8) !important;
        box-shadow: 0 0 0 1px rgba(167, 139, 250, 0.25) !important;
    }

    div[data-baseweb="input"] input {
        color: #ffffff !important;
        background: transparent !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #a8a0bd !important;
    }


    /* -----------------------------------------------------
       BUTTON
    ----------------------------------------------------- */

    div.stButton > button {
        width: 100%;
        min-height: 48px;

        border: none !important;
        border-radius: 12px !important;

        background:
            linear-gradient(
                135deg,
                #7c3aed,
                #8b5cf6,
                #6366f1
            ) !important;

        color: white !important;
        font-size: 1rem !important;
        font-weight: 700 !important;

        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35);

        transition: all 0.25s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(124, 58, 237, 0.50);
    }


    /* -----------------------------------------------------
       METRIC CARDS
    ----------------------------------------------------- */

    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 16px !important;
        padding: 16px !important;

        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
    }

    div[data-testid="stMetricLabel"] {
        color: #c4b5fd !important;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700 !important;
    }


    /* -----------------------------------------------------
       SUCCESS / INFO / WARNING / ERROR
    ----------------------------------------------------- */

    div[data-testid="stAlert"] {
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
    }


    /* -----------------------------------------------------
       AI ANALYSIS
    ----------------------------------------------------- */

    .ai-card {
        background:
            linear-gradient(
                135deg,
                rgba(124, 58, 237, 0.12),
                rgba(99, 102, 241, 0.06)
            );

        border: 1px solid rgba(167, 139, 250, 0.25);
        border-radius: 18px;
        padding: 24px;
        margin-top: 8px;

        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }


    /* -----------------------------------------------------
       MARKDOWN TEXT & READABILITY FIXES
    ----------------------------------------------------- */

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: #e2e8f0 !important;
        font-size: 0.98rem;
        line-height: 1.6;
    }

    [data-testid="stMarkdownContainer"] strong {
        color: #ffffff !important;
    }

    h1, h2, h3, h4 {
        color: #ffffff !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }


    /* -----------------------------------------------------
       FOOTER
    ----------------------------------------------------- */

    .footer {
        text-align: center;
        color: #a098ba;
        font-size: 0.85rem;
        margin-top: 40px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# API KEYS
# =========================================================

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)


# =========================================================
# LOCATION FUNCTION
# =========================================================

def get_location(city):
    url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city,
        "limit": 1,
        "appid": WEATHER_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=15)
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

    except requests.RequestException:
        return None, "Unable to connect to the location service."


# =========================================================
# WEATHER FUNCTION
# =========================================================

def get_weather(latitude, longitude):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code != 200:
            return None, response.text

        data = response.json()

        weather = {
            "temperature": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "humidity": round(data["main"]["humidity"]),
            "description": data["weather"][0]["description"],
            "wind_speed": round(data["wind"]["speed"], 1),
            "pressure": round(data["main"]["pressure"])
        }

        return weather, None

    except requests.RequestException:
        return None, "Unable to connect to the weather service."


# =========================================================
# AI SITUATION ANALYSIS
# =========================================================

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

Analyze the CURRENT environmental and weather conditions
for the specific location provided below.

{situation_data}

Your analysis MUST be based on the actual weather values provided.
Do NOT give a generic weather report.

Return the following sections:

### Current Situation
Explain what is happening at this specific location.

### Risk Level
Choose exactly ONE: Low, Moderate, High, Critical.
Justify the risk level using the actual weather conditions.

### Important Concerns
Mention only concerns that are relevant to the current conditions.

### Recommended Actions
Give practical actions that a person at this location should consider.

### Outdoor Activity Advice
Choose exactly ONE: Generally Safe, Use Caution, Not Recommended.

Keep the analysis concise, practical, and location-specific.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text, None

    except Exception as e:
        return None, str(e)


# =========================================================
# HEADER
# =========================================================

st.markdown('<div class="main-title">🌍 AI Live Situation Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-time environmental intelligence powered by Generative AI</div>', unsafe_allow_html=True)


# =========================================================
# LOCATION INPUT CARD
# =========================================================

city = st.text_input(
    "Select Location",
    placeholder="Example: Lahore, Dubai, London"
)

analyze_button = st.button("🔍 Analyze Current Situation", type="primary")


if analyze_button:
    if not city.strip():
        st.warning("Please enter a city name.")
    else:
        # -------------------------------------------------
        # LOCATION
        # -------------------------------------------------
        with st.spinner("Finding location..."):
            location, location_error = get_location(city)

        if location_error:
            st.error(location_error)
        else:
            location_name = location["name"]
            if location["state"]:
                location_name += f", {location['state']}"
            location_name += f", {location['country']}"

            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="section-title">📍 Location Detected</div>
                    <div style="font-size: 1.25rem; font-weight: 700; color: white; margin-bottom: 4px;">
                        {location_name}
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.88rem;">
                        Coordinates: {location['latitude']:.4f}, {location['longitude']:.4f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # -------------------------------------------------
            # WEATHER
            # -------------------------------------------------
            with st.spinner("Getting live weather data..."):
                weather, weather_error = get_weather(
                    location["latitude"],
                    location["longitude"]
                )

            if weather_error:
                st.error("Unable to retrieve live weather data.")
                st.code(weather_error)
            else:
                # -------------------------------------------------
                # WEATHER SECTION
                # -------------------------------------------------
                st.markdown('<div class="section-title">🌦️ Live Weather</div>', unsafe_allow_html=True)

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Temperature", f'{weather["temperature"]} °C')
                with col2:
                    st.metric("Feels Like", f'{weather["feels_like"]} °C')
                with col3:
                    st.metric("Humidity", f'{weather["humidity"]} %')
                with col4:
                    st.metric("Wind Speed", f'{weather["wind_speed"]} m/s')

                # Fixed HTML rendering bug by placing content directly inside native Streamlit container
                st.markdown(
                    f"""
                    <div class="glass-card" style="text-align:center; margin-top: 14px;">
                        <div style="color:#c4b5fd; font-size:0.85rem; font-weight:600; letter-spacing:1px; margin-bottom:4px;">
                            CURRENT CONDITION
                        </div>
                        <div style="color:white; font-size:1.3rem; font-weight:700;">
                            {weather["description"].title()}
                        </div>
                        <div style="color:#cbd5e1; font-size:0.85rem; margin-top:6px;">
                            Atmospheric Pressure: {weather["pressure"]} hPa
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # -------------------------------------------------
                # AI ANALYSIS
                # -------------------------------------------------
                st.markdown('<div class="section-title">🧠 AI Situation Intelligence</div>', unsafe_allow_html=True)

                with st.spinner("Gemini is analyzing the current situation..."):
                    analysis, analysis_error = analyze_situation(
                        location,
                        weather
                    )

                if analysis_error:
                    st.error("Unable to generate AI analysis.")
                    st.code(analysis_error)
                else:
                    # Streamlit Markdown container cleanly wrapping output without broken div tags
                    with st.container():
                        st.markdown('<div class="ai-card">', unsafe_allow_html=True)
                        st.markdown(analysis)
                        st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        AI Live Situation Intelligence · Real-time data + Generative AI
    </div>
    """,
    unsafe_allow_html=True
)
