from flask import Flask, render_template, request
import os
api_key = os.getenv("WEATHER_API_KEY")
import requests
from dotenv import load_dotenv
# load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# fetch the API key from environment variable
api_key = os.getenv("WEATHER_API_KEY")
@app.route("/", methods=["GET", "POST"])
def home():
    """
    Home route to display weather information based on user input city.
    GET - empty search bar which records input(city name)
    POST - fetches weather data from OpenWeather API and displays it.
    """
    weather_data = None
    if request.method == "POST":
        # get city name from form
        city = request.form.get("city_name")
        # construct the API URL
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        # make a GET request to the API
        response = requests.get(url)
        if response.status_code == 200:
            # True - parse the JSON response
            data = response.json()
            weather_data = {
                "city": city,
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"].capitalize()
            }
        else:
            # False - city not found
            weather_data = {
                "error": "city not found"
            }
    # render the template with weather data
    return render_template("index1.html",**(weather_data or {}))

if __name__ == "__main__":
    app.run(debug=True)