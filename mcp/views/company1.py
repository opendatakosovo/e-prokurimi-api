from flask import Response
from flask.views import View
from bson import json_util, SON
from mcp import mongo


class CompanyList(View):
#@app.route("/<string:komuna>/monthly-summary")
    def dispatch_request(self, komuna):
        json = mongo.db.procurements.aggregate([
            {
                "$match": {
                    "city": komuna
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
                    "count": {
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
