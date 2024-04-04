import os
import re

import requests
import urllib3
from requests import Response, RequestException


class Url:
    def __init__(self, page_home):
        self.slug_country = os.path.basename(os.getenv("PATH_INPUT")).split('.')[0]
        self.page_home = page_home
        self.add_http()

    def add_http(self):
        if not self.page_home.startswith('http') and not self.page_home.startswith('https'):
            self.page_home = 'https://' + self.page_home
        if self.page_home.endswith('/'):
            self.page_home = self.page_home[:-1]

    def create_request(self, url=''):
        page_url = self.page_home + url
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        try:
            return requests.get(page_url, headers=headers, timeout=15)
        except requests.exceptions.SSLError:
            print("Nie działa SSL")
            try:
                return requests.get(page_url, headers=headers, timeout=15, verify=False)
            except (RequestException, urllib3.exceptions.LocationParseError):
                return self.helper_request(page_url)
        except (RequestException, urllib3.exceptions.LocationParseError):
            return self.helper_request(page_url)

    def helper_request(self, page_url):
        print("Brak dostępu do strony")
        response = Response
        response.url = page_url
        response.status_code = 404
        return response

    def extract_domain(self):
        domain_pattern = r'https?://(?:www\.)?([\w.-]+)'
        domains = re.findall(domain_pattern, self.page_home)

        if domains:
            domain_parts = domains[0].split('.')
            return domain_parts[-1]
        else:
            return None
