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
         J1 = self.db[self.n].find({'answ_V': 1})
         J2 = self.db[self.n].find({'answ_L': 1})#.sort('answ_V',pymongo.DESCENDING)
         J3 = self.db[self.n].find({'answ_H': 1})#.sort('answ_V',1)
         print (J1.count(),J2.count(), J3.count())
         for i in J2:
              i["_id"] = str(i["_id"])
              #print (i)
              if i['answ_H'] == i['answ_L']:
                #print (i)
                list.append(i)
         print (len(list))       
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
     
     def count(self):
         return self.db[self.n].find().count()


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
#        classDB.del_db_by_name("o")
#        print ("\nклассы:")
#        classDB.create_collection("collection")
#        print ("See all post:", classDB.see_all_post())
#        classDB.see_collection() # Collection - Типы классы 
        classDB.create_collection("bicycles_3x3.tar_2019-12-24 20:12:41")
        #ddd = classDB.see_all_sort_post()
        ddd = classDB.see_all_post()
        print ("Loock:", len(ddd))
        files = open('bicycles_3x3.tar_2019-12-24 20:12:41.csv', 'w')
        #file.write("{};{};\n".format(x["file"].split("/")[-1], [int(f) for f in x["answ_V"]]))
        for xxx in ddd:
           files.write("{};{};\n".format(xxx['file'].split("/")[-1], xxx))
           #f_file = open(xxx['file'], "rb").read()
           #to_file = open("buses/"+xxx['file'].split("/")[-1],"wb").write(f_file)
        
        
        


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


    


        
