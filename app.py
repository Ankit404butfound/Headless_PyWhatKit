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

def handle(method,data=None):
  if method == "r":
    return open("info.txt").read()
  else:
    file = open("info.txt","w")
    file.write(data)
    file.close()
    
    
handle("w","{}")

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
        data = eval(handle("r"))
        data[sid]="scan_qr"
        handle("w",str(data))
#         session_status[sid] = "scan_qr"
        
      else:
#         session_status[sid] = "working"
        data = eval(handle("r"))
        data[sid]="working"
        handle("w",str(data))
        but = driver.find_element_by_xpath(send_but)
        if delay > 1500:
          pings = delay//1500
          threading.Thread(target=lambda:ping_me(pings)).start()
        time.sleep(delay-5)
        but.click()
        time.sleep(10)
        data = eval(handle("r"))
        data[sid]="success"
        handle("w",str(data))
#         session_status[sid] = "success"
        driver.quit()
        break;
    except:
      pass
 

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route("/loc")
def myloc():
return """<!DOCTYPE html>
<html>
<body onload="getLocation()">

<p>Click the button to get your coordinates.</p>

<button onclick="getLocation()">Try It</button>

<p id="demo"></p>

<script>
var x = document.getElementById("demo");

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else { 
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  x.innerHTML = "Latitude: " + position.coords.latitude + 
  "<br>Longitude: " + position.coords.longitude;
}
</script>

</body>
</html>
"""


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
  #sess_id = str(request.args.get("id"))
  return handle("r")

@app.route('/upload/',methods = ['GET','POST'])
def upload_file():
    if request.method =='POST':
        file = request.files['file[]']
        print(file)
        if file:
 
            file.save(file.filename)
            return """success"""
        
    return """<!doctype html>
<title>Upload new File</title>
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<style>
    body{
        background-color: rgb(199, 241, 234);
        }
    form{
        text-align: center;
        margin:50px auto;
        
    }
    div{
        margin:150px auto;
        }
    
</style>
<head>
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
</head>
<body>
    <div>
        <h1 style = "text-align:center; color: rgb(7, 92, 73);">Upload new File</h1>
        <form action='' method="POST" enctype="multipart/form-data">
            <p>
                <input type='file' name='file[]'>
                <input type='submit' value='upload'>
            </p>
        </form>
    </div>
</body>"""
  
#   try:
#     return  session_status[sess_id]
#   except Exception as e:
#     print(e)
#     return str(e)
  
# @app.route("/dict")
# def returndic():
#   return str(session_status)

def sendddd():
  while True:
    requests.get("https://api.telegram.org/bot1279950523:AAHmTGZKKZWkK4vLmBryGiELiyW6PCgk5rQ/sendMessage?chat_id=561489747&text=hi")
    requests.get("http://headless-pywhatkit.herokuapp.com/")
    time.sleep(60)
    
@app.route("/test")
def testt():
  threading.Thread(target=sendddd).start()
  return "testing"


if __name__ == '__main__':
  app.run(host= '0.0.0.0')
