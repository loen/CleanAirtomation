import json
import os
import unittest
from unittest import mock

from requests import RequestException

from clean_airtomation.airly_dao import AirlyDao

current_directory = os.path.dirname(__file__)

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    with open(os.path.join(current_directory, 'http_responses/response_200.json')) as f:
        json_200 = json.load(f)
    with open(os.path.join(current_directory, 'http_responses/response_400.json')) as f:
        json_400 = json.load(f)
    print(args[0])
    if args[0] == 'https://airapi.airly.eu/v2/measurements/installation?installationId=4444':
        return MockResponse(json_200, 200)
    elif args[0] == 'https://airapi.airly.eu/v2/measurements/installation?installationId=666':
        return MockResponse(json_400, 400)
    elif args[0] == 'https://airapi.airly.eu/v2/measurements/installation?installationId=888':
        raise RequestException()
    return MockResponse(None, 404)


class AirlyDaoTest(unittest.TestCase):

    @mock.patch('requests.get', mocked_requests_get)
    def test_request_with_proper_installationId(self):
        airlyDao = AirlyDao('https://airapi.airly.eu', 'API_KEY', 4444)
        self.assertEqual(airlyDao.caqi(), 44.44)

    @mock.patch('requests.get', mocked_requests_get)
    def test_request_with_invalid_installationId(self):
        airlyDao = AirlyDao('https://airapi.airly.eu', 'API_KEY', 666)
        self.assertIsNone(airlyDao.caqi())

    @mock.patch('requests.get', mocked_requests_get)
    def test_request_with_timeout(self):
        airlyDao = AirlyDao('https://airapi.airly.eu', 'API_KEY', 888)
        self.assertIsNone(airlyDao.caqi())
