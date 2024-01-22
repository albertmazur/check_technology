import requests
from bs4 import BeautifulSoup
import re
import csv

row_url = 0
path_input = 'pl.txt'
path_output = 'website-results.csv'


def addHttp(url):
    if not url.startswith('http') or not url.startswith('https'):
        url = 'http://' + url
    if url.endswith('/'):
        url = url[:-1]
    return url


def check_wordpress_meta_tag(response):
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tag = soup.find('meta', attrs={'name': 'generator'})
        if meta_tag is not None and 'wordpress' in meta_tag.get('content', '').lower():
            version_match = re.search(r'wordpress\s*(\d+\.\d+(?:\.\d+)?)', meta_tag.get('content', ''),
                                      re.IGNORECASE)
            version = version_match.group(1) if version_match else ''
            return True, version
    return False, None


def check_wordpress_in_robots_txt(response):
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


def read_urls_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]


file_extension = path_input.split('.')[-1].lower()
if file_extension == 'csv':
    with open(path_input, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        list_url = [row[row_url] for row in reader]
elif file_extension == 'txt':
    list_url = read_urls_from_txt(path_input)
else:
    raise ValueError("Unsupported file format. Please use a .csv or .txt file.")

with open(path_output, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["URL", "IS WordPress", "Version WordPress", "IS WooCommerce", "Version WooCommerce"])

    for index, url in enumerate(list_url, start=1):
        print(url)
        try:
            response = requests.get(addHttp(url), timeout=60)
            is_wp, wp_version = check_wordpress_meta_tag(response)
            is_wp2 = check_wordpress_in_robots_txt(response)
            is_wc, wc_version = check_woocommerce_and_version(response)
            is_wc2 = check_woocommerce_js(response)
            if is_wc:
                is_wp = True
        except requests.RequestException as e:
            print("Brak dostępu do strony: " + str(e))

        main_is_wp = is_wp or is_wp2
        main_is_wc = is_wc or is_wc

        wp_result = f"WordPress" if main_is_wp else ""
        wp_result_version = f"{wp_version}" if main_is_wp and wp_version is not None else ""
        wc_result = f"WooCommerce" if main_is_wc else ""
        wc_result_version = f"{wc_version}" if main_is_wc and wc_version is not None else ""

        writer.writerow([url, wp_result, wp_result_version, wc_result, wc_result_version])

        progress = (index / len(list_url)) * 100
        print(f"Przetworzono {index}/{len(list_url)} ({progress:.2f}%)")
