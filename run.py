from flask import Flask
from flask import Response
from bson import json_util, SON
from pymongo import MongoClient
import argparse

# krijojme nje objekt te MongoClient(), klase e cila gjendet ne pymongo
mongo = MongoClient()

# ruajme instancen e databazes mongo.gjakova ne db
db = mongo.kosovoprocurements

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


@app.route("/<string:komuna>/piechart/<int:viti>")
def piechart(komuna, viti):
    ''' permes app.route caktojme URL ne te cilen do te kthejme rezultatin
        qe na nevojitet, dhe permes <int:viti> kerkojme qe te caktojme vitin
        ne URL per te kerkuar nga databaza te dhenat perkatese te atij viti
        Shembull : http://127.0.0.1:5000/piechart/2011
    '''
    # ruajme rezultatin qe na kthehet nga databaza permes ekzekutimit te kerkeses(Query) ne json.
    json = db.procurements.aggregate([
        {
            "$match": {
                "city":komuna,
                #bejme match ne baze te vitit te cilin e kemi marre nga URL, <int:viti>
                "viti": viti
            }
        },
        {
            "$group": {
                "_id": {
                    "tipi": "$tipi"
                },
                "shuma": {
                    "$sum": "$kontrata.vlera"
                }
            }
        },
        {
            "$sort": {
                "_id.tipi": 1
            }
        },
        {
            "$project": {
                "tipi": "$_id.tipi",
                "shuma": "$shuma",
                "_id": 0
            }
        }
    ])
    # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne resp
    resp = Response(
        response=json_util.dumps(json['result']),
        mimetype='application/json')

    # ne momentin kur hapim  sh.: http://127.0.0.1:5000/piechart/2011 duhet te kthejme JSON, ne rastin tone resp.
    return resp


@app.route("/<string:komuna>/treemap/<int:viti>")
# krijojme funksionin treemap(viti) i cili pranon vitin nga <int:viti>
def treemap(komuna, viti):
    ''' permes app.route caktojme URL ne te cilen do te kthejme rezultatin
        qe na nevojitet, dhe permes <int:viti> kerkojme qe te caktojme vitin
        ne URL per te kerkuar nga databaza te dhenat perkatese te atij viti
        Shembull : http://127.0.0.1:5000/treemap/2011
    '''
    json = db.procurements.aggregate([
        {
            "$match": {
                "city":komuna,
                "viti": viti
            }
        },
        {
            "$group": {
                "_id": {
                    "kompania": "$kompania.slug",
                    "tipi": "$tipi"
                },
                "shuma": {
                    "$sum": "$kontrata.vlera"
                },
                "count": {
                    "$sum": 1
                }
            }
        },
        {
            "$sort": {
                "_id.tipi": 1,
                "_id.kompania": 1
            }
        },
        {
            "$project": {
                "kompania": "$_id.kompania",
                "tipi": "$_id.tipi",
                "shuma": "$shuma",
                "count": "$count",
                "_id": 0
            }
        }
    ])
    # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne  resp
    resp = Response(
        response=json_util.dumps(json['result']),
        mimetype='application/json')

    # ne momentin kur hapim  sh.: http://127.0.0.1:5000/treemap/2011 duhet te kthejme JSON, ne rastin tone resp.
    return resp


@app.route("/<string:komuna>/treemap/price/<int:viti>")
# krijojme funksionin treemap(viti) i cili pranon vitin nga <int:viti>
def treemap_price(komuna, viti):
    ''' permes app.route caktojme URL ne te cilen do te kthejme rezultatin
        qe na nevojitet, dhe permes <int:viti> kerkojme qe te caktojme vitin
        ne URL per te kerkuar nga databaza te dhenat perkatese te atij viti
        Shembull : http://127.0.0.1:5000/treemap/2011
    '''
    json = db.procurements.aggregate([
        {
            "$match": {
                "city":komuna,
                "viti": viti
            }
        },
        {
            "$group": {
                "_id": {
                    "kompania": "$kompania.slug",
                    "tipi": "$tipi"
                },
                "shuma": {
                    "$sum": "$kontrata.qmimi"
                },
                "count": {
                    "$sum": 1
                }
            }
        },
        {
            "$sort": {
                "_id.tipi": 1,
                "_id.kompania": 1
            }
        },
        {
            "$project": {
                "kompania": "$_id.kompania",
                "tipi": "$_id.tipi",
                "shuma": "$shuma",
                "count": "$count",
                "_id": 0
            }
        }
    ])
    # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne  resp
    resp = Response(
        response=json_util.dumps(json['result']),
        mimetype='application/json')

    # ne momentin kur hapim  sh.: http://127.0.0.1:5000/treemap/2011 duhet te kthejme JSON, ne rastin tone resp.
    return resp

