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

send_but = '//button[@class="_2Ujuu"]'
qr_code = "To use WhatsApp on your computer:"
session_status = {}

try:
  os.mkdir("static")
except:
  pass


def ping_me(ping_freq):
  for i in range(ping_freq):
    requests.get("https://headless-pywhatkit.herokuapp.com")
    time.sleep(1500)


def send(driver,sid,delay):
  print("here")
  delay = int(delay)
  for i in range(404):
    try:
      if qr_code in driver.page_source:
        time.sleep(2)
        driver.save_screenshot('static/%s.png'%sid)
        session_status[sid] = "scan_qr"
      else:
        session_status[sid] = "working"
        but = driver.find_element_by_xpath(send_but)
        if delay > 25:
          pings = delay//25
          threading.Thread(target=lambda:ping_me(pings)).start()
        time.sleep(delay-5)
        but.click()
        time.sleep(10)
        session_status[sid] = "success"
        driver.quit()
        break;
    except:
      pass
 

@app.route('/')
def hello_world():
  return 'Hello, World!'


@app.route("/send")
def sendmsg():
  number = request.args.get("num")
  message = request.args.get("message")
  delay = request.args.get("delay")
  driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

  print(f"https://web.whatsapp.com/send?phone={number}&text={message}")
  driver.get(f"https://web.whatsapp.com/send?phone={number}&text={message}")

  session_id = ""
  for i in range(6):
        session_id = session_id + random.choice(lower_case)

  print(session_id)
  driver.save_screenshot('static/%s.png'%session_id)
  threading.Thread(target=lambda:send(driver,session_id,delay)).start()
  return "https://headless-pywhatkit.herokuapp.com/%s.png"%session_id


@app.route("/session-status")
def stats():
  sess_id = request.args.get("id")
  try:
    return  session_status[sess_id]
  except:
    return "Invalid Session Id"


if __name__ == '__main__':
  app.run(host= '0.0.0.0')
