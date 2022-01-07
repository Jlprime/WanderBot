import requests
import json

def cardClass(lat, long):
    def __init__(self):
        self.weather = weather(lat, long)
        self.eatPlace = eatPlace(lat, long)
        self.visitPlace = visitPlace(lat, long)

def weather(lat, long):
    api_key = "5649fe25da87c63923302dbd96adf26e"
    lat = lat
    lon = long
    url = "api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s" % (lat, lon, api_key)

    response = requests.get(url)
    data = json.loads(response.text)
    print(data)
    #current = data["çurrent"]["weather"]["main"]
    #return current

#weather(1.3521,103.8198)