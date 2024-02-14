import csv
import re

import requests
from bs4 import BeautifulSoup


def create_request(url_page, verify):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    if verify is False:
        return requests.get(url_page, headers=headers, timeout=30, verify=verify)
    else:
        return requests.get(url_page, headers=headers, timeout=30)


def add_http(url):
    if not url.startswith('http') and not url.startswith('https'):
        url = 'http://' + url
    if url.endswith('/'):
        url = url[:-1]
    return url


def read_urls_from_txt(file_path, start_line=1, count_line=None):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        end_line = (start_line-1) + count_line if count_line is not None else len(lines)
        return [line.strip() for line in lines[start_line-1:end_line] if line.strip()]


def read_urls_from_csv(path_input, start_line=1, count_line=None, column_url=0):
    with open(path_input, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        return [row[column_url] for row in reader][start_line - 1:start_line - 1 + count_line]


def get_emails(url, main_verify):
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

    def check_page(url_page, verify):
        response = create_request(url_page, verify)
        if response.status_code == 200:
            add_emails(response)

    check_page(url, main_verify)
    check_page(url + '/contact', main_verify)
    check_page(url + '/kontakt', main_verify)
    check_page(url + '/kontakt-2', main_verify)
    check_page(url + '/skontaktuj-sie-z-nami', main_verify)

    if emails_set:
        return list(emails_set)
    else:
        return None


def get_title(response):
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.title
        if title_tag:
            title_text = title_tag.get_text().strip()
            title_text = re.sub(r'(Strona główna\s*-\s*|Home\s*-\s*|\s*-\s*Strona główna|\s*-\s*Home)', '', title_text,
                                flags=re.IGNORECASE)
            title_text = title_text.strip()
            return title_text
