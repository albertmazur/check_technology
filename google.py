import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=options))
search_url = 'https://www.google.pl/search?q=site%3Apl+intitle%3A%22sklep+internetowy%22+OR+intitle%3A%22e-sklep%22+OR+intitle%3A%22internetowy+sklep%22+OR+inurl%3A%22sklep-online%22+OR+inurl%3A%22sklep%22+OR+inurl%3A%22shop%22+OR+inurl%3A%22produkty%22+-oferta+-tworzenie+-stw%C3%B3rz+-wskaz%C3%B3wek+-za%C5%82%C3%B3%C5%BC+-za%C5%82o%C5%BCenie+-integracje&sca_esv=600284955&hl=pl&sxsrf=ACQVn0_SIuBO3QkcRPOpWmQkPGp24QzMDw%3A1705877820061&source=hp&ei=PKGtZZFerP3A8A_r3b5Q&iflsig=ANes7DEAAAAAZa2vTAuo9u60bK0hGPTwiSr66fi-JlxG&udm=&ved=0ahUKEwiR7PeLyu-DAxWsPhAIHeuuDwoQ4dUDCA0&uact=5&oq=site%3Apl+intitle%3A%22sklep+internetowy%22+OR+intitle%3A%22e-sklep%22+OR+intitle%3A%22internetowy+sklep%22+OR+inurl%3A%22sklep-online%22+OR+inurl%3A%22sklep%22+OR+inurl%3A%22shop%22+OR+inurl%3A%22produkty%22+-oferta+-tworzenie+-stw%C3%B3rz+-wskaz%C3%B3wek+-za%C5%82%C3%B3%C5%BC+-za%C5%82o%C5%BCenie+-integracje&gs_lp=Egdnd3Mtd2l6Iu8Bc2l0ZTpwbCBpbnRpdGxlOiJza2xlcCBpbnRlcm5ldG93eSIgT1IgaW50aXRsZToiZS1za2xlcCIgT1IgaW50aXRsZToiaW50ZXJuZXRvd3kgc2tsZXAiIE9SIGludXJsOiJza2xlcC1vbmxpbmUiIE9SIGludXJsOiJza2xlcCIgT1IgaW51cmw6InNob3AiIE9SIGludXJsOiJwcm9kdWt0eSIgLW9mZXJ0YSAtdHdvcnplbmllIC1zdHfDs3J6IC13c2thesOzd2VrIC16YcWCw7PFvCAtemHFgm_FvGVuaWUgLWludGVncmFjamUyBhCzARiFBDIKEC4YAxiPARjqAjIKEAAYAxiPARjqAjIKEAAYAxiPARjqAjIKEC4YAxiPARjqAjIKEAAYAxiPARjqAjIKEAAYAxiPARjqAjIKEC4YAxiPARjqAjIKEC4YAxiPARjqAjIKEAAYAxiPARjqAjIKEAAYAxiPARjqAkjYClDJAVjJAXABeACQAQCYAQCgAQCqAQC4AQPIAQD4AQL4AQGoAgs&sclient=gws-wiz'
driver.get(search_url)
driver.maximize_window()

button = driver.find_elements("xpath", "//div[contains(text(),'Zaakceptuj wszystko')]")
button[1].click()
time.sleep(2)
for x in range(50):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)
    link = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Więcej wyników"]')
    try:
        link.click()
    except Exception as e:
        print("Błąd")

links = driver.find_elements(By.TAG_NAME, "cite")
unique_urls = set()
with open('url_google.txt', 'a') as file:
    for link in links:
        full_text = link.get_attribute("textContent")

        clean_url = re.sub(r' › .+$', '', full_text)

        if clean_url not in unique_urls:
            unique_urls.add(clean_url)
            print(clean_url)
            file.write(clean_url + '\n')
