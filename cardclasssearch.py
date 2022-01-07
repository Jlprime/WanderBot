import requests
import json
import config
from random import randint, choice
from reversegeo import geocoder_radius

class cardClassSearch:
    def __init__(self, city):
        self.weather = weather(city)
        self.eatPlace = place(city, "eat")
        self.visitPlace = place(city, "visit")


def weather(city):
    # Using OpenWeather API, we can derive the current weather conditions of the current place of the user
    url = "http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s" % (city, config.WEATHER_API_KEY)
    response = requests.get(url)
    data = json.loads(response.text)
    current = data['weather'][0]['description']
    return current.title()

def place(city, which):

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
        return choice(visTypeList)

    def eat_generator():
        return choice(eatTypeList)

    def generate(placeType):
        added = []
        try:
            cityDetails = geocoder_radius(city)
        except:
            return []
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s&radius=%s&type=%s&key=%s" % (
            cityDetails[0], cityDetails[1], cityDetails[2], placeType, config.GG_API_KEY)
        response = requests.get(url)
        data = json.loads(response.text)
        if data['status'] != 'ZERO_RESULTS':
            for i in range(len(data['results'])):
                if ('rating' in data['results'][i]) and (data['results'][i]['rating'] >= 4):
                    added.append(data['results'][i])
            return added
        else:
            return []

    recommended, count = [], 0
    if which == "visit":
        while (not recommended and count != 10):
            recommended = generate(vis_generator())
            count += 1
            if count == 10:
                return {}
        rand = randint(0, len(recommended) - 1)
        res = recommended[rand]
        print(res)
        return res
    else:
        while (not recommended and count != 10):
            recommended = generate(eat_generator())
            count += 1
            if count == 10:
                return {}
        rand = randint(0, len(recommended) - 1)
        res = recommended[rand]
        print(res)
        return res