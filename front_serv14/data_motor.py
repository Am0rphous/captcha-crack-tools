# -*- coding: utf-8 -*-
import pymongo
import os
import motor.motor_tornado

#mongodb_uri = os.getenv('MONGODB_URI', default='mongodb://localhost:27017/')
#client = pymongo.MongoClient(mongodb_uri)
client = motor.motor_tornado.MotorClient('mongodb://localhost:27017')
db = client["t"] 

#list_m = []
#for i in db.list_collection_names():
#     print(i)
#     list_m.append(i)
async def gg():
    async for document in db.find():
          print (document)
gg()        
#IOLoop.current().run_sync(gg)



    


        
