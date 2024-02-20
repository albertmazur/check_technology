from FileHandler import FileHandler
from Url import Url
from technology import Joomla, Wordpress, PrestaShop

column_url = 0
path_input = 'pl.txt'
path_output = 'website-results.csv'
start_line = 670000
count_line = 100


def check(page_home_url):
    print(page_home_url)

    url = Url(page_home_url)
    response = url.create_request()
    response_robots = url.create_request('/robots.txt')
    wordpress = Wordpress.Wordpress(response, response_robots)
    joomla = Joomla.Joomla(response, response_robots)
    presta_shop = PrestaShop.PrestaShop(response, response_robots)

    if wordpress.is_that_wp:
        return wordpress.get_result()
    elif joomla.is_that:
        return joomla.get_result()
    elif presta_shop.is_that:
        return presta_shop.get_result()
    else:
        return [url.page_home]


def main2():
    file_handler = FileHandler(path_input, path_output, start_line, count_line, column_url)

    file_handler.writer_header_to_csv(
        ["URL", "Technology", "Version WordPress", "IS WooCommerce", "Version WooCommerce", "Company", "E-mail"])

    lines = file_handler.lines

    total_lines = start_line + count_line - 1
    for index, url in enumerate(lines):
        progress = (index / count_line) * 100
        print(f"Przetworzono {start_line + index}/{total_lines} ({progress:.2f}%)")
        data = check(url)
        file_handler.writer(data)


main2()