@app.route("/<string:komuna>/company/<string:name>")
def company_details(komuna, name):
    json = db.procurements.find(
        {
            "city":komuna,
            "kompania.slug": name

        }
    )
    # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze
    #te json_util.dumps() e ruajme ne  resp
    resp = Response(
        response=json_util.dumps(json),
        mimetype='application/json')

    # ne momentin kur hapim  sh.: http://127.0.0.1:5000/treemap
    # duhet te kthejme JSON, ne rastin tone resp.
    return resp


@app.route("/<string:komuna>/monthly-summary")
def company_list(komuna):
    json = db.procurements.aggregate([
        {
            "$match": {
                "city":komuna
            }
        },
        {
            "$group": {
                '_id': {
                    'viti': {
                        '$year': "$dataNenshkrimit"
                    },
                    'muaji': {
                        '$month': "$dataNenshkrimit"
                    }
                },
                "vlera": {
                    "$sum": "$kontrata.vlera"
                },
                "qmimi": {
                    "$sum": "$kontrata.qmimi"
                },
                "count":{
                    "$sum": 1
                }
            },
        },
        {
            "$project": {
                "muaji": "$_id.muaji",
                "viti": "$_id.viti",
                "vlera": "$vlera",
                "qmimi": "$qmimi",
                "count": "$count",
                "_id": 0
            }
        },
        {
            '$sort':
                SON([
                    ('viti', 1),
                    ('muaji', 1)])
        }
    ])
    # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne  resp
    resp = Response(
        response=json_util.dumps(json['result']),
        mimetype='application/json')

    # ne momentin kur hapim  sh.: http://127.0.0.1:5000/treemap duhet te kthejme JSON, ne rastin tone resp.
    return resp


@app.route("/<string:komuna>/budget-type/<int:year>")
def budget_type(komuna, year):
    ''' Ruajme rezultatin qe na kthehet nga databaza permes ekzekutimit
        te kerkeses(Query) ne json.
    '''
    json = db.procurements.aggregate([
        {
            "$match": {
                "city": komuna,
                "viti": year
            }
        },
        {
            "$group": {
                "_id": {
                    "tipi": "$tipiBugjetit"
                },
                "shuma": {
                    "$sum": "$kontrata.vlera"}
            }
        },
        {
            "$sort": {
                "_id.tipi": 1
            }
        },
        {
            "$project": {
                "tipi": "$_id.tipi",
                "shuma": "$shuma",
                "_id": 0
            }
        }
    ])
    # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne resp
    resp = Response(
        response=json_util.dumps(json['result']),
        mimetype='application/json')

    # ne momentin kur hapim  sh.: http://127.0.0.1:5000/piechart/2011 duhet te kthejme JSON, ne rastin tone resp.
    return resp


@app.route("/<string:komuna>/procurement-type/<int:year>")
def procurement_type(komuna, year):
    ''' ruajme rezultatin qe na kthehet nga databaza permes ekzekutimit
        te kerkeses(Query) ne json.
    '''
    json = db.procurements.aggregate([
        {
            "$match": {
                "city":komuna,
                "viti": year
            }
        },
        {
            "$group": {
                "_id": {
                    "tipi": "$tipi"
                },
                "shuma": {
                    "$sum": "$kontrata.vlera"}
            }
        },
        {
            "$sort": {
                "_id.tipi": 1
            }
        },
        {
            "$project": {
                "tipi": "$_id.tipi",
                "shuma": "$shuma",
                "_id": 0
            }
        }
    ])
    # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne resp
    resp = Response(
        response=json_util.dumps(json['result']),
        mimetype='application/json')

    # ne momentin kur hapim  sh.: http://127.0.0.1:5000/piechart/2011 duhet te kthejme JSON, ne rastin tone resp.
    return resp


# Run the app
if __name__ == '__main__':

    # Define the arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to: [%(default)s].')
    parser.add_argument('--port', type=int, default='5030', help='Port to listen to: [%(default)s].')
    parser.add_argument('--debug', action='store_true', default=True, help='Debug mode: [%(default)s].')

    # Parse arguemnts and run the app.
    args = parser.parse_args()
    app.run(debug=args.debug, host=args.host, port=args.port)
