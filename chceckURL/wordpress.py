from bs4 import BeautifulSoup
import re


def check_meta_tag(response):
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tag = soup.find('meta', attrs={'name': 'generator'})
        if meta_tag is not None and 'wordpress' in meta_tag.get('content', '').lower():
            version_match = re.search(r'wordpress\s*(\d+\.\d+(?:\.\d+)?)', meta_tag.get('content', ''),
                                      re.IGNORECASE)
            version = version_match.group(1) if version_match else ''
            return True, version
    return False, None


def check_in_robots_txt(response):
    if response.status_code == 200 and 'wp-admin' in response.text:
        return True
    return False


def check_woocommerce_and_version(response):
    is_w = False
    version = None
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup.find_all('script', src=True):
            if '/woocommerce/' in script['src']:
                version_match = re.search(r'wc.(\d+\.\d+\.\d+)', script['src'])
                version = version_match.group(1) if version_match else None
                is_w = True
                if version != '':
                    break
        if is_w:
            return True, version
    return False, None


def check_woocommerce_js(response):
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        body_tag = soup.find('body')
        if body_tag and 'woocommerce-js' in body_tag.get('class', []):
            return True
    return False

