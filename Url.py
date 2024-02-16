import requests


class Url:
    def __init__(self, page_home):
        self.page_home = page_home
        self.add_http()

    def add_http(self):
        if not self.page_home.startswith('http') and not self.page_home.startswith('https'):
            self.page_home = 'http://' + self.page_home
        if self.page_home.endswith('/'):
            self.page_home = self.page_home[:-1]

    def create_request(self, url=''):
        page_url = self.page_home + url
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        try:
            return requests.get(page_url, headers=headers, timeout=30)
        except requests.exceptions.SSLError:
            print("Nie działa SSL")
            return requests.get(page_url, headers=headers, timeout=30, verify=False)
        except requests.RequestException as e:
            print("Brak dostępu do strony: " + str(e))
