from flask import Flask, request

from bs4 import BeautifulSoup
from selenium import webdriver


app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def get_preview():
    if request.method == 'POST':
        url = request.form['url']
    else:
        url = 'https://note.com/npaka/n/n5c3e4ca67956#dGbkR'
    result = _get_preview(url)
    print(result)
    if result is None:
        return "Error"
    else:
        return result


def _get_preview(url):
    print("start process")
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor="http://selenium-hub:4444/wd/hub",
        options=chrome_options
    )
    result = {}
    print("start process")

    driver.get(url)
    html = driver.page_source.encode('utf-8')    
    soup = BeautifulSoup(html, 'html.parser')

    print("start parse")
    title = soup.find('title').text
    print(title)
    result['title'] = title

    description = soup.find('meta', attrs={'name': 'description'})
    if description is not None:
        result['description'] = description.get('content')
        
    og_img = soup.find('meta', attrs={'property': 'og:image', 'content': True})
    if og_img is not None:
        result['og_img'] = og_img.get('content')

    twitter_image = soup.find('meta', attrs={'property': 'twitter:image', 'content': True})
    if twitter_image is not None:
        result['twitter_image'] = twitter_image.get('content')
    driver.quit()
    return result
    