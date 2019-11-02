import requests
import logging
from lxml import html
from logging.config import fileConfig


class CalendarDao:

    def __init__(self, url):
        fileConfig('logging_config.ini')
        self.logger = logging.getLogger()
        self.url = url

    def is_holiday(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                tree = html.fromstring(response.content)
                text = tree.xpath("//span[contains(@class,'dc_feasts')]/span/text()")
                if len(text) > 0:
                    print(text[0])
                    return True
                else:
                    return False
            else:
                return False
        except requests.exceptions.RequestException:
            self.logger.info('Unable to connect to kalendarzswiat.pl')
            return False
