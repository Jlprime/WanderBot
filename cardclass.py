import requests
import json
import config
from random import randint

class cardClass:
    def __init__(self, lat, long, rad):
        self.weather = weather(lat, long)
        self.eatPlace = place(lat, long, rad, "eat")
        self.visitPlace = place(lat, long, rad, "visit")


def weather(lat, long):
    # Using OpenWeather API, we can derive the current weather conditions of the current place of the user
    lat = lat
    lon = long
    url = "http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, config.WEATHER_API_KEY)

    response = requests.get(url)
    data = json.loads(response.text)
    current = data['weather'][0]['description']
    return current.title()


def place(lat, long, rad, which):
    while True:
        try:
            recommended = []
            def visit():
                typeList = ["aquarium",
                            "art_gallery",
                            "beauty_salon",
                            "clothing_store",
                            "hindu_temple",
                            "library",
                            "mosque",
                            "movie_theater",
                            "museum",
                            "night_club",
                            "painter",
                            "park",
                            "shopping_mall",
                            "spa",
                            "stadium",
                            "synagogue",
                            "tourist_attraction",
                            "zoo"]

                rand = randint(0, len(typeList)-1)
                return typeList[rand]

            def eat():
                typeList = ["bakery",
                            "bar",
                            "cafe",
                            "liquor_store",
                            "meal_takeaway",
                            "restaurant"]

                rand = randint(0, len(typeList) - 1)
                return typeList[rand]

            if which == "eat":
                placeType = eat()
            else:
                placeType = visit()

            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s&radius=%s&type=%s&key=%s" % (
                lat, long, rad, placeType, config.GG_API_KEY)
            response = requests.get(url)
            data = json.loads(response.text)
            for i in range(len(data['results'])):
                if data['results'][i]['rating'] >= 4:
                    recommended.append(data['results'][i])
            rand = randint(0, len(recommended)-1)
            return recommended[rand]
        except:
            pass
        else:
            break


