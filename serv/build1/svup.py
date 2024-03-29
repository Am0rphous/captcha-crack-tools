# -*- coding: utf-8 -*-
#from GPUi import gg #YOLO
from pymongo import MongoClient
from tornado.escape import json_encode
from bson.objectid import ObjectId

import cv2
import numpy as np
import os, sys, io
import glob, base64, json, time

from zipfile import ZipFile
import tarfile
import requests

import tornado.ioloop
import tornado.web
import tornado.websocket


mgDC = {"4x4":["mountains",
               "palms",
               "hydrants",	
               "buses",
               "crosswalks",
               "traffic_lights",
               "chimneys",
               "stairs",
               "motorbike",
               "bicycles",
               "tractors",
               "taxi",
               "bridges"]}



class DATA(object):
        def __init__(self):
            self.file = {}
            self.csv = "";
            #self.parseIMG()
            #print self.file
            #try:
            #  self.parseCSV()
            #except IOError:
            #  pass
            
        def parseCSV(self):
              with open(self.csv, 'r') as g:
                             for gh in g.readlines():
                                         gh = gh.split('\n')[0].split(';') 
                                         try:
                                              list = self.file[gh[0]]
                                              if gh[1] != 'no_matching_images':
                                                  convRUC = [int(i) for i in gh[1].split(':')[1].split('/')]
                                                  list.append(convRUC)
                                                  self.file[gh[0]] = list
                                              else:
                                                  list.append([])
                                                  self.file[gh[0]] = list
                                         except KeyError:
                                              pass

        def parseIMG(self, dir_name):
                path = "data/"+dir_name
                print ("PARSING",path)
                valid_images = [".jpg",".png"]
                for r, d, f in os.walk(path):
                    for file in f:
                        if valid_images[0] in file or valid_images[1] in file:
                           self.file[file.split(".")[0]] = [os.path.join(r, file)]
                        if ".csv" in file:
                           self.csv = os.path.join(r, file)

def LeoPost(x, idx, task):
    url = "http://148.251.0.181:8084/"
    with open(x, "rb") as f:
            data = f.read()
            payload = {"image":data.encode("base64"), "id":idx, "key":"oru6SF9kasU0uljhid6P0wSoZBduX8nY", "type":task}
            headers = { 'Content-Type': "application/json",
                        'cache-control': "no-cache" }
            response = requests.request("POST", url, data=json_encode(payload), headers=headers)
            return json.loads(response.text)


def ViPost(x, idx, task, c_box):
    url = "http://178.158.131.41:8800/"
    with open(x, "rb") as f:
            data = f.read()
            data = base64.b64encode(data).decode('utf-8')
            payload = {"image":data, "id":idx, "key":"oru6SF9kasU0uljhid6P0wSoZBduX8nY", "type":task, "c_box": c_box }
            headers = { 'Content-Type': "application/json",
                        'cache-control': "no-cache" }
            response = requests.request("POST", url, data=json_encode(payload), headers=headers)
            return json.loads(response.text)



def imgbite(x):
           x = cv2.resize(x,(412,412))
           img = x.astype(np.uint8)
           _, img_str = cv2.imencode('.jpg', img)
           BS = img_str.tobytes()
           return BS


def deansw(x):
    s = []
    for ix, i in enumerate(x):
        if i == 1:
           s.append(ix+1)
    return s


class DB(object):
    def __init__(self):
        self.pyDB = MongoClient('localhost', 27017)
        self.db = self.pyDB.test_database  
        self.posts = self.db.posts  

new = DB()    

