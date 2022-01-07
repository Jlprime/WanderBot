import requests
import json
import config
from random import randint, choice

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

    visTypeList = ["aquarium",
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

    eatTypeList = ["bakery",
                "bar",
                "cafe",
                "liquor_store",
                "meal_takeaway",
                "restaurant"]

    def vis_generator():
        while True:
            yield choice(visTypeList)

    def eat_generator():
        while True:
            yield choice(eatTypeList)

    def generate(placeType):
        added = []
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s&radius=%s&type=%s&key=%s" % (
            lat, long, rad, placeType, config.GG_API_KEY)
        response = requests.get(url)
        data = json.loads(response.text)
        if data['status'] != 'ZERO_RESULTS':
            for i in range(len(data['results'])):
                if ('rating' in data['results'][i]) and (data['results'][i]['rating'] >= 4):
                    added.append(data['results'][i])
            return added
        else:
            return []

    vis_res, eat_res, recommended = {}, {}, []
    if which == "visit":
        while not recommended:
            recommended = generate(vis_generator())
        rand = randint(0, len(recommended) - 1)
        vis_res = recommended[rand]
        # DEBUG: print(vis_res)
        return vis_res
    else:
        while not recommended:
            recommended = generate(eat_generator())
        rand = randint(0, len(recommended) - 1)
        eat_res = recommended[rand]
        # DEBUG: print(eat_res)
        return eat_res
