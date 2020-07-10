# -*- coding: utf-8 -*-
from pymongo import MongoClient
import os

mongodb_uri = os.getenv('MONGODB_URI', default='mongodb://localhost:27017/')

class mDB(object):
     def __init__(self):
         self.client = MongoClient(mongodb_uri)#MongoClient('localhost', 27017)
         self.db = self.client.test_database  
         self.posts = self.db.posts  

     def DBmongo(self):
         for idb in self.client.list_databases():
             print (idb) 
     

     def deldb(self):
         self.client.drop_database('test_database')

     def seecount(self):
         return  self.posts.count()

     def seealldb(self):
         for i in self.posts.find():
              print  (i)#.deleted_count 

     def seeonedb(self, idx):
         return  self.posts.find_one(idx)


     def delalldb(self):
         for i in self.posts.find():
                 result = self.posts.find_one(i["_id"])
                 #print result, result["_id"] 
                 result = self.posts.delete_one(result)
                 result.deleted_count  

     def delonedb(self, idx):   
                 result = self.posts.find_one(idx)
                 #print result, result["_id"] 
                 result = self.posts.delete_one(result)
                 result.deleted_count  

     def post_db(self, post):
                 post_id = self.posts.insert_one(post).inserted_id
                 return (post_id)



classDB = mDB()
#classDB.post_db({"task":"chimneys"})
classDB.deldb()
"""
fl = open("hydrantsWarningStep.txt","r")

for u in fl.readlines():
   #print u.split("\n")[0].split(";")[0], u.split("\n")[0].split(";")[1]
   try:
	   post = {"file": u.split("\n")[0].split(";")[0], 
		   "answ": "", "answ_V": u.split("\n")[0].split(";")[1], "task":"fire hydrant",
                   "type":3}
	   classDB.post_db(post)  
   except:
           print (u) 
"""


    


        
