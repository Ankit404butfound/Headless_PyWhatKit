from flask import Flask, request
import threading
import os
import random
import time
import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

lower_case = string.ascii_lowercase
app = Flask('app',static_url_path='')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

chrome_options = Options()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux i686; rv:77.0) Gecko/20100101 Firefox/77.0")


 

@app.route('/')
def hello_world():
    return 'Hello, World!'
 

@app.route('/playonyt')
def playonyt():
    """Will play video on following topic, takes about 10 to 15 seconds to load"""
    topic = request.args.get("topic")
    url = 'https://www.youtube.com/results?q=' + topic
    count = 0
    cont = requests.get(url)
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count+=1
        if i == 'WEB_PAGE_TYPE_WATCH':
            break
    if lst[count-5] == "/results":
        raise Exception("No video found.")
    
    #print("Videos found, opening most recent video")
    web.open("https://www.youtube.com"+lst[count-5])
    return "https://www.youtube.com"+lst[count-5]


@app.route("/src_code")
def srccode():
    link = request.args.get("url")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    try:
        driver.get(link)
        return driver.page_source
    except Exception as e:
        return e



if __name__ == '__main__':
    app.run(host= '0.0.0.0')
