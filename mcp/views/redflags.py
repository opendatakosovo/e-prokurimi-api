from flask import Response
from flask.views import View
from bson import json_util
from mcp import mongo


class RedFlags(View):
#@app.route("/<string:komuna>/monthly-summary")
    def dispatch_request(self, viti, komuna):
        json = mongo.db.procurements.aggregate([
            {
                "$match": {
                    "viti": viti,
                    "komuna.slug": komuna
                }
            },
            {
                "$group": {
                    '_id': {
                        'kompania_emri': '$kompania.emri',
                        "selia": "$kompania.selia.emri",
                        "aktiviteti": "$aktiviteti",
                        'muaji': {
                            '$month': '$dataNenshkrimit'
                        }
                    },
                    "vlera": {
                        "$sum": "$kontrata.vlera"
                    },
                    "qmimi": {
                        "$sum": "$kontrata.qmimi"
                    },
                    "qmimiAneks": {
                        "$sum": "$kontrata.qmimiAneks"
                    }
                },
            },
            {
                '$sort': {
                        'muaji': -1
                    }
            },
            {
                "$project": {
                    "_id": 0,
                    "pershkrimi": "$_id.aktiviteti",
                    "kompania": "$_id.kompania_emri",
                    "selia": "$_id.selia",
                    "vlera": "$vlera",
                    "qmimi": "$qmimi",
                    "qmimiAneks": "$qmimiAneks",
                }
            }
        ])

        #pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne  resp
        resp = Response(
            response=json_util.dumps(json['result']),
            mimetype='application/json')

        #ne momentin kur hapim  sh.: http://127.0.0.1:5000/treemap duhet te kthejme JSON, ne rastin tone resp.
        return resp
