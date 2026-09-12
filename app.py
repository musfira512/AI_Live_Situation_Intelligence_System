import html
import re

import requests
import streamlit as st
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
# CUSTOM THEME
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    html {
        color-scheme: dark;
    }

    body {
        background: #090414 !important;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 10% 5%,
                rgba(124, 58, 237, 0.28),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(99, 102, 241, 0.20),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(168, 85, 247, 0.15),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #090414 0%,
                #120725 48%,
                #1b0b38 100%
            ) !important;

        min-height: 100vh;
        color: #ffffff !important;
    }

    [data-testid="stAppViewContainer"] {
        background: transparent !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    [data-testid="stToolbar"] {
        background: transparent !important;
    }

    .block-container {
        max-width: 1050px !important;
        padding-top: 42px !important;
        padding-bottom: 45px !important;
    }


    /* =====================================================
       REMOVE UNNECESSARY STREAMLIT SPACING
       ===================================================== */

    [data-testid="stVerticalBlock"] {
        gap: 0.65rem;
    }

    div[data-testid="stElementContainer"] {
        margin-bottom: 0.2rem;
    }


    /* =====================================================
       HERO
       ===================================================== */

    .hero {
        text-align: center;
        margin-bottom: 34px;
    }

    .hero-title {
        font-size: 42px;
        line-height: 1.15;
        font-weight: 800;
        letter-spacing: -1.2px;
        margin: 0;
        color: #ffffff;

        background: linear-gradient(
            90deg,
            #ffffff 0%,
            #ddd6fe 35%,
            #a78bfa 65%,
            #c4b5fd 100%
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        margin-top: 12px;
        font-size: 16px;
        line-height: 1.6;
        font-weight: 400;
        color: #e2e8f0 !important;
    }


    /* =====================================================
       GLASS CARD
       ===================================================== */

    .glass-card {
        background: rgba(255, 255, 255, 0.065);

        border: 1px solid rgba(255, 255, 255, 0.14);

        border-radius: 20px;

        padding: 24px;

        margin: 0 0 24px 0;

        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);

        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.28),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }


    /* =====================================================
       SECTION TITLES
       ===================================================== */

    .section-title {
        font-size: 20px;
        line-height: 1.4;
        font-weight: 700;
        color: #ffffff !important;

        margin: 0 0 16px 0;
    }

    .section-description {
        font-size: 15px;
        line-height: 1.65;
        color: #e2e8f0 !important;

        margin-bottom: 18px;
    }


    /* =====================================================
       INPUT FIELD
       ===================================================== */

    div[data-testid="stTextInput"] {
        margin-bottom: 0 !important;
    }

    div[data-testid="stTextInput"] label {
        color: #e2e8f0 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stTextInput"] > div {
        background: transparent !important;
    }

    div[data-baseweb="input"] {
        background: rgba(9, 4, 20, 0.72) !important;

        border: 1px solid rgba(196, 181, 253, 0.22) !important;

        border-radius: 14px !important;

        min-height: 50px !important;

        box-shadow:
            inset 0 1px 2px rgba(0, 0, 0, 0.25) !important;
    }

    div[data-baseweb="input"]:focus-within {
        background: rgba(12, 6, 27, 0.90) !important;

        border-color: #a78bfa !important;

        box-shadow:
            0 0 0 2px rgba(167, 139, 250, 0.15),
            0 0 20px rgba(124, 58, 237, 0.18) !important;
    }

    div[data-baseweb="input"] input {
        background: transparent !important;

        color: #ffffff !important;

        font-size: 16px !important;

        font-weight: 400 !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #a8a0bd !important;

        opacity: 1 !important;
    }


    /* =====================================================
       ANALYZE BUTTON
       ===================================================== */

    div.stButton {
        margin-top: 12px;
        margin-bottom: 0;
    }

    div.stButton > button {
        width: 100% !important;

        min-height: 50px !important;

        border: 0 !important;

        border-radius: 14px !important;

        background:
            linear-gradient(
                135deg,
                #7c3aed 0%,
                #8b5cf6 50%,
                #6366f1 100%
            ) !important;

        color: #ffffff !important;

        font-size: 16px !important;

        font-weight: 700 !important;

        box-shadow:
            0 8px 25px rgba(124, 58, 237, 0.30) !important;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease !important;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 12px 32px rgba(124, 58, 237, 0.45) !important;

        border: 0 !important;
    }

    div.stButton > button:focus {
        border: 0 !important;

        outline: none !important;
    }


    /* =====================================================
       LOCATION CARD
       ===================================================== */

    .location-name {
        font-size: 21px;
        line-height: 1.4;
        font-weight: 700;
        color: #ffffff !important;

        margin-bottom: 8px;
    }

    .coordinates {
        font-size: 15px;
        line-height: 1.6;
        color: #e2e8f0 !important;
    }


    /* =====================================================
       WEATHER CARDS
       ===================================================== */

    .weather-grid {
        display: grid;

        grid-template-columns:
            repeat(4, minmax(0, 1fr));

        gap: 16px;

        margin-bottom: 24px;
    }

    .weather-card {
        background: rgba(255, 255, 255, 0.065);

        border: 1px solid rgba(255, 255, 255, 0.13);

        border-radius: 18px;

        padding: 20px;

        min-height: 112px;

        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.22);
    }

    .weather-label {
        font-size: 14px;
        line-height: 1.4;

        color: #c4b5fd !important;

        font-weight: 600;

        margin-bottom: 9px;
    }

    .weather-value {
        font-size: 24px;
        line-height: 1.25;

        color: #ffffff !important;

        font-weight: 750;
    }


    /* =====================================================
       CURRENT CONDITION
       ===================================================== */

    .condition-card {
        background:
            linear-gradient(
                135deg,
                rgba(124, 58, 237, 0.13),
                rgba(99, 102, 241, 0.06)
            );

        border: 1px solid rgba(167, 139, 250, 0.22);

        border-radius: 20px;

        padding: 22px 24px;

        margin-bottom: 28px;

        text-align: center;

        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
    }

    .condition-label {
        font-size: 13px;
        letter-spacing: 1px;
        font-weight: 700;

        color: #c4b5fd !important;

        margin-bottom: 8px;
    }

    .condition-value {
        font-size: 24px;
        font-weight: 750;

        color: #ffffff !important;

        margin-bottom: 8px;
    }

    .condition-detail {
        font-size: 15px;
        line-height: 1.6;

        color: #e2e8f0 !important;
    }


    /* =====================================================
       AI SECTION
       ===================================================== */

    .ai-header {
        font-size: 21px;
        font-weight: 700;

        color: #ffffff !important;

        margin: 0 0 16px 0;
    }

    .ai-card {
        background:
            linear-gradient(
                135deg,
                rgba(124, 58, 237, 0.15),
                rgba(99, 102, 241, 0.08)
            );

        border: 1px solid rgba(167, 139, 250, 0.24);

        border-radius: 20px;

        padding: 26px;

        margin-bottom: 24px;

        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);

        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.25);
    }

    .ai-card h3 {
        color: #ffffff !important;

        font-size: 18px !important;

        line-height: 1.45 !important;

        margin-top: 20px !important;

        margin-bottom: 9px !important;
    }

    .ai-card h3:first-child {
        margin-top: 0 !important;
    }

    .ai-card p {
        color: #e2e8f0 !important;

        font-size: 15px !important;

        line-height: 1.75 !important;

        margin-top: 7px !important;

        margin-bottom: 12px !important;
    }

    .ai-card ul {
        margin-top: 6px !important;

        margin-bottom: 15px !important;

        padding-left: 22px !important;
    }

    .ai-card li {
        color: #e2e8f0 !important;

        font-size: 15px !important;

        line-height: 1.7 !important;

        margin-bottom: 5px !important;
    }

    .ai-card strong {
        color: #ffffff !important;
    }


    /* =====================================================
       STREAMLIT MARKDOWN
       ===================================================== */

    [data-testid="stMarkdownContainer"] p {
        color: #e2e8f0;
    }

    [data-testid="stMarkdownContainer"] li {
        color: #e2e8f0;
    }

    [data-testid="stMarkdownContainer"] strong {
        color: #ffffff;
    }

    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {
        color: #ffffff !important;
    }


    /* =====================================================
       ALERTS
       ===================================================== */

    [data-testid="stAlert"] {
        border-radius: 14px !important;

        background: rgba(255, 255, 255, 0.07) !important;

        border: 1px solid rgba(255, 255, 255, 0.13) !important;

        color: #ffffff !important;
    }

    [data-testid="stAlert"] p {
        color: #e2e8f0 !important;

        font-size: 15px !important;
    }


    /* =====================================================
       SPINNER
       ===================================================== */

    [data-testid="stSpinner"] {
        color: #e2e8f0 !important;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {
        text-align: center;

        color: #cbd5e1 !important;

        font-size: 14px;

        line-height: 1.6;

        margin-top: 35px;

        padding-top: 22px;

        border-top:
            1px solid rgba(255, 255, 255, 0.10);
    }


    /* =====================================================
       RESPONSIVE
       ===================================================== */

    @media (max-width: 850px) {

        .hero-title {
            font-size: 34px;
        }

        .weather-grid {
            grid-template-columns:
                repeat(2, minmax(0, 1fr));
        }
    }


    @media (max-width: 560px) {

        .block-container {
            padding-left: 18px !important;
            padding-right: 18px !important;
            padding-top: 28px !important;
        }

        .hero-title {
            font-size: 28px;
        }

        .hero-subtitle {
            font-size: 15px;
        }

        .glass-card {
            padding: 20px;
        }

        .weather-grid {
            grid-template-columns: 1fr;
        }

        .weather-value {
            font-size: 22px;
        }

        .ai-card {
            padding: 20px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# API CONFIGURATION
# =========================================================

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)


# =========================================================
# LOCATION
# =========================================================

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
            timeout=15
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

    except requests.RequestException:
        return None, "Unable to connect to the location service."


# =========================================================
# WEATHER
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

        response = requests.get(
            url,
            params=params,
            timeout=15
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

    except requests.RequestException:
        return None, "Unable to connect to the weather service."


# =========================================================
# GEMINI ANALYSIS
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

Consider:

- Temperature
- Feels-like temperature
- Humidity
- Weather condition
- Wind speed
- Atmospheric pressure
- Heat stress
- Cold stress
- Rain
- Storms
- Strong winds
- Poor outdoor conditions
- Other relevant environmental risks

Return exactly these sections:

### Current Situation

Explain what is happening at this specific location.

### Risk Level

Choose exactly ONE:

Low
Moderate
High
Critical

Justify the risk level using the actual weather conditions.

### Important Concerns

Mention only concerns relevant to the current conditions.

### Recommended Actions

Give practical actions that a person at this location should consider.

### Outdoor Activity Advice

Choose exactly ONE:

Generally Safe
Use Caution
Not Recommended

Keep the analysis concise, practical, and location-specific.

Do not claim certainty or emergency-level warnings unless
the actual weather conditions justify them.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text, None

    except Exception as e:

        return None, str(e)


# =========================================================
# CONVERT GEMINI MARKDOWN TO SAFE HTML
# =========================================================

def render_ai_analysis(markdown_text):

    if not markdown_text:
        return ""

    lines = markdown_text.splitlines()

    output = []

    in_list = False

    for line in lines:

        line = line.strip()

        if not line:
            if in_list:
                output.append("</ul>")
                in_list = False

            continue

        # Headings
        if line.startswith("### "):

            if in_list:
                output.append("</ul>")
                in_list = False

            heading = html.escape(
                line[4:].strip()
            )

            output.append(
                f"<h3>{heading}</h3>"
            )

            continue

        # Bullet points
        if line.startswith("- ") or line.startswith("* "):

            if not in_list:
                output.append("<ul>")
                in_list = True

            item = html.escape(
                line[2:].strip()
            )

            item = re.sub(
                r"\*\*(.*?)\*\*",
                r"<strong>\1</strong>",
                item
            )

            output.append(
                f"<li>{item}</li>"
            )

            continue

        # Normal paragraph
        if in_list:
            output.append("</ul>")
            in_list = False

        paragraph = html.escape(line)

        paragraph = re.sub(
            r"\*\*(.*?)\*\*",
            r"<strong>\1</strong>",
            paragraph
        )

        output.append(
            f"<p>{paragraph}</p>"
        )

    if in_list:
        output.append("</ul>")

    return "".join(output)


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">
            🌍 AI Live Situation Intelligence
        </div>

        <div class="hero-subtitle">
            Real-time environmental intelligence powered by Generative AI
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOCATION INPUT
# =========================================================

st.markdown(
    """
    <div class="glass-card">

        <div class="section-title">
            📍 Select Location
        </div>

        <div class="section-description">
            Enter a city to analyze its current environmental
            conditions and receive an AI-powered situation assessment.
        </div>

    """,
    unsafe_allow_html=True
)

city = st.text_input(
    "City",
    placeholder="Example: Lahore, Dubai, London",
    label_visibility="collapsed"
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


analyze_button = st.button(
    "🔍  Analyze Current Situation",
    type="primary"
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze_button:

    if not city.strip():

        st.warning(
            "Please enter a city name."
        )

    else:

        # -------------------------------------------------
        # LOCATION
        # -------------------------------------------------

        with st.spinner("Finding location..."):

            location, location_error = get_location(
                city.strip()
            )

        if location_error:

            st.error(location_error)

        else:

            location_name = location["name"]

            if location["state"]:
                location_name += (
                    f", {location['state']}"
                )

            location_name += (
                f", {location['country']}"
            )

            safe_location_name = html.escape(
                location_name
            )

            st.markdown(
                f"""
                <div class="glass-card">

                    <div class="section-title">
                        📍 Location Detected
                    </div>

                    <div class="location-name">
                        {safe_location_name}
                    </div>

                    <div class="coordinates">
                        Coordinates:
                        {location['latitude']:.4f},
                        {location['longitude']:.4f}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            # -------------------------------------------------
            # WEATHER
            # -------------------------------------------------

            with st.spinner(
                "Getting live weather data..."
            ):

                weather, weather_error = get_weather(
                    location["latitude"],
                    location["longitude"]
                )

            if weather_error:

                st.error(
                    "Unable to retrieve live weather data."
                )

                st.code(weather_error)

            else:

                st.markdown(
                    """
                    <div class="section-title">
                        🌦️ Live Weather
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # -------------------------------------------------
                # WEATHER GRID
                # -------------------------------------------------

                weather_html = f"""
                <div class="weather-grid">

                    <div class="weather-card">
                        <div class="weather-label">
                            Temperature
                        </div>

                        <div class="weather-value">
                            {weather["temperature"]} °C
                        </div>
                    </div>


                    <div class="weather-card">
                        <div class="weather-label">
                            Feels Like
                        </div>

                        <div class="weather-value">
                            {weather["feels_like"]} °C
                        </div>
                    </div>


                    <div class="weather-card">
                        <div class="weather-label">
                            Humidity
                        </div>

                        <div class="weather-value">
                            {weather["humidity"]} %
                        </div>
                    </div>


                    <div class="weather-card">
                        <div class="weather-label">
                            Wind Speed
                        </div>

                        <div class="weather-value">
                            {weather["wind_speed"]} m/s
                        </div>
                    </div>

                </div>
                """

                st.markdown(
                    weather_html,
                    unsafe_allow_html=True
                )


                # -------------------------------------------------
                # CURRENT CONDITION
                # -------------------------------------------------

                safe_description = html.escape(
                    weather["description"].title()
                )

                st.markdown(
                    f"""
                    <div class="condition-card">

                        <div class="condition-label">
                            CURRENT CONDITION
                        </div>

                        <div class="condition-value">
                            {safe_description}
                        </div>

                        <div class="condition-detail">
                            Atmospheric Pressure:
                            {weather["pressure"]} hPa
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # -------------------------------------------------
                # AI ANALYSIS
                # -------------------------------------------------

                st.markdown(
                    """
                    <div class="ai-header">
                        🧠 AI Situation Intelligence
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                with st.spinner(
                    "Gemini is analyzing the current situation..."
                ):

                    analysis, analysis_error = analyze_situation(
                        location,
                        weather
                    )


                if analysis_error:

                    st.error(
                        "Unable to generate AI analysis."
                    )

                    st.code(
                        analysis_error
                    )

                else:

                    analysis_html = render_ai_analysis(
                        analysis
                    )

                    st.markdown(
                        f"""
                        <div class="ai-card">

                            {analysis_html}

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        AI Live Situation Intelligence ·
        Real-time data + Generative AI
    </div>
    """,
    unsafe_allow_html=True
)
