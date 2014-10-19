from flask import Flask
#from flask import Response
#from bson import json_util
#from pymongo import MongoClient


#mongo = MongoClient()

#db = mongo.gjakova
app = Flask(__name__)

@app.route("/")
def index():
    # Krijo nje liste

    # Krijo nje dictionary

    # loop the list

    # loop the dictionary

    # operacionet me string (length, replace, concatenation)
	return "Hello World"

if __name__=="__main__":
    app.run(debug=True)
