import config

def retrievePics (reference):
    url = "https://maps.googleapis.com/maps/api/place/photo?maxheight=250&photo_reference=%s&key=%s" % (reference, config.GG_API_KEY)
    return url