from flask import Flask
#from flask import Response
#from bson import json_util
#from pymongo import MongoClient


#mongo = MongoClient()

#db = mongo.gjakova
app = Flask(__name__)

@app.route("/")
def index():
    # Krijo nje varg
	vargu = ["elementi0","elementi1","elementi2","elementi3"]
    # Krijo nje dictionary
	dictinary = {"qelsi1":"vlera1","qelsi2":"vlera2"}
    # loop the list
	for elementi in vargu:
		print elementi
    # loop the dictionary

    # operacionet me string (length, replace, concatenation)
	return "<h1>Tungjatjeta Gjakov</h1>"

if __name__=="__main__":
    app.run(debug=True)
