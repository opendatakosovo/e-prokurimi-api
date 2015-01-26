from flask import Response
from flask.views import View
from bson import json_util
from mcp import mongo


class Map(View):

    def dispatch_request(self, komuna, viti):
        json = mongo.db.procurements.aggregate([
                {
                  "$match": {
                        "city": komuna,
                        "viti": viti
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "selia": "$kompania.selia.slug",
                            "gjeresi": "$kompania.selia.kordinatat.gjeresi",
                            "gjatesi": "$kompania.selia.kordinatat.gjatesi",
                        },
                        "qmimi": {
                            "$sum": "$kontrata.qmimi"
                        },
                        "vlera": {
                            "$sum": "$kontrata.vlera"
                        },
                        "count": {
                            "$sum": 1
                        }
                    }
                },
                {
                    "$sort": {
                        "_id.selia": 1
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "selia": "$_id.selia",
                        "gjeresia": "$_id.gjeresi",
                        "gjatesia": "$_id.gjatesi",
                        "qmimi": "$qmimi",
                        "vlera": "$vlera",
                        "count": "$count",
                    }
                }
            ])

        #pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne  resp

        resp = Response(
            response=json_util.dumps(json['result']),
            mimetype='application/json')

        return resp
