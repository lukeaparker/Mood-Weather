from flask import Flask, render_template, request
import requests
import os
import json 
from os import environ 
from pymongo import MongoClient

# Import enviorment variables
API_KEY = environ.get('API_KEY')
URI = environ.get('URI')

# Setup database
client = MongoClient(URI)
db = client.get_default_database()
samples = db.samples 

app = Flask(__name__, static_url_path='/static')

# Landing page 
@app.route('/')
def landing():
    return render_template('landing.html')

# Survey view 
@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    base_url = 'https://api.openweathermap.org/data/2.5/weather?'
    url = base_url + "q=" + city + "&units=imperial" + "&appid=" + API_KEY
    print(url)
    response = requests.get(url)
    data = response.json()
    icon = data['weather'][0]['icon']
    temp = int(data['main']['temp'])
    description = data['weather'][0]['description']
    return render_template('weather.html', description=description, temp=temp, city=city, icon=icon)

# Record sample
@app.route('/record-sample/<city>/<temperture>/<weather>/<mood>', methods=['GET'])
def record_sample(city, temperture, weather, mood):
    samples.insert_one({
        'city': city,
        'temperture': temperture,
        'weather': weather,
        'mood': mood
    })
    return render_template('landing.html')

    
