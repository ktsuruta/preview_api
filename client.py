import requests
import ast

url = 'https://python.civic-apps.com/http-request-post-get/'
response = requests.post('http://127.0.0.1:5000', data={'url': url})
preview = ast.literal_eval(response.text)
print(preview)
print(preview['og_img'])
