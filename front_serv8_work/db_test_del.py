# -*- coding: utf-8 -*-
import pymongo
import os
from bson.objectid import ObjectId

mongodb_uri = os.getenv('MONGODB_URI', default='mongodb://localhost:27017/')



class mDB(object):
     def __init__(self):
         self.client = pymongo.MongoClient(mongodb_uri) #MongoClient('localhost', 27017)

         # 2 вариант
         self.db = self.client["o"] 
         self.n ="collection"
         
         
     def create_collection(self, x): #self.n
                self.n = x
                #self.db[self.n]

     def create_post(self, post):
                 #print (post)
                 #self.db[self.n]
                 post_id = self.db[self.n].insert_one(post).inserted_id
                 return post_id

     def create_many(self, post):
                 self.db[self.n]
                 post_id = self.db[self.n].insert_many(post)
                 return post_id        


     def see_all_post(self):
         #self.n ="post4"
         list = []
         for i in self.db[self.n].find():
              #print  ("документы\n" ,i)
              i["_id"] = str(i["_id"])
              list.append(i)
         return list

     def see_test_post(self, x):
         #self.n ="post4"
         list = []
         for i in self.db[self.n].find({'task': x}):
              #print  ("документы\n" ,i)
              i["_id"] = str(i["_id"])
              list.append(i)
         return list
         
         
     def see_test_post2(self):
         #self.n ="post4"
         list = []
         for i in self.db[self.n].find():
              #print  ("документы\n" ,i)
              i["_id"] = str(i["_id"])
              list.append(i)
         return list                
#     def see_test_post2(self):
#         #self.n ="post4"
#         list1 = []
#         list2 = []
#         for i in self.db[self.n].find({"answ_V": 1}):
#              #print  ("документы\n" ,i)
#              i["_id"] = str(i["_id"])
#              list1.append(i)
#         for i in self.db[self.n].find({"answ_L": 1}):
#              #print  ("документы\n" ,i)
#              i["_id"] = str(i["_id"])
#              list2.append(i)
#         return list1, list2         
         
         
     def see_all_sort_post(self, x):
         list = []
         #J = self.db[self.n].find({'answ_V': 1})
         J = self.db[self.n].create_index([('answ_V',1)])
         print (">>>>",J)
         #J = self.db[self.n].find().sort('answ_V',pymongo.DESCENDING)
         J = self.db[self.n].find()#.sort('answ_V',1)
         #J = J.sort('answ_L',pymongo.DESCENDING)
         #J = J.sort('answ_H',pymongo.DESCENDING)
         #([("answ_V", pymongo.DESCENDING), ("answ_H", pymongo.DESCENDING)])
         # #pymongo.ASCENDING
         for i in J:
              i["_id"] = str(i["_id"])
              #print (i)
              list.append(i)
         return list
 
     def see_post(self, idx):
         #print (idx, self.n)
         return self.db[self.n].find_one(idx)
         
     def upd_post(self, idx, post):
         print (post)
         return self.db[self.n].update_one({"_id" : idx},
                                           {"$set": post}, upsert=True)


     def del_all_post(self):
         self.db[self.n].delete_many({}) 


     def del_post(self):
         for i in self.db[self.n].find():
                 print (i["_id"])#result, result["_id"] 
                 result = self.db[self.n].find_one(i["_id"])
                 result = self.db[self.n].delete_one(result)
                 result.deleted_count 

     def del_one_post(self, idx):
                 print (idx, self.n)
                 result = self.db[self.n].find_one({"_id":idx})
                 #print (result) 
                 result = self.db[self.n].delete_one(result)
                 #result = self.db[self.n].delete_one(idx)
                 result.deleted_count  
     # Список баз
     


     def del_db_by_name(self, x):
         self.client.drop_database(x)

     #Удаляет из колекции материл
     def del_collection(self):
         result = self.db[self.n].drop() 

     def see_collection(self):
        list = []
        for i in self.db.list_collection_names():
           print(i)
           list.append(i)
        return list

     def see_client(self):
         for idb in self.client.list_databases():
             print (idb, "Имя базы данных")




