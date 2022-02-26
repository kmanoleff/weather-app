import requests


def geocode(city, state, country):
    query_string_param = city + ',' + state + ',' + country
    response = requests.get('http://api.openweathermap.org/geo/1.0/direct?q=' + query_string_param +
                            '&limit=1&appid=a24cd5475e04ba00bf005899b2214d69')
    if response.status_code == 200:
        return response.json()
    else:
        return None


def retrieve_weather(lat, lon):
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?lat=' + str(lat) + '&lon=' + str(lon) +
                            '&appid=a24cd5475e04ba00bf005899b2214d69&units=imperial')
    if response.status_code == 200:
        r = response.json()
        if 'main' in r:
            return r['main']
        return None
    else:
        return None
