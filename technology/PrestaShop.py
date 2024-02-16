from bs4 import BeautifulSoup

from technology.Base import Base


class PrestaShop(Base):
    def __init__(self, response, response_robots):
        super().__init__(response, response_robots, "PrestaShop")
        self.is_that = self.check_scripts() or self.check_in_robots_txt()

    def check_in_robots_txt(self):
        if self.response_robots.status_code == 200 and 'Prestashop' in self.response_robots.text:
            return True
        return False

    def check_scripts(self):
        if self.response.status_code == 200:
            soup = BeautifulSoup(self.response.text, 'html.parser')
            script_tags = soup.find_all('script', attrs={'type': 'text/javascript'})

            for script in script_tags:
                script_content = script.text if script.text else script.get('src', '')
                if 'prestashop' in script_content.lower():
                    return True
        return False
