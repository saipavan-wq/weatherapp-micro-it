import streamlit as st
import requests
import plotly.graph_objs as go
from datetime import datetime

# ✅ Use your API key here
API_KEY = "849a0a013f9e618ea222050aecae68bd"

def get_weather(city):
    # 🛠 Correct API URL with metric units
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def main():
    st.set_page_config(page_title="🌦️ Big Weather App", layout="centered")
    st.title("🌍 Weather Forecast App")
    st.markdown("Enter a city name to get current weather and a 5-day forecast.")

    city = st.text_input("City Name", "Hyderabad")

    if city:
        data = get_weather(city)

        if data.get("cod") != "200":
            st.error("❌ City not found or API error! Please try again.")
            return

        current = data["list"][0]
        st.subheader(f"📍 Current Weather in {city.title()}")
        st.metric("🌡 Temperature", f"{current['main']['temp']} °C")
        st.metric("💧 Humidity", f"{current['main']['humidity']} %")
        st.metric("🌬 Wind Speed", f"{current['wind']['speed']} m/s")
        st.markdown(f"**Condition:** {current['weather'][0]['description'].title()}")

        # Optional: Sunrise/Sunset
        sunrise = datetime.utcfromtimestamp(data['city']['sunrise']).strftime('%H:%M:%S')
        sunset = datetime.utcfromtimestamp(data['city']['sunset']).strftime('%H:%M:%S')
        st.write(f"🌅 Sunrise: {sunrise} UTC")
        st.write(f"🌇 Sunset: {sunset} UTC")

        # 5-day forecast chart
        st.subheader("📈 5-Day Temperature Forecast (3-hour intervals)")
        temps = [entry["main"]["temp"] for entry in data["list"]]
        times = [entry["dt_txt"] for entry in data["list"]]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=times, y=temps, mode='lines+markers', name='Temperature (°C)'))
        fig.update_layout(xaxis_title='Date & Time', yaxis_title='Temperature (°C)', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