if __name__ == "__main__":
	#print ("Start")
	
	
        classDB = mDB()
        #classDB.see_collection()
        #classDB.create_collection("collection")
        for iop in classDB.see_all_post():
          #print (iop)
          if iop['collectionName'] == "cars.tar.xz_2019-12-26 11:50:57":
            print (">>>", iop["_id"],iop['collectionName'])
            #classDB.create_collection("collection")
            classDB.del_one_post(ObjectId(iop["_id"]))
        
        
        #print (csss)
        #m = "5e04bfc0214be726c1d50182"
        #classDB.del_one_post(ObjectId(m))
        
        
        #"cars.tar.xz_2019-12-26 14:10:47"
        #"cars.tar.xz_2019-12-26 14:10:09"
        #"buses.tar.xz_2019-12-26 14:12:16"
        
        
        classDB.create_collection("cars.tar.xz_2019-12-26 11:50:57")
        classDB.del_collection() # 
        print ("FINAL")
        
        classDB.see_collection()
        """"""
        #csss = classDB.see_all_post()
#        csss = classDB.see_test_post("cars")
#        #print (csss, len(csss))
#        T_list = []
#        for f in csss:
#           
#           classDB.create_collection(f['collectionName'])
#           fg = classDB.see_test_post2()
#           
#           for gg in fg:
#             #print (gg)
##             if gg["answ_L"] != []:
##                      print (gg, "answ_L")
#             if gg["answ_V"] == [1]:
#                      print (gg, "answ_V")
##             if gg["answ_H"] != "":
##                      print (gg, "answ_H+")
#            
#                      #if gg["answ_V"] == gg["answ_L"]:
#                         #T_list.append(gg)
#                 
#        print (T_list)  
        
        
        
        
        
        
               
           #print (fg[:3])
#        classDB.del_db_by_name("o")
#        print ("\nклассы:")
#        classDB.create_collection("collection")
#        print ("See all post:", classDB.see_all_post())
#        classDB.see_collection() # Collection - Типы классы 
#        classDB.create_collection("hydrants error.zip_2019-12-18 08:36:19")
#        ddd = classDB.see_all_sort_post("x")
#        print ("Loock:", len(ddd))
        
        
        
        


"""
db.Account.find().sort("UserName")  
db.Account.find().sort("UserName",pymongo.ASCENDING)   
db.Account.find().sort("UserName",pymongo.DESCENDING) 
Для запроса формирую временную колекцию
колекция в которой храняться колекции данных
колекция из колекций в которой храняться 

base64
коллекция к колекции
в коллекции на коллекции


Структура

{
  "_id" : 1,
  "_task" : "Целая",
  "struct" : [
    {
      "_id" : 1,
      "task" : "car",
      "size" : 2
    },
    {
      "_id" : 2,
      "task" : "bike",
      "size"  : 2000
    },
    {
      "_id" : 3,
      "task" : "bus",
      "size" : 0
    }
    ...
  ]
}

{
  "_id" : 2,
  "_task" : "Части",
  "struct" : [
    {
      "_id" : 1,
      "task" : "car",
      "size" : 100
    },
    {
      "_id" : 2,
      "task" : "bike",
      "size"  : 2000
    },
    {
      "_id" : 3,
      "task" : "bus",
      "size" : 5000
    }
    ...
  ]
}

Структура новых данных/архивов:
{
  "_id" : 2,
  "_task": Части/Целая
  "_name_bd" : ...,
  "data": 10.10.19
}

Данные 4x4

{
 "_id" : 1,
 "_type": 4x4,
 "_task": целая/части,
 "_name_bd": ...,

 "task": "car",
 "file": имя файла,
 "answ": "",
 "answ_H": "",
 "answ_L": "",
 "answ_V": "",
}

Данные 3x3 и 1x1
{
 "_id" : 1,
 "_type": 3x3,
 "_task": целая/части,
 "_name_bd": ...,
 "task": "car",

 "file": имя файла,
 "answ": "",
 "answ_H": "",
 "answ_L": "",
 "answ_V": "",

 "file": имя файла,
 "answ": "",
 "answ_H": "",
 "answ_L": "",
 "answ_V": "",
  ...
}



гидрант
4x4 НЕ резать решили
"""


    


        
