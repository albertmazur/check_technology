from bs4 import BeautifulSoup

from technology.Base import Base


class Joomla(Base):
    def __init__(self, response, response_robots):
        super().__init__(response, response_robots, "Joomla")
        self.is_that = self.check_script_class() or self.check_in_robots_txt()

    def check_script_class(self):
        if self.response.status_code == 200:
            soup = BeautifulSoup(self.response.text, 'html.parser')
            script_tag = soup.find('script', attrs={'type': 'application/json', 'class': 'joomla-script-options'})
            if script_tag is not None:
                return True
        return False

    def check_in_robots_txt(self):
        if self.response.status_code == 200 and '/joomla/administrator/' in self.response.text:
            return True
        return False
