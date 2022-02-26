from flask_marshmallow import Schema
from marshmallow.fields import Str


class ErrorSchema(Schema):
    class Meta:
        fields = ['error_message']

    error_message = Str()
