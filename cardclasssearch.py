import requests
import json
import config
from random import randint, choice

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
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s&type=%s" % (
            city, config.GG_API_KEY, placeType)
        print(url)
        response = requests.get(url)
        data = json.loads(response.text)
        if data['status'] != 'ZERO_RESULTS':
            for i in range(len(data['results'])):
                if ('rating' in data['results'][i]) and (data['results'][i]['rating'] >= 4):
                    added.append(data['results'][i])
            return added
        else:
            return []

    vis_res, eat_res, recommended, count = {}, {}, [], 0
    if which == "visit":
        while (not recommended and count != 10):
            recommended = generate(vis_generator())
            count += 1
            if count == 10:
                return {}
        rand = randint(0, len(recommended) - 1)
        vis_res = recommended[rand]
        return vis_res
    else:
        while (not recommended and count != 10):
            recommended = generate(eat_generator())
            count += 1
            if count == 10:
                return {}
        rand = randint(0, len(recommended) - 1)
        eat_res = recommended[rand]
        return eat_res