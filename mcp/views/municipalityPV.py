from flask import Response
from flask.views import View
from bson import json_util, SON
from mcp import mongo

class MunicipalityList(View):
#@app.route("/<string:komuna>/monthly-summary")
    def dispatch_request(self, viti):
        json = mongo.db.procurements.aggregate([
            {
                "$match": {
                    "viti": viti
                }
            },
            {
                "$group": {
                    '_id': {
                        'komuna': "$city",
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
                },
            },
            {
                "$project": {
                    "muaji": "$_id.muaji",
                    "viti": "$_id.viti",
                    "komuna": "$_id.komuna",
                    "vlera": "$vlera",
                    "qmimi": "$qmimi",
                    "_id": 0
                }
            },
            {
                '$sort':
                    SON([
                        ('komuna', 1),
                        ('muaji', 1)])
            }
        ])
        # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne  resp
        resp = Response(
            response=json_util.dumps(json['result']),
            mimetype='application/json')

        # ne momentin kur hapim  sh.: http://127.0.0.1:5000/treemap duhet te kthejme JSON, ne rastin tone resp.
        return resp
