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