from flask import Response
from flask.views import View
from bson import json_util, SON
from mcp import mongo

class MunicipalityList(View):
#@app.route("/<string:komuna>/monthly-summary")
    def dispatch_request(self, viti):
        json1 = mongo.db.procurements.aggregate([
            {
                "$match": {
                    "viti": viti
                }
            },
            {
                "$group": {
                    '_id': {
                        'komuna': "$komuna.slug",
                        'komuna_emri': "$komuna.emri",
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
                    "numriKontratave": {
                        "$sum": 1
                    }
                },
            },
            {
                "$project": {
                    "muaji": "$_id.muaji",
                    "komuna_emri": "$_id.komuna_emri",
                    "viti": "$_id.viti",
                    "komuna": "$_id.komuna",
                    "vlera": "$vlera",
                    "qmimi": "$qmimi",
                    "numriKontratave": "$numriKontratave",
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
        json = mongo.db.procurements.find_one()
        # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne  resp
        resp = Response(response=json_util.dumps(json),mimetype='application/json')

        # ne momentin kur hapim  sh.: http://127.0.0.1:5000/treemap duhet te kthejme JSON, ne rastin tone resp.
        return resp
