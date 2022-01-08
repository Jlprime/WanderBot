import os


def retrievePics (reference):
    url = "https://maps.googleapis.com/maps/api/place/photo?maxheight=250&photo_reference=%s&key=%s" % (reference, os.getenv('GG_TOKEN') )
    return url