import os
import unittest
from unittest import mock

from requests import RequestException

from clean_airtomation.calendar_dao import CalendarDao

current_directory = os.path.dirname(__file__)


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, content, status_code):
            self.content = content
            self.status_code = status_code

        def content(self):
            return self.content

    with open(os.path.join(current_directory, 'http_responses/isHoliday.html')) as f:
        html_is_holiday = f.read()
    with open(os.path.join(current_directory, 'http_responses/isNotHoliday.html')) as f:
        html_is_not_holiday = f.read()
    print(args[0])
    if args[0] == 'https://kalendarzswiat.pl/isHoliday':
        return MockResponse(html_is_holiday, 200)
    elif args[0] == 'https://kalendarzswiat.pl/isNotHoliday':
        return MockResponse(html_is_not_holiday, 200)
    elif args[0] == 'https://kalendarzswiat.pl/error':
        raise RequestException()
    return MockResponse(None, 404)


class TestCalendarDao(unittest.TestCase):

    @mock.patch('requests.get', mocked_requests_get)
    def test_request_is_Holiday(self):
        calendar_dao = CalendarDao('https://kalendarzswiat.pl/isHoliday')
        result = calendar_dao.is_holiday()
        self.assertTrue(result)

    @mock.patch('requests.get', mocked_requests_get)
    def test_request_is_not_Holiday(self):
        calendar_dao = CalendarDao('https://kalendarzswiat.pl/isNotHoliday')
        result = calendar_dao.is_holiday()
        self.assertFalse(result)

    @mock.patch('requests.get', mocked_requests_get)
    def test_request_is_Error(self):
        calendar_dao = CalendarDao('https://kalendarzswiat.pl/error')
        result = calendar_dao.is_holiday()
        self.assertFalse(result)
