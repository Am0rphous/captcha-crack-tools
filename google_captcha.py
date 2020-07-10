from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from pynput.mouse import Button, Controller

from bs4 import BeautifulSoup
import numpy as np
import cv2
import requests as R
import time
import random
import json
import os
import ast
import io
#from data_base_work import DataBase
from bson.objectid import ObjectId
import scipy.interpolate as si

class RequestLib():
    def __init__(self):
        self.session = R.session()
        self.session.proxies = {}
        self.session.proxies['http'] = 'socks5://127.0.0.1:9050'
        self.session.proxies['https'] = 'socks5://127.0.0.1:9050'
        self.headers = {}
        self.headers['User-agent'] = UserAgent().random
        self.headers['Accept-Language'] = "en,en-US;q=0,5"
        self.headers['Content-Type'] = "application/x-www-form-urlencoded"
        self.headers['Connection'] = "keep-alive"
        self.headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    def get(self, http):
        #print (http)
        get_page = self.session.get(http, headers=self.headers)#, timeout=(10, 10)) 
        return get_page#.text 

# signal TOR for a new connection
def switchIP():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

# get a new selenium webdriver with tor as the proxy
def my_proxy(PROXY_HOST,PROXY_PORT):
    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks",PROXY_HOST)
    fp.set_preference("network.proxy.socks_port",int(PROXY_PORT))

    fp.update_preferences()
    options = Options()
    #options.add_argument('headless')
    #options.add_argument("--headless")
    #options.headless = True
    return webdriver.Firefox(options=options, firefox_profile=fp)

def scroll():
    w = last_height//1000
    igg = 100
    for i in range(w):
        proxy.execute_script("window.scrollTo(0, {})".format(igg))
        time.sleep(0.3)
        igg += 100
    

#https://www.liveauctioneers.com/search/?keyword=rolex&sort=-relevance&status=archive
#proxy.get("https://www.liveauctioneers.com/search/?keyword=rolex&sort=-relevance&status=online")
#proxy.get("https://www.liveauctioneers.com/search/?keyword=rolex&sort=-saleStart&status=archive")
def imgs(x):
      cv2.imshow('Rotat', np.array(x))
      cv2.waitKey(1)
      #cv2.destroyAllWindows()
#
# Using B-spline for simulate humane like mouse movments
def human_like_mouse_move(action, start_element):

    points = [[6, 2], [3, 2],[0, 0], [0, 2]];
    points = np.array(points)
    x = points[:,0]
    y = points[:,1]


    t = range(len(points))
    ipl_t = np.linspace(0.0, len(points) - 1, 100)


    x_tup = si.splrep(t, x, k=1)
    y_tup = si.splrep(t, y, k=1)

    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

    x_i = si.splev(ipl_t, x_list)
    y_i = si.splev(ipl_t, y_list)

    startElement = start_element

    action.move_to_element(startElement);
    action.perform();

    c = 5
    i = 0
    for mouse_x, mouse_y in zip(x_i, y_i):
        action.move_by_offset(mouse_x,mouse_y);
        action.perform();
        print("Move mouse to, %s ,%s" % (mouse_x, mouse_y))   
        i += 1    
        if i == c:
            break;
            
#proxy.get("https://www.liveauctioneers.com/search/?keyword=rolex&page={}&sort=-saleStart&status=archive".format(iD))  
#proxy.get("https://www.invaluable.com/search?keyword=rolex") #https://www.invaluable.com/
#def main():
def ocr(x):
   pass
if __name__ == "__main__":
        #classdb = DataBase()
        proxy = my_proxy("127.0.0.1", 9050)
        #proxy = my_proxy("198.46.160.38", 8080)
        #proxy = my_proxy('111.111.111.111', 1111)
        Sess = RequestLib()
        proxy.get("https://www.google.com/search?client=ubuntu&channel=fs&q=rolex&ie=utf-8&oe=utf-8")#search?keyword=rolex&upcoming=false

        
#        data = proxy.get_screenshot_as_png()
#        nparr = np.frombuffer(data, np.uint8)
#        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#        imgs(img)
#        cv2.imwrite("newTest.jpg", img)
        proxy.switch_to.frame(proxy.find_elements_by_tag_name("iframe")[0]) 
        check_box = WebDriverWait(proxy, 10).until(EC.element_to_be_clickable((By.ID ,"recaptcha-anchor")))
        time.sleep(5)
        action =  ActionChains(proxy);
        human_like_mouse_move(action, check_box)
        check_box.click() 

        #proxy.find_element_by_css_selector('.rc-image-tile-wrapper')
        #print (el.text)
        #<img class="rc-image-tile-44"
        for fps in range(30):
                data = proxy.get_screenshot_as_png()
                nparr = np.frombuffer(data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                #imgs(img)
        #WebDriverWait(proxy, 1.5).until(EC.presence_of_element_located((By.NAME, "submit"))).click()     
        #proxy.switch_to.frame(proxy.find_elements_by_tag_name("iframe")[0])         
        #verify_button = WebDriverWait(proxy, 10).until(EC.element_to_be_clickable((By.ID ,"recaptcha-verify-button")))
        verify_button = WebDriverWait(proxy, 10).until(EC.element_to_be_clickable((By.ID ,"recaptcha-verify-button")))
        #proxy.find_elements_by_id("recaptcha-verify-button")
        #WebDriverWait(proxy, 10).until(EC.element_to_be_clickable((By.ID ,"recaptcha-verify-button"))).click()
#        sign_in = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign in")))
#sign_in.click()
        #time.sleep(5)
        #proxy.switch_to.frame(proxy.find_elements_by_tag_name("iframe")[0])
        #recaptcha-verify-button
        #verify_button = proxy.find_element_by_xpath(".//*[@id='recaptcha-verify-button']")
        #action =  ActionChains(proxy);
        #human_like_mouse_move(action, verify_button)
        verify_button.click()         
        #ocr(nparr)
        time.sleep(2000)


#mouse = Controller()
#o = cv2.imread("newTest.jpg")

#o = np.array(o)
#o[300:330, 140:170,:] = 2
#mouse.position = (144,315)
#imgs(o)

#mouse.click(Button.left, 1)
#mouse.scroll(0, -100)


#x1 = 144, y1 = 303
#x2 = 170, y1 = 330
#img = Image.open(io.BytesIO(data))
#numpy_array = np.asarray(img) 



