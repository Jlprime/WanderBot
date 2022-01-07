import requests
import json
import config
from Pillow import Image

def retrievePics (reference):
    url = "https://maps.googleapis.com/maps/api/place/photo?photo_reference=%s&key=%s" % (reference, config.GG_API_KEY)
    response = requests.get(url)
    img = Image.open(response)
    img.show()

retrievePics('Aap_uEDCjcNufVxAviCKqoYSzYn2CjPVgmyIVPoeg-OSPTLsXkrQP8Ifz0J3NzWE-kLKJr29x8pliuPHcm4szRGwzvFLLPsVMZsL_FYjpVrwLwXQhoVBFi2-6OcNmJN-riqb9SsDdRIQXeS0-5sURbfC7dXB6Ft4UtOJbn8NZ4jmYOIfXsdB')