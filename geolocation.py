import os

import telebot
from telebot.types import ChatLocation
from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="@hnrwanderbot")

def location (message):
    lat = message.location.latitude
    long = message.location.longitude
    cityLocation = geolocator.reverse('{} {}'.format(lat, long))
    return cityLocation.address