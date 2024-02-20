import os

from dotenv import load_dotenv

from FileHandler import FileHandler
from Url import Url
from technology import Joomla, Wordpress, PrestaShop


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


class Main:
    def __init__(self):
        load_dotenv()
        self.column_url = os.getenv("COLUMN_URL")
        self.path_input = os.getenv("PATH_INPUT")
        self.path_output = os.getenv("PATH_OUTPUT")
        self.start_line = int(os.getenv("START_LINE"))
        self.count_line = int(os.getenv("COUNT_LINE"))

        file_handler = FileHandler(self.path_input, self.path_output, self.start_line, self.count_line, self.column_url)
        file_handler.writer_header_to_csv(
            ["URL", "Technology", "Version WordPress", "IS WooCommerce", "Version WooCommerce", "Company", "E-mail"])

        lines = file_handler.lines
        total_lines = self.start_line + self.count_line - 1
        for index, url in enumerate(lines):
            progress = (index / self.count_line) * 100
            print(f"Przetworzono {self.start_line + index}/{total_lines} ({progress:.2f}%)")
            data = check(url)
            file_handler.writer(data)


Main()
