import csv
import requests

import untils
from chceckURL import joomla, wordpress, prestaShop
from untils import add_http, read_urls_from_txt, read_urls_from_csv

column_url = 0
path_input = 'pl.txt'
path_output = 'website-results.csv'
start_line = 670000
count_line = 100


def main(url, verify):
    if verify is True:
        print(url)
    technology = None
    title = None
    emails = None
    try:
        url = add_http(url)
        response = untils.create_request(url, verify)
        response_robots = untils.create_request(url + '/robots.txt', verify)
        is_wp, wp_version = wordpress.check_meta_tag(response)
        is_wp2 = wordpress.check_in_robots_txt(response_robots)
        is_wc, wc_version = wordpress.check_woocommerce_and_version(response)
        is_wc2 = wordpress.check_woocommerce_js(response)

        if is_wc:
            is_wp = True
        main_is_wp = is_wp or is_wp2
        main_is_wc = is_wc or is_wc2
        if main_is_wp:
            technology = "WordPress"

        is_joomla = joomla.check_script_class(response)
        is_joomla2 = joomla.check_in_robots_txt(response_robots)
        if is_joomla or is_joomla2:
            technology = "Joomla"

        is_presta_shop = prestaShop.check_in_robots_txt(response_robots)
        is_presta_shop2 = prestaShop.check_scripts(response)
        if is_presta_shop or is_presta_shop2:
            technology = "PrestaShop"

        if technology is not None:
            emails = untils.get_emails(url, verify)
            title = untils.get_title(response)

        wp_result_version = f"{wp_version}" if main_is_wp is True and wp_version is not None else ""
        wc_result = f"WooCommerce" if main_is_wc else ""
        wc_result_version = f"{wc_version}" if main_is_wc is True and wc_version is not None else ""
        result_title = title if title is not None else ""

        if emails is not None:
            row_data = [url, technology, wp_result_version, wc_result, wc_result_version, result_title] + emails
            writer.writerow(row_data)
        else:
            writer.writerow([url, technology, wp_result_version, wc_result, wc_result_version, result_title, ""])
        progress = (index / count_line) * 100
        print(f"Przetworzono {start_line + index - 1}/{total_lines} ({progress:.2f}%)")

    except requests.exceptions.SSLError as e:
        print("Nie działa SSL")
        main(url, False)
    except requests.RequestException as e:
        print("Brak dostępu do strony: " + str(e))
        writer.writerow([url])


file_extension = path_input.split('.')[-1].lower()
if file_extension == 'csv':
    list_url = read_urls_from_csv(path_input, start_line, count_line, column_url)
elif file_extension == 'txt':
    list_url = read_urls_from_txt(path_input, start_line, count_line)
else:
    raise ValueError("Unsupported file format. Please use a .csv or .txt file.")

with open(path_output, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["URL", "Technology", "Version WordPress", "IS WooCommerce", "Version WooCommerce", "Company", "E-mail"])

    total_lines = start_line + count_line
    for index, url in enumerate(list_url, start=1):
        main(url, True)
