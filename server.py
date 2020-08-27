from flask import Flask, render_template,request
import requests

app = Flask(__name__)


###################################################################################

@app.route('/')
def show_homepage():
    """display form for input."""
    return render_template('homepage.html')


@app.route('/getWeather', methods=["POST"])
def get_weather_update():
    """return response weather update."""
    latitude = request.form.get("lat")
    longitude = request.form.get("long")

    lat = int(float(latitude))
    long = int(float(longitude))

    if lat < -90 or lat > 90 or long < -180 or long > 180:
        return "Invalid co-ordinates please input correct co-ordinates"

    get_uri = "https://api.weather.gov/points/{},{}".format(latitude, longitude)
    data_response = requests.get(url=get_uri)
    data = data_response.json()
    uri = data['properties']['forecast']

    forecast_response = requests.get(url=uri)

    f = forecast_response.json()
    current_forecast = f['properties']['periods'][0]
    forecast = current_forecast['detailedForecast']
    temperature = current_forecast['temperature']
    return {"forecast": forecast,
            "temperature": temperature}

####################################################################################

if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
    app.debug = True