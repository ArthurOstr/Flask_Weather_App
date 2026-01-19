import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")

city = "Kyiv"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

print(f"Connecting to OpenWeather for {city}...")
response = requests.get(url)

print(f"Status code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    print("---------------------------")
    print(f"Weather Report for {city}:")
    print(f"Temperature: {temp} C")
    print(f"Description: {desc.capitalize()}")
    print("---------------------------")
else:
    print(f"Error code: {response.status_code}")