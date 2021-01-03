from flask import Flask, request, redirect
import threading
import os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options as FirefoxOptions


app = Flask('app',static_url_path='')
try:
    os.mkdir("static")
except:
    pass


options = FirefoxOptions()
fp = webdriver.FirefoxProfile("kaliprofile")
options.add_argument('--no-sandbox')
options.add_argument("--headless")
        


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
  driver = webdriver.Firefox(firefox_profile=fp, options=options, executable_path=os.environ.get("GECKODRIVER_PATH"),firefox_binary=os.environ.get("FIREFOX_BIN"))

  driver.get(f"https://web.whatsapp.com/send?phone={number}&text=Hello")
  threading.Thread(target=lambda:send(driver)).start()
  print(os.listdir())
  driver.save_screenshot('static/screenie.png')
  print(os.listdir())
  return redirect("https://headless-pywhatkit.herokuapp.com/screenie.png",302)
  


if __name__ == '__main__':
  app.run(host= '0.0.0.0')
