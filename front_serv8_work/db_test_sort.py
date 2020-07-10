# -*- coding: utf-8 -*-
import pymongo
import os

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
         
     def see_all_sort_post(self):
         list = []
         #J = self.db[self.n].find({'answ_V': 1})
         #self.db[self.n].drop_index([("answ_V", 1)])
         #J = self.db[self.n].create_index("answ_L")
         #print (">>>>",J) 
            
         gj = self.db[self.n].find().count()  
         news = gj // 100000
         print (gj, news)
         for hj in range(0, news):
              for i in self.db[self.n].find().sort("answ_V", pymongo.DESCENDING).limit(100000):
                   list.append(i)
         #J = self.db[self.n].find({"answ_L":1}).sort('answ_V',1)
         #J = J.sort('answ_V',pymongo.DESCENDING)
         #J = J.sort('answ_L',pymongo.DESCENDING)
         #J = J.sort('answ_H',pymongo.DESCENDING)
         #([("answ_V", pymongo.DESCENDING), ("answ_H", pymongo.DESCENDING)])
         # #pymongo.ASCENDING
         
#         for i in J:
#              #i["_id"] = str(i["_id"])
#              
#              #if i['answ_V'] == [1]:
#              print (i)
#              list.append(i)
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
                 result = self.db[self.n].find_one(idx)
                 #print result, result["_id"] 
                 #result = self.db[self.n].delete_one(result)
                 result = self.db[self.n].delete_one(idx)
                 result.deleted_count  
     # Список баз
     


     def del_db_by_name(self, x):
         self.client.drop_database(x)

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
        classDB.see_collection()
        
        classDB.create_collection("buses_3x3.tar_2019-12-25 20:03:54")
        print (classDB.see_all_sort_post()[:10])
#        classDB.del_db_by_name("o")
#        print ("\nклассы:")
#        classDB.create_collection("collection")
#        print ("See all post:", classDB.see_all_post())
#        classDB.see_collection() # Collection - Типы классы 
#        ddd = classDB.see_all_sort_post("x")
 #       print ("Loock:", len(ddd))
        
        
        
        


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


    


        
