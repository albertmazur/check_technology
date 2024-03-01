from bs4 import BeautifulSoup
import re

from technology.Base import Base


class Wordpress(Base):

    def __init__(self, response, response_robots):
        super().__init__(response, response_robots, "Wordpress")

        is_wp, self.wp_version = self.check_meta_tag()
        is_wp2 = self.check_in_robots_txt()
        is_wc, self.wc_version = self.check_woocommerce_and_version()
        is_wc2 = self.check_woocommerce_js()

        if is_wc:
            is_wp = True
        self.is_that = is_wp or is_wp2
        self.is_that_wc = is_wc or is_wc2

    def check_meta_tag(self):
        if self.response.status_code == 200:
            soup = BeautifulSoup(self.response.text, 'html.parser')
            meta_tag = soup.find('meta', attrs={'name': 'generator'})
            if meta_tag is not None and 'wordpress' in meta_tag.get('content', '').lower():
                version_match = re.search(r'wordpress\s*(\d+\.\d+(?:\.\d+)?)', meta_tag.get('content', ''),
                                          re.IGNORECASE)
                version = version_match.group(1) if version_match else ''
                return True, version
        return False, ""

    def check_in_robots_txt(self):
        if self.response_robots.status_code == 200 and 'wp-admin' in self.response_robots.text:
            return True
        return False

    def check_woocommerce_and_version(self):
        is_w = False
        version = ""
        if self.response.status_code == 200:
            soup = BeautifulSoup(self.response.text, 'html.parser')
            for script in soup.find_all('script', src=True):
                if '/woocommerce/' in script['src']:
                    version_match = re.search(r'wc.(\d+\.\d+\.\d+)', script['src'])
                    version = version_match.group(1) if version_match else ""
                    is_w = True
                    if version != '':
                        break
            if is_w:
                return True, version
        return False, ""

    def check_woocommerce_js(self):
        if self.response.status_code == 200:
            soup = BeautifulSoup(self.response.text, 'html.parser')
            body_tag = soup.find('body')
            if body_tag and 'woocommerce-js' in body_tag.get('class', []):
                return True
        return False

    def get_result(self):
        return [self.url.page_home, self.name, self.wp_version, "WooCommerce" if self.is_that_wc is True else "",
                self.wc_version, self.get_title()] + self.get_emails()
