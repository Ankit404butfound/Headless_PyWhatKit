# from flask import Flask, request, redirect
# import threading
# import os
# import time
# from selenium import webdriver
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.firefox.options import Options as FirefoxOptions


# app = Flask('app',static_url_path='')
# try:
#     os.mkdir("static")
# except:
#     pass


# options = FirefoxOptions()
# #fp = webdriver.FirefoxProfile('/root/.mozilla/firefox/abcdefgh.default')
# #driver = webdriver.Firefox(profile)
# profile = webdriver.FirefoxProfile()
# profile.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Linux i686; rv:77.0) Gecko/20100101 Firefox/77.0")
# options.add_argument('--no-sandbox')
# options.add_argument("--headless")

        


# def send(driver):
#   print("here")
  
#   while True:
#     try:
#       driver.save_screenshot('static/screens.png')
#       but = driver.find_element_by_xpath('//button[@class="_2Ujuu"]')
#       but.click()
#       driver.quit()
#       break;
#     except:
#       pass
    

# @app.route('/')
# def hello_world():
#   return 'Hello, World!'

# @app.route("/send")
# def sendmsg():
#   number = request.args.get("num")
#   driver = webdriver.Firefox(firefox_profile=profile,options=options, executable_path=os.environ.get("GECKODRIVER_PATH"),firefox_binary=os.environ.get("FIREFOX_BIN"))
#   driver.save_screenshot('static/screens.png')
#   driver.get(f"https://web.whatsapp.com/send?phone={number}&text=Hello")
#   threading.Thread(target=lambda:send(driver)).start()
#   print(os.listdir())
#   print(os.listdir())
#   return redirect("https://headless-pywhatkit.herokuapp.com/screens.png",302)
  


# if __name__ == '__main__':
#   app.run(host= '0.0.0.0')


from flask import Flask, request, redirect
import threading
import os

app = Flask('app',static_url_path='')
os.mkdir("static")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux i686; rv:77.0) Gecko/20100101 Firefox/77.0")

def send(driver):
  print("here")
  
  while True:
    try:
      driver.save_screenshot('static/screens.png')
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
  threading.Thread(target=lambda:send(driver).start())
  driver.save_screenshot('static/screens.png')
  return redirect("https://headless-pywhatkit.herokuapp.com/screens.png",302)
  

if __name__ == '__main__':
  app.run(host= '0.0.0.0')
