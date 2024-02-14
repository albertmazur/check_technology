from bs4 import BeautifulSoup


def check_in_robots_txt(response):
    if response.status_code == 200 and 'Prestashop' in response.text:
        return True
    return False


def check_scripts(response):
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tags = soup.find_all('script', attrs={'type': 'text/javascript'})

        for script in script_tags:
            script_content = script.text if script.text else script.get('src', '')
            if 'prestashop' in script_content.lower():
                return True
    return False
