from flask import Flask, request

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc


app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def hellp_world():
    if request.method == 'POST':
        url = request.form['url']
    else:
        url = 'https://note.com/npaka/n/n5c3e4ca67956#dGbkR'
    soup = _get_soup(url)
    print(soup)
    result = _get_meta_image(soup)
    print(result)
    if result is None:
        return "No image"
    else:
        return result.split("?")[0]

def _get_soup(url):
    options = Options()    
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("start-maximized")
    driver = uc.Chrome(options=options)
    
    driver.get(url)

    # HTMLを文字コードをUTF-8に変換してから取得します。
    html = driver.page_source.encode('utf-8')    
    soup = BeautifulSoup(html, 'html.parser')
    
    return soup
    
def _get_meta_image(soup):
    
    target_sources = ['twitter:image','og:image']
    taregt_attributes = ['property', 'name']
    for target_source in target_sources:
        for target_attribute in taregt_attributes:
            for meta_tag in soup.find_all('meta', attrs={target_attribute: target_source}):
                return meta_tag.get('content')
