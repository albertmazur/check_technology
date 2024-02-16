import re

from bs4 import BeautifulSoup

from Url import Url


class Base:
    def __init__(self, response, response_robots, name):
        self.is_that = None
        self.name = name
        self.response = response
        self.response_robots = response_robots
        self.url = Url(self.response.url)

    def get_is_that(self):
        return self.is_that

    def get_title(self):
        if self.response.status_code == 200:
            soup = BeautifulSoup(self.response.text, 'html.parser')
            title_tag = soup.title
            if title_tag:
                title_text = title_tag.get_text().strip()
                title_text = re.sub(r'(Strona główna\s*-\s*|Home\s*-\s*|\s*-\s*Strona główna|\s*-\s*Home)', '',
                                    title_text,
                                    flags=re.IGNORECASE)
                title_text = title_text.strip()
                return title_text

    def get_emails(self):
        emails_set = set()

        def add_emails(response):
            nonlocal emails_set
            soup = BeautifulSoup(response.text, 'html.parser')
            email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

            for tag in soup.find_all(True):
                tag_text = tag.string
                if tag_text:
                    emails = re.findall(email_pattern, tag_text)
                    emails_set.update(emails)

            for tag in soup.find_all(True):
                tag_text = ' '.join(tag.stripped_strings)
                emails = re.findall(email_pattern, tag_text)
                emails_set.update(emails)

        def check_page(response):
            if response.status_code == 200:
                add_emails(response)

        check_page(self.url.create_request())
        check_page(self.url.create_request('/contact'))
        check_page(self.url.create_request('/kontakt'))
        check_page(self.url.create_request('/kontakt-2'))
        check_page(self.url.create_request('/skontaktuj-sie-z-nami'))

        if emails_set:
            return list(emails_set)
        else:
            return None
