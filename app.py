from flask import Flask, request, redirect
import threading
import os
from selenium import webdriver


app = Flask('app',static_url_path='')
try:
    os.mkdir("static")
except:
    pass

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("user-agent=Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

def send(driver):
  print("here")
  
  while True:
    try:
      but = driver.find_element_by_xpath('//button[@class="_2Ujuu"]')
      but.click()
      break;
    except:
      pass
    

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route("/send")
def sendmsg():
  number = request.args.get("num")
  driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
  driver.get(f"https://web.whatsapp.com/send?phone={number}&text=Hello")
  threading.Thread(target=lambda:send(driver)).start()
  print(os.listdir())
  driver.save_screenshot('static/screenie.png')
  print(os.listdir())
  return redirect("https://headless-pywhatkit.herokuapp.com/screenie.png",302)
  


if __name__ == '__main__':
  app.run(host= '0.0.0.0')
