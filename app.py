from distutils import extension
from flask import Flask, request

from bs4 import BeautifulSoup
from selenium import webdriver
import hashlib
import urllib.error
import urllib.request

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

def _download_file(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file:
            data = web_file.read()
            with open(dst_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
        print(e)

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
    twitter_image = soup.find('meta', attrs={'property': 'twitter:image', 'content': True})
    hs = hashlib.md5(url.encode()).hexdigest()
    if og_img is not None:
        extension = og_img.get('content').split("?")[0].split("/")[-1].split(".")[1]
        images_dst = "/images/{file_name}.{extension}".format(file_name=hs, extension=extension)
        _download_file(og_img.get('content'),images_dst)
        result['image'] = "http://localhost/{file_name}.{extension}".format(file_name=hs, extension=extension)
    elif twitter_image is not None:
        result['image'] = twitter_image.get('content')
    else:
        result['image'] = "http://localhost/{file_name}.png".format(file_name=hs)
        
    # get width and height of the page
    w = driver.execute_script("return document.body.scrollWidth;")
    h = 1080
    # set window size
    driver.set_window_size(w,h)
    FILENAME = "/images/{file_name}.png".format(file_name=hs)

    driver.save_screenshot(FILENAME)
    
    driver.quit()
    return result
    