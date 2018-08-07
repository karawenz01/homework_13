import pymongo
import scrape_mars

conn = 'mongodb://localhost:27017'

client = pymongo.MongoClient(conn)

db = client.mydatabase
collection = db.mars

data = scrape_mars.scrape()

collection.insert(data)