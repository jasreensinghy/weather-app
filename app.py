from flask import Flask, render_template, request
import configparser
import requests
from datetime import datetime

app = Flask(__name__)
app.debug = True


@app.route('/')
def weather_dashboard():
    return render_template('home.html')


@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    temp_units = request.form['temp_units']
    api_key = get_api_key()
    if temp_units == 'F':
        data = get_weather_results_imperial(zip_code, api_key)
        temp = data["main"]["temp"]
    else:hj
        data = get_weather_results_metric(zip_code, api_key)
        temp = data["main"]["temp"]
    print (data)
    icon = data["weather"][0]["icon"]
    iconurl = "https://openweathermap.org/img/w/" + icon + ".png"
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]
    sunrise = data["sys"]["sunrise"]
    dt_obj = datetime.fromtimestamp(int(sunrise))
    now = datetime.now()
    print(now)
    offset = data["timezone"]
    utc = datetime.utcnow()
    local_time = utc offset
    print(local_time)
    #change into timestamp
    #add offset to utc (+)
    #convert back to datetime
    return render_template('results.html',
                           location=location, temp=temp, temp_units=temp_units, iconurl=iconurl, dt_obj=dt_obj,
                           feels_like=feels_like, weather=weather, sunrise=sunrise )

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results_imperial(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()

def get_weather_results_metric(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


if __name__ == '__main__':
    app.run()
