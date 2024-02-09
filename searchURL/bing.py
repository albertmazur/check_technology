import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=options))
search_url = 'https://www.bing.com/search?q=sklep&sp=-1&ghc=1&lq=0&pq=sklep&sc=11-5&qs=n&sk=&cvid=44DCC3BD873E476C862E3598171F7531&ghsh=0&ghacc=0&ghpl=&FPIG=A4E46250F5C8404B92C6E57BDC58FD60&first=1&FORM=PQRE1'
driver.get(search_url)
driver.maximize_window()


def getAndSaveUrl():
    links = driver.find_elements(By.TAG_NAME, "cite")
    unique_urls = set()
    with open('url_bing.txt', 'a') as file:
        for link in links:
            full_text = link.get_attribute("textContent")

            clean_url = re.sub(r' › .+$', '', full_text)

            if clean_url not in unique_urls:
                unique_urls.add(clean_url)
                print(clean_url)
                file.write(clean_url + '\n')


def getNavNextLink():
    while True:
        getAndSaveUrl()
        try:
            time.sleep(5)
            linkNext = driver.find_element(By.CLASS_NAME, 'sb_pagN')
            print(linkNext.get_attribute("outerHTML"))
            linkNext.click()
        except NoSuchElementException as e:
            break



button = driver.find_element("xpath", "//a[contains(text(),'Akceptuj')]")
button.click()
getNavNextLink()
