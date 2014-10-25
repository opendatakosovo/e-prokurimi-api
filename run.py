from flask import Flask
from flask import Response
from bson import json_util
from pymongo import MongoClient

# krijojme nje objekt te MongoClient(), klase e cila gjendet ne pymongo
mongo = MongoClient()

# ruajme instancen e databazes mongo.gjakova ne db
db = mongo.gjakova

# krijojme objekt te Flask
app = Flask(__name__)

# krijojme HomePage permes @app.route("/")
@app.route("/")
def index():

    return "<h3>Per te shfaqur JSON Dokumentet per diagramet PieChart atehere ne URL duhet te ekzekutoni per PieChart:</h3>" \
           "http://127.0.0.1:5000/piechart/viti<br><br>" \
           "<em>Spjegim:</em> Ne vend te vitit perdorni vitin per te cilin" \
           " deshironi te shfaqni JSON Dokumentin.<br>" \
           "<em>Shembull:</em> <a href='http://127.0.0.1:5000/piechart/2013' target='_blank'>http://127.0.0.1:5000/piechart/2013</a> <br>"\
           "<h3>Ndersa per te shfaqur JSON Dokumentet per diagramet Treemap atehere ndjekni po te njejtet hapa si per PieChart</h3> "\
           " http://127.0.0.1:5000/treemap/viti"

# permes app.route caktojme URL ne te cilen do te kthejme rezultatin qe na nevojitet, dhe permes <int:viti> kerkojme
# qe te caktojme vitin ne URL per te kerkuar nga databaza te dhenat perkatese te atij viti
# Shembull : http://127.0.0.1:5000/piechart/2011

@app.route("/piechart/<int:viti>")
def piechart(viti):
    # ruajme rezultatin qe na kthehet nga databaza permes ekzekutimit te kerkeses(Query) ne json.
    json = db.procurements.aggregate([
            {
                "$match":{
                    #bejme match ne baze te vitit te cilin e kemi marre nga URL, <int:viti>
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
    # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne resp
    resp = Response(response = json_util.dumps(json['result']), mimetype = 'application/json')
    # ne momentin kur hapim  sh.: http://127.0.0.1:5000/piechart/2011 duhet te kthejme JSON, ne rastin tone resp.
    return resp


@app.route("/piechart")
def piechart_all():
    # ruajme rezultatin qe na kthehet nga databaza permes ekzekutimit te kerkeses(Query) ne json.
    json = db.procurements.aggregate([
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
    # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne resp
    resp = Response(response = json_util.dumps(json['result']), mimetype = 'application/json')
    # ne momentin kur hapim  sh.: http://127.0.0.1:5000/piechart/2011 duhet te kthejme JSON, ne rastin tone resp.
    return resp

# permes app.route caktojme URL ne te cilen do te kthejme rezultatin qe na nevojitet, dhe permes <int:viti> kerkojme
# qe te caktojme vitin ne URL per te kerkuar nga databaza te dhenat perkatese te atij viti
# Shembull : http://127.0.0.1:5000/treemap/2011

@app.route("/treemap/<int:viti>")
# krijojme funksionin treemap(viti) i cili pranon vitin nga <int:viti>
def treemap(viti):
    json = db.procurements.aggregate([
            {
                "$match":{
                    #bejme match ne baze te vitit te cilin e kemi marre nga URL, <int:viti>
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
    # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne  resp
    resp = Response(response = json_util.dumps(json['result']), mimetype = 'application/json')
    # ne momentin kur hapim  sh.: http://127.0.0.1:5000/treemap/2011 duhet te kthejme JSON, ne rastin tone resp.
    return resp


@app.route("/treemap")
def treemap_all():
    json = db.procurements.aggregate([
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
    # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne  resp
    resp = Response(response = json_util.dumps(json['result']), mimetype = 'application/json')
    # ne momentin kur hapim  sh.: http://127.0.0.1:5000/treemap duhet te kthejme JSON, ne rastin tone resp.
    return resp

@app.route("/company/<string:name>")
def company_details(name):
    json = db.procurements.find(
            {"kompania.slug":name

            }
        )
    # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne  resp
    resp = Response(response = json_util.dumps(json), mimetype = 'application/json')
    # ne momentin kur hapim  sh.: http://127.0.0.1:5000/treemap duhet te kthejme JSON, ne rastin tone resp.
    return resp



@app.route("/company-list")
def company_list():
    json = db.procurements.aggregate([
            {
                "$group":{
                        "_id":{
                            "emri":"$kompania.emri",
                            "tipi":"$tipi",
                            "slug":"$kompania.slug",
                            "selia":"$kompania.selia",
                            "viti":"$viti"
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
                        "emri":"$_id.emri",
                        "viti":"$_id.viti",
                        "tipi":"$_id.tipi",
                        "slug":"$_id.slug",
                        "shuma":"$shuma",
                        "_id":0
                        }
            }
])
    # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne  resp
    resp = Response(response = json_util.dumps(json['result']), mimetype = 'application/json')
    # ne momentin kur hapim  sh.: http://127.0.0.1:5000/treemap duhet te kthejme JSON, ne rastin tone resp.
    return resp

@app.route("/budget-type")
def budget_type():
    # ruajme rezultatin qe na kthehet nga databaza permes ekzekutimit te kerkeses(Query) ne json.
    json = db.procurements.aggregate([
            {
                "$group":{
                        "_id":{
                            "tipi":"$tipiBugjetit"
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
    # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne resp
    resp = Response(response = json_util.dumps(json['result']), mimetype = 'application/json')
    # ne momentin kur hapim  sh.: http://127.0.0.1:5000/piechart/2011 duhet te kthejme JSON, ne rastin tone resp.
    return resp

@app.route("/procurement-type")
def procurement_type():
    # ruajme rezultatin qe na kthehet nga databaza permes ekzekutimit te kerkeses(Query) ne json.
    json = db.procurements.aggregate([
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
    # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne resp
    resp = Response(response = json_util.dumps(json['result']), mimetype = 'application/json')
    # ne momentin kur hapim  sh.: http://127.0.0.1:5000/piechart/2011 duhet te kthejme JSON, ne rastin tone resp.
    return resp

if __name__ == "__main__":
    app.run(debug=True)
