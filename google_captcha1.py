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
import base64
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
 
def imgs(x):
    cv2.imshow("Image", x) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()
   
def cutimg(data, col):
	if True:
                im_w, im_h, im_c = data.shape
                w, h = im_w//col, im_h//col
                w_num, h_num = int(im_w/w), int(im_h/h)
                num = 0
                ls = []
                try: 
                        #print "post>"
                        for wi in range(0, w_num):
                           for hi in range(0, h_num):
                                num += 1
                                
                                imgs(data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :])
                        return ls
                except IndexError: 
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
        #proxy1 = proxy
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
        
        #--->verify_button = WebDriverWait(proxy, 10).until(EC.element_to_be_clickable((By.ID ,"recaptcha-verify-button")))
        time.sleep(4) 
        action =  ActionChains(proxy);
        human_like_mouse_move(action, check_box)
        #proxy.find_elements_by_id("recaptcha-verify-button")
        #WebDriverWait(proxy, 10).until(EC.element_to_be_clickable((By.ID ,"recaptcha-verify-button"))).click()
#        sign_in = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign in")))
#sign_in.click()
        #time.sleep(5)
        #proxy.switch_to.frame(proxy.find_elements_by_tag_name("iframe")[0])
        #recaptcha-verify-button
        #verify_button = proxy.find_element_by_xpath(".//*[@id='recaptcha-verify-button']")
        
        #proxy.switch_to.frame(proxy.find_elements_by_tag_name("iframe")[0]) 
        proxy.switch_to.default_content()
        iframes = proxy.find_elements_by_tag_name("iframe")
        proxy.switch_to.frame(iframes[2])
        #action =  ActionChains(proxy);
        #human_like_mouse_move(action, verify_button)
        #time.sleep(20)
        #search_btn = WebDriverWait(proxy1, 20).until( EC.presence_of_element_located((By.ID ,"recaptcha-verify-button")))
        search_btn = WebDriverWait(proxy, 4).until(EC.element_to_be_clickable((By.XPATH ,'//button[@id="recaptcha-verify-button"]'))) 
        action =  ActionChains(proxy);
        human_like_mouse_move(action, search_btn)
        #proxy.implicitly_wait(10)
        # Wait again
        #time.sleep(20)
        search_btn.click() # click on submit
        
        #print ("NEXT>>>>>>>>>>>>>>>>>>", proxy.page_source)
        html = proxy.page_source
        soup = BeautifulSoup(html, features = "html.parser")
        J = soup.find_all('td', {"class": "rc-imageselect-tile"})
        JJ = soup.find('img', {"class" : "rc-image-tile-33"})
        JJJ = soup.find('img', {"class" : "rc-image-tile-44"})
        #print (html, len(J), JJ, JJJ)#["src"]
        t_temp = ""
        t_type = ""
        if JJ != None:
           t_temp = JJ["src"]
           t_type = 3
           #print (JJ["src"])
        if JJJ != None: 
           t_temp = JJJ["src"] 
           t_type = 4 
           #print (JJJ["src"])#
        Sess = RequestLib()
        Sess.headers['User-agent'] = UserAgent().random
        response = Sess.get(t_temp)
        print (t_temp, response, len(J), t_type)
        if response.status_code == 200:
           #jpg_original = base64.b64decode(response.content)
           nparr = np.fromstring(response.content, np.uint8)
           img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
           #print (img_np.shape)
           
           ids = proxy.find_elements_by_xpath('//td[@class="rc-imageselect-tile"]')
           #btn_t = WebDriverWait(proxy, 4).until(EC.element_to_be_clickable((By.XPATH ,'//td[@class="rc-imageselect-tile"]')))
          
           ids[3].click()
           #cutimg(img_np, t_type)
            
           #imgr = cv2.imread(response.content)
           print (ids[3],len(ids))
           #with open("t_temp.jpg", 'wb') as fli:
           #    fli.write(response.content)  
        #time.sleep(20)
        #self.wait_between(LONG_MIN_RAND, LONG_MAX_RAND) # wait again
        #--->verify_button.click()
                
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

#    </script><div id="rc-anchor-container" class="rc-anchor rc-anchor-normal rc-anchor-light"><div id="recaptcha-accessible-status" class="rc-anchor-aria-status" aria-hidden="true">Пройдите проверку reCAPTCHA.. </div><div class="rc-anchor-error-msg-container" style="display:none"><span class="rc-anchor-error-msg" aria-hidden="true"></span></div><div class="rc-anchor-content"><div class="rc-inline-block"><div class="rc-anchor-center-container"><div class="rc-anchor-center-item rc-anchor-checkbox-holder"><span class="recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox recaptcha-checkbox-clearOutline" role="checkbox" aria-checked="false" id="recaptcha-anchor" dir="ltr" aria-labelledby="recaptcha-anchor-label" style="" aria-disabled="false" tabindex="0"><div class="recaptcha-checkbox-border" role="presentation" style=""></div><div class="recaptcha-checkbox-borderAnimation" role="pres entation" style=""></div><div class="recaptcha-checkbox-spinner" role="presentation" style="display: none; animation-play-state: running; opacity: 0; transform: scale(0);"><div class="recaptcha-checkbox-spinner-overlay" style="animation-play-state: running;"></div></div><div class="recaptcha-checkbox-checkmark" role="presentation"></div></span></div></div></div><div class="rc-inline-block"><div class="rc-anchor-center-container"><label class="rc-anchor-center-item rc-anchor-checkbox-label" aria-hidden="true" role="presentation" id="recaptcha-anchor-label"><span aria-live="polite" aria-labelledby="recaptcha-accessible-status"></span>Я не робот</label></div></div></div><div class="rc-anchor-normal-footer"><div class="rc-anchor-logo-portrait" aria-hidden="true" role="presentation"><div class="rc-anchor-logo-img rc-anchor-logo-img-portrait"></div><div class="rc-anchor-logo-text">reCAPTCHA</div></div><div class="rc-anchor-pt"><a href="https://www.google.com/intl/ru/policies/privacy/" target="_blank">Конфиденциальность</a><span aria-hidden="true" role="presentation"> - </span><a href="https://www.google.com/intl/ru/policies/terms/" target="_blank">Условия использования</a></div></div></div><iframe style="display: none;"></iframe></body></html>


