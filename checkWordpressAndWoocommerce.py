import csv
import requests

from chceckURL.wordpress import check_in_robots_txt, check_meta_tag, check_woocommerce_and_version, \
    check_woocommerce_js, wordpress_email

column_url = 0
path_input = 'pl.txt'
path_output = 'website-results-with-email.csv'
start_line = 100000
count_line = 5000


def addHttp(url):
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


file_extension = path_input.split('.')[-1].lower()
if file_extension == 'csv':
    with open(path_input, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        list_url = [row[column_url] for row in reader][start_line-1:start_line-1+count_line]
elif file_extension == 'txt':
    list_url = read_urls_from_txt(path_input, start_line, count_line)
else:
    raise ValueError("Unsupported file format. Please use a .csv or .txt file.")

with open(path_output, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["URL", "IS WordPress", "Version WordPress", "IS WooCommerce", "Version WooCommerce", "E-mail"])

    total_lines = start_line + count_line
    for index, url in enumerate(list_url, start=1):
        print(url)
        is_wp = None
        is_wp2 = None
        is_wc = None
        is_wc2 = None
        try:
            url = addHttp(url)
            response = requests.get(url, timeout=60)
            responseRobots = requests.get(url + '/robots.txt', timeout=60)
            is_wp, wp_version = check_meta_tag(response)
            is_wp2 = check_in_robots_txt(responseRobots)
            is_wc, wc_version = check_woocommerce_and_version(response)
            is_wc2 = check_woocommerce_js(response)

            if is_wc:
                is_wp = True
            main_is_wp = is_wp or is_wp2
            main_is_wc = is_wc or is_wc2

            wp_email = wordpress_email(main_is_wp, url)

        except requests.RequestException as e:
            print("Brak dostępu do strony: " + str(e))

        wp_result = f"WordPress" if main_is_wp else ""
        wp_result_version = f"{wp_version}" if main_is_wp and wp_version is not None else ""
        wc_result = f"WooCommerce" if main_is_wc else ""
        wc_result_version = f"{wc_version}" if main_is_wc and wc_version is not None else ""
        wp_result_email = f"{', '.join(wp_email)}" if wp_email is not None else ""

        writer.writerow([url, wp_result, wp_result_version, wc_result, wc_result_version, wp_result_email])
        progress = (index / count_line) * 100
        print(f"Przetworzono {start_line + index - 1}/{total_lines} ({progress:.2f}%)")
