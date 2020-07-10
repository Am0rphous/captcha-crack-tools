# -*- coding: utf-8 -*-
import pymongo
import os

mongodb_uri = os.getenv('MONGODB_URI', default='mongodb://localhost:27017/')



class mDB(object):
     def __init__(self):
         self.client = pymongo.MongoClient(mongodb_uri) #MongoClient('localhost', 27017)

         # 2 вариант
         self.db = self.client["t"] 
         self.n ="collection"
         
         
         #self.db = self.client["x"] 
         #self.n ="collection"
         
         
     def create_collection(self, x): #self.n
                self.n = x

     def create_post(self, post):
                 post_id = self.db[self.n].insert_one(post).inserted_id
                 return post_id

     def create_many(self, post):
                 self.db[self.n]
                 post_id = self.db[self.n].insert_many(post)
                 return post_id        


     def see_all_post(self):
         list = []
         for i in self.db[self.n].find():
              i["_id"] = str(i["_id"])
              list.append(i)
         return list
         
     def see_all_post4(self, list):
         #list = []
         for i in self.db[self.n].find():
              i["_id"] = str(i["_id"])
              list.append(i)
         #return list 
         
     def see_all_sort_post(self):
         list = []
         J1 = self.db[self.n].find({'answ_V': 1})
         J2 = self.db[self.n].find({'answ_L': 1})#.sort('answ_V',pymongo.DESCENDING)
         J3 = self.db[self.n].find({'answ_H': 1})#.sort('answ_V',1)
         J_all = self.db[self.n].find()
         print (J1.count(),J2.count(), J3.count())
         if J3.count() != 0:
                 for i in J3:
                 #for i in J_all:
                      i["_id"] = str(i["_id"])
                      #print (i)
                      if i['answ_H'] != i['answ_L']:
                        #print (i)
                        list.append(i)
                      #list.append(i)  
                 return list
         else:
               for i in J_all:  
                  i["_id"] = str(i["_id"])
                  list.append(i)
               return list  
               
               
               
     def see_sort(self):
         list = []
         J1 = self.db[self.n].find({'answ_V': 1})
         J2 = self.db[self.n].find({'answ_L': 1})#.sort('answ_V',pymongo.DESCENDING)
         J3 = self.db[self.n].find({'answ_H': 1})#.sort('answ_V',1)
         J_all = self.db[self.n].find()
         print ("ANSW V", J1.count(), "ANSW L", J2.count(), "ANSW H", J3.count())
         for i in J_all:  
                  i["_id"] = str(i["_id"])
                  list.append(i)
         return list                 
                
     def stat(self):
         J1 = self.db[self.n].find({'answ_V': 1})
         J2 = self.db[self.n].find({'answ_L': 1})#.sort('answ_V',pymongo.DESCENDING)
         J3 = self.db[self.n].find({'answ_H': 1})#.sort('answ_V',1)
         J4 = self.db[self.n].find({'answ': 1})
         return [J1.count(), J2.count(), J3.count(), J4.count()]   
             
     def stat4(self):
         ls = []
         self.see_all_post4(ls)
         ls_L = []
         ls_V = []
         ls_H = []
         answ = []
         for i in ls:
            if i['answ_H'] != "":
               ls_H.append(i)
            if i['answ_L'] != "":
               ls_L.append(i)
            if i['answ_V'] != "":
               ls_V.append(i)
            if i['answ'] != "":
               answ.append(i)
               
         return len(ls_V), len(ls_L), len(ls_H), len(answ)             
         
     def see_sort_load(self, list):
         J_all = self.db[self.n].find()
         for i in J_all:  
                  i["_id"] = str(i["_id"])
                  #if i['answ_H'] == i['answ_L'] or i['answ'] == [1]: #i['answ'] == [1]:
                  list.append(i)
         #return list     
 
     def see_post(self, idx):
         #print (idx, self.n)
         return self.db[self.n].find_one(idx)
         
     def upd_post(self, idx, post):
         #print (post)
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
                 result = self.db[self.n].delete_one(result)
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







    


        
