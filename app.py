from flask import Flask, request, redirect
import threading
import os
from selenium import webdriver


app = Flask('app')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

def send(driver):
  print("here")
  driver.save_screenshot('screenie.png')
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
  threading.Thread(target=lambda:send().start())
  return redirect("headless-pywhatkit.herokuapp.com/screenie.png",302)
  


if __name__ == '__main__':
  app.run(host= '0.0.0.0')
