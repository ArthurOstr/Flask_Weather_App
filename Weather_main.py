from flask import Flask, render_template, request
import os
import requests
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# fetch the API key from environment variable
api_key = os.getenv("WEATHER_API_KEY")
# configure the postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# define a model for storing weather search history
class WeatherSearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


#view representation of the model in debugging
    def __repr__(self):
        return f"<WeatherSearch {self.city} - {self.temperature}C - {self.description}>"
with app.app_context():
    db.create_all()
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
            # store the search in the database
            new_entry = WeatherSearch(
                city=city,
                temperature=data["main"]["temp"],
                description=data["weather"][0]["description"].capitalize()
            )
            db.session.add(new_entry)
            db.session.commit()
        else:
            # False - city not found
            weather_data = {
                "error": "city not found"
            }
    recent_searches = WeatherSearch.query.order_by(WeatherSearch.timestamp.desc()).limit(5).all()
    # render the template with weather data
    return render_template("index1.html",weather=weather_data, history=recent_searches)

if __name__ == "__main__":
    app.run(debug=True)