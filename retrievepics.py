import config

def retrievePics (reference):
    url = "https://maps.googleapis.com/maps/api/place/photo?maxheight=250&photo_reference=%s&key=%s" % (reference, config.GG_API_KEY)
    return url

    # print(url)
    # response = requests.get(url)
    # file = open("sample_image.png","wb")
    # file.write(response.content)
    # file.close()