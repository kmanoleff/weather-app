from http import HTTPStatus

from flasgger import swag_from
from flask import Blueprint, request

from api.model.error_model import ErrorModel
from api.model.weather_model import WeatherModel
from api.schema.error_schema import ErrorSchema
from api.schema.weather_schema import WeatherSchema
from api.service import weather_service

weather_api = Blueprint('api', __name__)


@weather_api.route('/weather', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'city',
            'in': 'query',
            'type': 'string',
            'required': 'true',
            'description': 'City name'
        },
        {
            'name': 'state',
            'in': 'query',
            'type': 'string',
            'required': 'true',
            'description': 'Two-letter state code'
        },
        {
            'name': 'country',
            'in': 'query',
            'type': 'string',
            'enum': [
                'USA',
                'CAN',
                'MEX'
            ],
            'default': 'USA',
            'description': 'Country code'
        }
    ],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Weather Response',
            'schema': WeatherSchema
        },
        HTTPStatus.BAD_REQUEST.value: {
            'description': 'Error Response',
            'schema': ErrorSchema
        }
    }
})
def get_weather():
    """
    Get weather for location
    Uses city, state, country to get weather for location
    Note country param is not required but if not provided will default to USA; city / state required
    ---
    """
    city = request.args.get('city')
    state = request.args.get('state')
    if None in (city, state):
        err = ErrorModel('city / state query params are required')
        return ErrorSchema().dump(err), 400

    country = request.args.get('country')
    if country is None:
        country = 'USA'
    elif country not in ('USA', 'MEX', 'CAN'):
        err = ErrorModel('invalid country code; valid values : USA, MEX, CAN')
        return ErrorSchema().dump(err), 400

    # geocode city, state, country to lat / lon first...
    geocode_results = weather_service.geocode(city=city, state=state, country=country)
    if geocode_results is None or len(geocode_results) == 0:
        err = ErrorModel('city, state, country cannot be geocoded')
        return ErrorSchema().dump(err), 400

    # ...then get the weather data
    weather_data = weather_service.retrieve_weather(lat=geocode_results[0]['lat'], lon=geocode_results[0]['lon'])
    if weather_data is None:
        err = ErrorModel('weather cannot be retrieved for city, state, country')
        return ErrorSchema().dump(err), 400

    result = WeatherModel(temperature=weather_data['temp'], temp_feel=weather_data['feels_like'],
                          low=weather_data['temp_min'], high=weather_data['temp_max'])
    return WeatherSchema().dump(result), 200