class ImageWebSocket(tornado.websocket.WebSocketHandler):
    clients = set()
    myfile = 0
    seeidx = 0
    name = "" 
    ss = new.posts.find()
    tempID = 0    

    def track_progress(self, x):
       for member in x:
              self.write_message(json.dumps({"Process": "load"}))
       

    def open(self):
        ImageWebSocket.clients.add(self)
        print("WebSocket opened from: " + self.request.remote_ip)


    def on_message(self, message):
        
                ms =  json.loads(message)
                if list(ms.keys())[0] == "Start":
                   """Начало загрузки"""

                   self.name = ms["Start"]["Name"]
                   try:
                           self.myfile = open("archiv/"+ms["Start"]["Name"], "wb")
                           self.write_message(json.dumps({"Process": "MoreData"}))
                   except IOError:
                           os.mkdir("archiv")
                           self.myfile = open("archiv/"+ms["Start"]["Name"], "wb")
                           self.write_message(json.dumps({"Process": "MoreData"}))
                           
                if list(ms.keys())[0] == "Upload":
                   """Процесс загрузки"""

                   da = ms["Upload"]["Data"]
                   da = da.split(",")[1]
                   file_bytes = io.BytesIO(base64.b64decode(da)).read()
                   self.myfile.write(file_bytes)
                   self.write_message(json.dumps({"Process": "MoreData"}))

                if list(ms.keys())[0] == "Done":
                   """Конец загрузки"""

                   self.myfile.close()
                   self.write_message(json.dumps({"Process": "Process"}))
                      
                if list(ms.keys())[0] == "Process":
                           HD = DATA()
                           lss = ["gz", "tar"]
                           if self.name.split(".")[-1] in lss:
                                   tar = tarfile.open("archiv/"+self.name, "r")
                                   tar.extractall("data/"+self.name, members=self.track_progress(tar))
                                   tar.close()
                                   HD.parseIMG(self.name)
                           if self.name.split(".")[-1] == "zip":
                                   zip = ZipFile("archiv/"+self.name)
                                   zip.extractall("data/"+self.name)
                           
                                   HD.parseIMG(self.name)
                           for ixx, fx in enumerate(list(HD.file.keys())[:]):
                                   
                                   file_n = HD.file[fx][0]
                                   try:
                                      answ_H = HD.file[fx][1]
                                   except IndexError:
                                      answ_H = ""
                                   #print file_n, ms["task"], int(ms["type"])
                                   #iop = cv2.imread(file_n)
                                   answ_V = ViPost(file_n, str(ixx), ms["task"], int(ms["type"]))#""#gg(iop, ms["task"], int(ms["type"]))
                                   #answ_L = LeoPost(file_n, str(ixx), ms["task"])
                                   #print answ_H, answ_L["text"] #answ_V[0]
                                   
                                   post = {"file": file_n, 
                                           "answ": "", "answ_H": answ_H, "type":ms["type"],
                                           "answ_L" : "", "answ_V": answ_V["text"], "task":ms["task"]}
                                           #"answ": "", "answ_V": "", "task":ms["task"], "type":ms["type"]}
                                           #"answ_L" : answ_L["text"], "answ_V": "1", "task":ms["task"]}
                                   I = new.posts.insert_one(post).inserted_id

                           self.ss = new.posts.find()
                           self.write_message(json.dumps({"Process": "loaddone"}))


                if list(ms.keys())[0] == "SeeAllData":
                      if ms["SeeAllData"] == "ProcessNext":
                                      
                                      try:
                                          self.tempID = ObjectId(ms["idxx"])
                                          posttoCH = new.posts.find_one(ObjectId(ms["idxx"]))
                                          posttoCH["answ_V"] = deansw(ms["answ_v"])
                                          new.posts.update_one({"_id" : ObjectId(ms["idxx"])},
                                                                  {"$set": posttoCH}, upsert=True)
                                          posttoCH = new.posts.find_one(ObjectId(ms["idxx"]))
       
                                      except KeyError:
                                          pass
                  
                                      if new.posts.count() != 0:

                                              try:
                                                 obj = self.ss.next()
                                              except StopIteration:
                                                 self.ss.rewind()
                                                 obj = self.ss.next()    
                                              idxx = obj["_id"]
                                              fname = obj["file"]
                                              answ_v = obj["answ_V"]
                                              answ = obj["answ"] 
                                              task = obj["task"] 
                                              tp = obj["type"]      
                                              #print (fname, answ_v, answ, idxx, task, tp)                
                                              iop = cv2.imread(fname)
                                              
                                              #LeoPost(fname, str(idxx))
                                 
                                              s = base64.b64encode(imgbite(iop))
                                              #print (s) 
                                              obj = {"image":s.decode('ascii'), 
                                                     "answ_V": answ_v, 
                                                     "answ": answ,
                                                     "task": task,
                                                     "type":tp,
                                                     "_id": str(idxx),
                                                     "name": fname}
                                              self.write_message(json.dumps(obj))




    def on_close(self):
        ImageWebSocket.clients.remove(self)
        print("WebSocket closed from: " + self.request.remote_ip)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
       self.render("index.html", title="Нейронная сеть/Тренировка")


class MainUpload(tornado.web.RequestHandler):
    def get(self):
        items = {}
        for x in mgDC["4x4"]:
           J = list(new.posts.find({"task": x}))
           items[x] =len(J)
        self.render("upload.html", title="Нейронная сеть/Тренировка", items=json.dumps(items))


