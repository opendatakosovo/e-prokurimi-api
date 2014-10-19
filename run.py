from flask import Flask
from flask import Response
from bson import json_util
from pymongo import MongoClient


mongo = MongoClient()

db = mongo.gjakova
app = Flask(__name__)


@app.route("/")
def index():

    return "Per te shfaqur JSON Dokumentet per diagramet PieChart atehere ne URL duhet te ekzekutoni per PieChart: <br>" \
           " http://127.0.0.1:5000/piechart/<int:viti>  Spjegim: Ne vend te vitit perdorni vitin per te cilin<br>"\
           " deshironi te shfaqni JSON Dokumentin. Shembull http://127.0.0.1:5000/piechart/2013 <br>"\
           "Ndersa per te shfaqur JSON Dokumentet per diagramet Treemap atehere ndjekni po te njejtet hapa <br> "\
           " http://127.0.0.1:5000/treemap/<int:viti>"



@app.route("/treemap/<int:viti>")
def treemap(viti):
    json = db.procurements.aggregate([
            {
                "$match":{
                        "viti":viti
                        }
            },
            {
                "$group":{
                        "_id":{
                            "kompania":"$kompania.slug",
                            "tipi":"$tipi"
                        },
                        "shuma":{
                            "$sum":"$kontrata.vlera"
                            }
                        }
            },
            {
                "$sort":{
                        "_id.tipi":1,
                        "_id.kompania":1
                        }
            },
            {
                "$project":{
                        "kompania":"$_id.kompania",
                        "tipi":"$_id.tipi",
                        "shuma":"$shuma",
                        "_id":0
                        }
            }
])
    resp = Response(response = json_util.dumps(json['result']), mimetype = 'application/json')

    return resp

@app.route("/piechart/<int:viti>")
def piechart(viti):

    json = db.procurements.aggregate([
            {
                "$match":{
                        "viti":viti
                        }
            },
            {
                "$group":{
                        "_id":{
                            "tipi":"$tipi"
                        },
                        "shuma":{
                            "$sum":"$kontrata.vlera"}
                        }
            },
            {
                "$sort":{
                        "_id.tipi":1
                        }
            },
            {
                "$project":{
                        "tipi":"$_id.tipi",
                        "shuma":"$shuma",
                        "_id":0
                        }
            }
        ])
    resp = Response(response = json_util.dumps(json['result']), mimetype = 'application/json')

    return resp

if __name__ == "__main__":
    app.run(debug=True)
