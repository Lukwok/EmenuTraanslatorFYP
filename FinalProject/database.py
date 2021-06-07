from pymongo import MongoClient, collation, results
from pprint import pprint
from bson.dbref import DBRef
from bson import ObjectId
import certifi
client = MongoClient("mongodb://admin03:admin03@cluster0-shard-00-00.ozhyv.mongodb.net:27017,cluster0-shard-00-01.ozhyv.mongodb.net:27017,cluster0-shard-00-02.ozhyv.mongodb.net:27017/fyp?ssl=true&replicaSet=atlas-gvd5u7-shard-0&authSource=admin&retryWrites=true&w=majority",tlsCAFile=certifi.where())
# db= client.fyp

def findDocs(criteria):
    db= client.fyp    
    data = db.restaurants.find(criteria)
    return data

def findDoc(criteria):
    db= client.fyp    
    data = db.restaurants.find_one(criteria)
    return data

def dereference(dbref):
    if not isinstance(dbref, DBRef):
        raise TypeError("cannot dereference a %s" % type(dbref))
    db= client.fyp
    table = dbref.collection
    if (table =="menu"):
        return db.menu.find_one({"_id":ObjectId(dbref.id)})
    elif (table == "restaurants"):
        return db.restaurants.find_one({"_id":ObjectId(dbref.id)})
    else:
        print ("No such table")
        return []

def show_edit(lang,r_id):
    db= client.fyp
    r_doc = db.shop.find_one({"_id": ObjectId(r_id)})
    if (lang=="zh"):
        m_id = r_doc["menu"]["zh"]
        data = db.menu.find_one({"_id": ObjectId(m_id)})
        return data  
    elif (lang =="en"):
        f_m_id = r_doc["menu"]["en"]
        data = db.en_menu.find_one({"_id": ObjectId(f_m_id)})
        return data
    elif (lang == "kr"):
        f_m_id = r_doc["menu"]["kr"]
        data = db.kr_menu.find_one({"_id": ObjectId(f_m_id)})
        return data
    elif (lang =="jp"):
        f_m_id = r_doc["menu"]["jp"]
        data = db.jp_menu.find_one({"_id": ObjectId(f_m_id)})
        return data

def update_data(data):
    db= client.fyp
    m_id=data["m_id"]
    query = {"_id": ObjectId(m_id)}
    set_query = {}
    if data["soup"] :
        set_query["soup"]=data["soup"]
    if data["level"]:
        set_query["level"]=data["level"]
    if data["topping"]:
        set_query["topping"]=data["topping"]

    if (data["lang"]=="zh"):
        table = db.menu
    elif (data["lang"]=="en"):
        table = db.en_menu
    elif (data["lang"]=="kr"):
        table = db.kr_menu
    elif (data["lang"]=="jp"):
        table = db.jp_menu
    
    m_doc = table.find_one(query)
    
    index = 0
    new_dish_list = []
    for orignal in m_doc["dish"]:
        orignal['name']= data["dish"][index]["name"]
        orignal['price'] = data["dish"][index]["price"]
        if data["dish"][index]["description"]:
           orignal["decription"] = data["dish"][index]["description"]
        new_dish_list.append(orignal)
        index = index+1

    set_query["dish"] = new_dish_list
    table.update_one(query,{"$set":set_query})
       
def find_menu(lang,m_id):
    db= client.fyp
    if (lang=="zh"):
        table = db.menu
    elif (lang=="en"):
        table = db.en_menu
    elif (lang=="kr"):
        table = db.kr_menu
    elif (lang=="jp"):
        table = db.jp_menu 

    data = table.find_one({"_id":ObjectId(m_id)})
    return data
		

# db= client.fyp
# data = db.shop.find()
# for data_item in data:
#     print(data_item)
# print (data)