class MainData(tornado.web.RequestHandler):
    def get(self):
       self.render("data.html", title="Нейронная сеть/Тренировка")



##
def LLK(i):
        aJNEW = {} 
        aJL = {}
        aJV = {} 
        for ix, x in enumerate(new.posts.find({ "task": i})):
            if new.posts.find_one(x["_id"])["answ"] != []:
               aJNEW[ix] = new.posts.find_one(x["_id"])
               aJNEW[ix]["_id"] = str(aJNEW[ix]["_id"])
               #print posts.find_one(x["_id"])#["answ_H"], posts.find_one(x["_id"])["answ_H_new"]
            if new.posts.find_one(x["_id"])["answ_L"] != []:
               aJL[ix] = new.posts.find_one(x["_id"])
               aJL[ix]["_id"] = str(aJL[ix]["_id"])
            if new.posts.find_one(x["_id"])["answ_V"] != []:
               aJV[ix] = new.posts.find_one(x["_id"])
               aJV[ix]["_id"] = str(aJV[ix]["_id"])

        return aJNEW, aJV, aJL
  

class record():
     def __init__(self, x):
         self.file = open(x+'.csv', 'w')
         #print "LOAD"

     def toDown(self, x):
         try:
            os.mkdir(x)
         except OSError:
            for fl in  os.listdir(x):
                file_path = os.path.join(x, fl)
                if os.path.isfile(file_path):
                   os.remove(file_path)
            os.rmdir(x)
            os.mkdir(x)
     def cop(self, x, y):
         f_file = open(x, "rb").read()
         to_file = open(y,"wb").write(f_file)
         #f_file.close()
         #to_file.close()  
     def save(self, x):
         #print i
         
         self.cop(x["file"], "temp/"+x["task"]+"/" + x["file"].split("/")[-1])
         self.file.write("{};answ_v:{};answ_l:{};answ_new_human:{};answ_human:{};task:{};\n".format(x["file"].split("/")[-1],
                                                                        x["answ_V"],
                                                                        x["answ_L"],
                                                                        x["answ"],
                                                                        x["answ_H"],
                                                                        x["task"])) 
         #self.file.close()


def tardir(path, tar_name):
    with tarfile.open(tar_name, "w:gz") as tar_handle:
        for root, dirs, files in os.walk(path):
            for file in files:
                tar_handle.add(os.path.join(root, file))




##
class MainLoad(tornado.web.RequestHandler):
    def get(self):
        items = {}
        for x in mgDC["4x4"]:
           J = list(new.posts.find({"task": x}))
           items[x] =len(J)
        self.render("load.html", title="Нейронная сеть/Тренировка", items=json.dumps(items))
    def post(self):
        data_json = json.loads(self.request.body)
        if data_json["st"] == "prep":
                Gg = LLK(data_json["task"])
                #print "POST", len(Gg[0].keys()),len(Gg[1].keys()), len(Gg[2].keys())#self.request.body #Gg
                """Готовим статистику""" 
                kolo = {"answ":len(Gg[0].keys()) , "answ_L":len(Gg[1].keys()) , "answ_V":len(Gg[2].keys())} 
                self.write(kolo)
        else:
                #print data_json["task"]
                
                """create load"""
                rec = record('temp_csv/'+data_json["task"])
                rec.toDown('temp/'+data_json["task"])
                for i in new.posts.find():
                   if i["task"] == data_json["task"] and i["answ"] != []:
                       rec.save(i)
                tardir('temp/'+data_json["task"], 'to_load/'+data_json["task"]+'.tar.gz')
                
                #print 'temp_csv/'+data_json["task"]+'.csv', 'to_load/'+data_json["task"]+'.tar.gz'
                kolo = {"csv":'temp_csv/'+data_json["task"]+'.csv' , "arch":'to_load/'+data_json["task"]+'.tar.gz' }
                self.write(kolo)





app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/upload", MainUpload),
        (r"/alldata", MainData),
        (r"/load", MainLoad),
        (r"/websocket", ImageWebSocket),
        (r"/(robots-AI.jpg)", tornado.web.StaticFileHandler, {'path':'./'}),
        (r"/(index.png)", tornado.web.StaticFileHandler, {'path':'./'}),
        (r"/(.*)", tornado.web.StaticFileHandler, {'path':'./', 'default_filename': 'index.html'}),
    ])
app.listen(8800)


tornado.ioloop.IOLoop.current().start()



