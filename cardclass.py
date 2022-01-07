import requests
import json

def cardClass(lat, long):
    def __init__(self):
        self.weather = weather(lat, long)
        #self.eatPlace = eatPlace(lat, long)
        #self.visitPlace = visitPlace(lat, long)

def weather(lat, long):
    #Using OpenWeather API, we can derive the current weather conditions of the current place of the user
    api_key = "5649fe25da87c63923302dbd96adf26e"
    lat = lat
    lon = long
    url = "http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)

    response = requests.get(url)
    data = json.loads(response.text)
    current = data['weather'][0]['description']
    return current.title()