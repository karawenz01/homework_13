# import dependencies
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo 
import scrape_mars

app = Flask(__name__)

# mongo connection
# app.config("MONGO_URI") = "mongodb://localhost:27017/myDatabase"
# mongo = PyMongo(app)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]


# Connect to a database. Will create one if not already available.
#collection = mongo.db.mars
collection = mydb["mars"]

# create route 
@app.route("/")
def home():

    data = collection.find_one()

    return render_template("index.html", data=data)


# scrape route
@app.route("/scrape")
def scrape():

    new_scrape = scrape_mars.scrape()

    # add scraped data
    collection.insert_one(new_scrape)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
