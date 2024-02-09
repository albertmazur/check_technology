import requests
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


def wordpress_email(is_wp, url):
    if is_wp:
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

        response_home = requests.get(url, timeout=60)
        if response_home.status_code == 200:
            add_emails(response_home)

        response_en = requests.get(url + '/contact', timeout=60)
        if response_en.status_code == 200:
            add_emails(response_en)

        response_pl = requests.get(url + '/kontakt', timeout=60)
        if response_pl.status_code == 200:
            add_emails(response_pl)

        response_pl = requests.get(url + '/kontakt-2', timeout=60)
        if response_pl.status_code == 200:
            add_emails(response_pl)

        response_pl = requests.get(url + '/skontaktuj-sie-z-nami', timeout=60)
        if response_pl.status_code == 200:
            add_emails(response_pl)

        if emails_set:
            return list(emails_set)
        else:
            return None

    return None
