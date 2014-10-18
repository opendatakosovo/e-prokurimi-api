from flask import Flask, Response
from bson import json_util
from pymongo import MongoClient


mongo = MongoClient()

db = mongo.gjakova
app = Flask(__name__)

@app.route("/")
def index():
    # Build a list
    # Build a dictionary
    # if, elif, else
    # loop the list
    # loop the dictionary
    # string operations (length, replace, concatenation)


    return "Hello World"

if __name__=="__main__":
    app.run(debug=True)
