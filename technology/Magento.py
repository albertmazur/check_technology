import re

from bs4 import BeautifulSoup

from technology.Base import Base


class Magento(Base):
    def __init__(self, response):
        super().__init__(response, None, "Magento")
        self.is_that = self.check_website()

    def check_website(self):
        if self.response.status_code == 200:
            soup = BeautifulSoup(self.response.text, 'html.parser')
            magento_pattern = re.compile(r'Magento_')
            if magento_pattern.search(soup.prettify()):
                return True
            else:
                return False
        return False
