import json
import unittest
from unittest import mock

from CleanAirtomation.AirlyDao import AirlyDao


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    with open('./http_responses/response_200.json') as f:
        json_200 = json.load(f)
    with open('./http_responses/response_400.json') as f:
        json_400 = json.load(f)
    print(args[0])
    if args[0] == 'https://airapi.airly.eu/v2/measurements/installation?installationId=4444':
        return MockResponse(json_200, 200)
    elif args[0] == 'https://airapi.airly.eu/v2/measurements/installation?installationId=666':
        return MockResponse(json_400, 400)
    return MockResponse(None, 404)


class AirlyDaoTest(unittest.TestCase):
    @mock.patch('requests.get', mocked_requests_get)
    def test_request_wit_proper_installationId(self):
        airlyDao = AirlyDao('API_KEY', 4444)
        self.assertEquals(airlyDao.caqi(), 44.44)
