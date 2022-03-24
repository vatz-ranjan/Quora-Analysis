from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver import Keys
from question import Question
import warnings


def web_scraping(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    entries = soup.findAll('div', attrs={'class': 'ZINbbc luh4tb xpd O9g5cc uUPGi'})
    for entry in entries:
        req_info = entry.findAll('a')[0].attrs['href']
        req_url = req_info[req_info.find('=')+1:req_info.find('&')]
        if 'quora' in req_url:
            new_doubt = Question()
            new_doubt.search(req_url)
            new_doubt.extract_info()
            new_doubt.load_excel()


def task():
    ques_lis = ['post traumatic stress disorder', 'clinical depression', 'depression', 'depressive', 'health', 'world']
    while True:
        ques = ques_lis[0]
        # ques = input("Enter your query: ")
        if len(ques) < 1: continue
        else: break
    search_val = ques + ' quora'
    base_url = 'https://www.google.com/'
    path = 'E:/Application/ChromeDriver/chromedriver.exe'
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(path, options=option)
    driver.get(base_url)
    search = driver.find_element_by_name("q")
    search.send_keys(search_val)
    search.send_keys(Keys.ENTER)
    url = driver.find_element_by_tag_name('HTML')
    web_scraping(url.get_attribute('baseURI'))
    driver.close()


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    task()
