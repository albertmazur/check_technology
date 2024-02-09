from bs4 import BeautifulSoup


def check_script_class(response):
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', attrs={'type': 'application/json', 'class': 'joomla-script-options'})
        if script_tag is not None:
            return True
    return False


def check_wordpress_in_robots_txt(response):
    if response.status_code == 200 and '/joomla/administrator/' in response.text:
        return True
    return False
