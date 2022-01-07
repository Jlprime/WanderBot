from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="wanderbot")

def reverse_geocoder(lat,long):
    location = geolocator.reverse(f'{lat},{long}')
    address = location.raw['address']
    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')
    # code = address.get('country_code')
    # zipcode = address.get('postcode')

    full_address = f'{city}, {state}, {country}'.strip(', ')

    return full_address

def geocoder_radius(city):
    location = geolocator.geocode(city)
    bounding = location.raw['boundingbox']
    x = abs(float(bounding[0]) - float(bounding[1]))
    y = abs(float(bounding[2]) - float(bounding[3]))
    if x <= y:
        x *= 111139
        return [location.raw['lat'], location.raw['lon'], x/2]
    else:
        y *= 111139
        return [location.raw['lat'], location.raw['lon'], y/2]