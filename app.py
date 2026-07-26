import streamlit as st
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from config import API_KEY

from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="SkyCast Pro",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)
with st.sidebar:

     selected = option_menu(
         menu_title="🌦️ Skycast Pro",
         options=[
            "Weather",
            "About"
         ],

         icons=[
            "cloud-sun",
            "person-circle"
         ],

         default_index=0
        
    )
     st.markdown("---")

     #favourite cities

     st.subheader("⭐ Favorite Cities")

     favorite_city = st.selectbox(
       "Choose a city",
      [
        "None",
        "Delhi",
        "Mumbai",
        "Jammu",
        "Bengaluru",
        "London",
        "New York",
        "Tokyo",
        "Dubai"
      ]
)
    

     if favorite_city != "None":
        st.session_state["city"] = favorite_city



     st.markdown("---")

    # API STATUS
     st.subheader("📡 API Status")
     st.success("🟢 Connected")

    #  Current Time
     st.subheader("🕒 Current Time")

     current_time = datetime.now(ZoneInfo("Asia/Kolkata"))

     st.write(current_time.strftime("%I:%M %p"))

    # 📅 Today's Date
     st.subheader("📅 Today's Date")

     st.write(current_time.strftime("%d %B %Y"))

     st.markdown("---")

    # ℹ️ App Info
     st.subheader("ℹ️ App Information")

     st.write("**🌦️ SkyCast Pro v1.0**")
     st.write("👨‍💻 Developer: Lakshay Sharma")
     st.write("🐍 Built with Python & Streamlit")

     st.markdown("---")

     st.caption("Made by Lakshay Sharma")

if selected == "Weather":

#-------------- HERO SECTION --------------#

    st.title("🌦️ SkyCast Pro")

    st.caption("Professional Real-Time Weather Forecast Application")

    st.markdown("---")

    left_col, right_col = st.columns([3, 1])

    with left_col:

        city = st.text_input(
            "📍Enter City Name",
            value = st.session_state.get("city", ""),
            placeholder="Example: Delhi, Mumbai, London"
        )

    with right_col:

        st.write("")
        st.write("")

        search = st.button(
            "🔍 Search",
            use_container_width=True
        )

    st.markdown("---")

    #------------- API REQUEST --------------#

    if search:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        with st.spinner("🔄 Fetching latest weather..."):

         response = requests.get(url)
         data = response.json()

        if data["cod"] != 200:
         st.error("❌ City not found! Please enter a valid city name.")
         st.stop()

        if "history" not in st.session_state:
         st.session_state.history = []

        if city not in st.session_state.history:
         st.session_state.history.insert(0, city)

    #---------------- WEATHER VARIABLES --------------

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        feels_like = data["main"]["feels_like"]
        pressure = data["main"]["pressure"]
        city_name = data["name"]
        country = data["sys"]["country"]
        wind_speed = data["wind"]["speed"]
        description = data["weather"][0]["description"]
        icon = data["weather"][0]["icon"]

        icon_url = f"https://openweathermap.org/img/wn/{icon}@4x.png"

        latitude = data["coord"]["lat"]
        longitude = data["coord"]["lon"]
        sunrise = data["sys"]["sunrise"]
        sunset = data["sys"]["sunset"]
        visibility = data["visibility"]

        timezone_offset = data["timezone"]
        
        sunrise_time = datetime.utcfromtimestamp(sunrise + timezone_offset).strftime("%I:%M %p")
        sunset_time = datetime.utcfromtimestamp(sunset + timezone_offset).strftime("%I:%M %p")

        current_hour = datetime.now().hour

        if current_hour < 12:
         greeting = "🌅 Good Morning"
        elif current_hour < 17:
         greeting = "☀️ Good Afternoon"
        elif current_hour < 20:
         greeting = "🌇 Good Evening"
        else:
         greeting = "🌙 Good Night"

        st.success(f"📍Weather Found for {city_name}, {country}")

        with st.container(border=True):

         st.header(greeting)

        left, right = st.columns([2,1])
        with left:
         st.subheader(f"📍 {city_name}, {country}")
         st.write(f"### 🌤️ {description.title()}")
         st.title(f"🌡️ {temperature:.1f}°C")

        with right:
         st.image(icon_url, width=200)

        st.markdown("---")

        with st.container(border=True):
            st.subheader("📊 Weather Highlights")
            st.caption("Live weather information fetched from OpenWeather API")

        
        col1, col2, col3, col4 = st.columns(4)

        with st.container(border=True):

            st.subheader("🌍 Additional Information")

        col5, col6, col7, col8 = st.columns(4)

        with col1:
         st.metric("🌡️ Temperature", f"{temperature:.1f} °C")

        with col2:
         st.metric("💧 Humidity", f"{humidity}%")

        with col3:
         st.metric("🌬️ Wind", f"{wind_speed} m/s")

        with col4:
         st.metric("☁️ Condition", description.title())

        with col5:
         st.metric("🥵 Feels Like", f"{feels_like:.1f} °C")

        with col6:
         st.metric("🌅 Sunrise", sunrise_time)

        with col7:
         st.metric("🌇 Sunset", sunset_time)

        with col8:
         st.metric("👁️ Visibility", f"{visibility/1000:.1f} km")

        st.markdown("---")
        st.subheader("💡 Weather Recommendation")
        
        if temperature >= 35:
            st.warning("🥵 It's very hot! Stay hydrated and avoid direct sunlight.")

        elif temperature >= 25:
            st.info("😎 Pleasant weather. A great time to go outside!")

        elif temperature >= 15:
            st.success("🌤️ Cool and comfortable weather. Enjoy your day!")

        else:
            st.error("🥶 It's cold outside. Wear warm clothes!")

# Rain recommendation
        if "rain" in description.lower():
            st.info("☔ Don't forget to carry an umbrella!")

# Snow recommendation
        if "snow" in description.lower():
            st.info("❄️ Snowfall expected. Stay warm!")

# Strong wind
        if wind_speed > 10:
            st.warning("💨 Strong winds detected. Be careful outdoors.")

        st.markdown("---")
        st.subheader("📊 Weather Overview")

        st.write("🌡️ Temperature")
        st.progress(min(int((temperature / 50) * 100), 100))

        st.write("💧 Humidity")
        st.progress(humidity)

        st.write("👁️ Visibility")
        st.progress(min(int((visibility / 10000) * 100), 100))

        st.write("🌬️ Wind Speed")
        st.progress(min(int((wind_speed / 20) * 100), 100))

elif selected == "About":

  st.title("ℹ️ About Project")

  st.info("""
      **SkyCast Pro v1.0**

     👨‍💻 Developer: Lakshay Sharma

     🌤️ Real-Time Weather Forecast Application

     🛠️ Technologies:
      • Python,
      • Streamlit,
      • OpenWeather API

     📅 Version: 1.0
        """)

    
