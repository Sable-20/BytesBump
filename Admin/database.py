import pymongo
from Admin.admin import Files

cluster = pymongo.MongoClient(Files.config("main", "mongo"))
db = cluster["main"]
collection = db["main"]

class Database:
  def exists(guild):
    r = collection.find_one({"_id":guild.id})
    if not r: return False
    return True
  
  def get_all():
    results = collection.find({})
    return [i for i in results]
  
  def get(guild):
    r = collection.find_one({"_id":guild.id})
    return r
  
  def find(data):
    r = collection.find_one(data)
    return r

  def add(guild):
    collection.insert_one({
      "_id":guild.id,
      "fetch_invite":None,
      "listing":None,
      "color":None,
      "description":None
    })
  
  def delete(guild):
    collection.delete_one({"_id":guild.id})

  def update(guild, values):
    collection.update_one({"_id":guild.id}, {"$set":values})