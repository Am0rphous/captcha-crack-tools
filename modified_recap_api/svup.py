# -*- coding: utf-8 -*-
import os, sys, io, base64, random, json, cv2
import tornado.ioloop
import tornado.web
import tornado.websocket
import numpy as np

def imgbite(x):
           x = cv2.resize(x,(412,412))
           img = x.astype(np.uint8)
           _, img_str = cv2.imencode('.jpg', img)
           BS = img_str.tobytes()
           return BS

class ImageWebSocket(tornado.websocket.WebSocketHandler):
    clients = set()
       
    def open(self):
        ImageWebSocket.clients.add(self)
        print("WebSocket opened from: " + self.request.remote_ip)


    def on_message(self, message):
         tp = random.choice([2,3,4,5])
         ms =  json.loads(message)
         if ms["Process"] == "captcha_start": 
                iop = cv2.imread("981490_3.jpg")
                print (iop.shape)
                ms =  json.loads(message)
                s = base64.b64encode(imgbite(iop))
                obj = {"image":s.decode('ascii'),
                       "type":tp
                      }
                self.write_message(json.dumps(obj))   
         if ms["Process"] == "captcha_done": 
                print (ms)
                #self.write_message(json.dumps(obj))          

    def on_close(self):
        ImageWebSocket.clients.remove(self)
        print("WebSocket closed from: " + self.request.remote_ip)


class MainData(tornado.web.RequestHandler):
    def get(self):
       self.render("data1.html", title="Нейронная сеть/Тренировка")





app = tornado.web.Application([
        (r"/", MainData),
        (r"/websocket", ImageWebSocket),
        (r"/(robots-AI.jpg)", tornado.web.StaticFileHandler, {'path':'./'}),
        (r"/(index.png)", tornado.web.StaticFileHandler, {'path':'./'}),
        (r"/(pv_layer_controls.png)", tornado.web.StaticFileHandler, {'path':'./'}),
        (r"/(.*)", tornado.web.StaticFileHandler, {'path':'./', 'default_filename': 'index.html'}),
    ])
app.listen(8800)


tornado.ioloop.IOLoop.current().start()

##Колекции
#{
#  "id" : "....."
#  "data"
#}
##Базы данных парсинга

##Лоты


