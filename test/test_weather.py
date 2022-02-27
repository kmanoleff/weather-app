from unittest import TestCase

from requests import codes

from app import create_app


class TestWeather(TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_weather(self):
        rv = self.app.get('/api/weather?city=Hampton&state=VA&country=USA')
        self.assertEqual(rv.status_code, codes.ok)
