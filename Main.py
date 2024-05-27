import os
from dotenv import load_dotenv
from multiprocessing import Pool
from FileHandler import FileHandler
from Url import Url
from technology import Joomla, Wordpress, PrestaShop, Magento


def check(page_home_url):
    print(page_home_url)
    url = Url(page_home_url)
    response = url.create_request()
    if response.status_code != 404:
        response_robots = url.create_request('/robots.txt')

        platforms = [
            Wordpress.Wordpress(response, response_robots),
            Joomla.Joomla(response, response_robots),
            PrestaShop.PrestaShop(response, response_robots),
            Magento.Magento(response),
        ]

        for platform in platforms:
            if platform.is_that:
                return platform.get_result()

    return None


class Main:
    def __init__(self):
        load_dotenv()
        self.column_url = os.getenv("COLUMN_URL")
        self.path_input = os.getenv("PATH_INPUT")
        self.path_output = os.getenv("PATH_OUTPUT")
        self.start_line = int(os.getenv("START_LINE"))
        self.count_line = int(os.getenv("COUNT_LINE"))

        self.file_handler = FileHandler(self.path_input, self.path_output, self.start_line, self.count_line, self.column_url)
        self.file_handler.writer_header_to_csv(
            ["URL", "Technology", "Version WordPress", "IS WooCommerce", "Version WooCommerce", "Company", "E-mail"]
        )

    def process_urls(self, urls):
        with Pool(processes=os.cpu_count()) as pool:
            results = pool.map(check, urls)
            self.file_handler.writer(results)
            print(f"Zapisano do pliku")


if __name__ == '__main__':
    main_instance = Main()
    main_instance.process_urls(main_instance.file_handler.lines)
