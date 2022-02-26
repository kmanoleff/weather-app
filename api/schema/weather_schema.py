from flask_marshmallow import Schema
from marshmallow.fields import Str


class WeatherSchema(Schema):
    class Meta:
        fields = ['temperature', 'temp_feel', 'low', 'high']

    temperature = Str()
    temp_feel = Str()
    low = Str()
    high = Str()
