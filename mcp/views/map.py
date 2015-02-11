from flask import Response
from flask.views import View
from bson import json_util
from mcp import mongo


class Map(View):

    def dispatch_request(self, komuna, viti):
        json = mongo.db.procurements.aggregate([
            {
              "$match": {
                    "komuna.slug": komuna,
                    "viti": viti,
                    "kompania.selia.slug": {'$ne': ''}
                }
            },
            {
                "$group": {
                    "_id": {
                        "selia": "$kompania.selia.slug",
                        "emri": "$kompania.selia.emri",
                        "gjeresi": "$kompania.selia.kordinatat.gjeresi",
                        "gjatesi": "$kompania.selia.kordinatat.gjatesi",
                    },
                    "cmimi": {
                        "$sum": "$kontrata.qmimi"
                    },
                    "vlera": {
                        "$sum": "$kontrata.vlera"
                    },
                    "numriKontratave": {
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
                    "selia": "$_id.selia",
                    "emri": "$_id.emri",
                    "gjeresia": "$_id.gjeresi",
                    "gjatesia": "$_id.gjatesi",
                    "cmimi": "$cmimi",
                    "vlera": "$vlera",
                    "numriKontratave": "$numriKontratave",
                    "_id": 0
                }
            }
        ])

        json_min_max = mongo.db.procurements.aggregate([
            {
                "$match": {
                    "komuna.slug": komuna,
                    "viti": viti,
                    "kompania.selia.slug": {'$ne': ''}
                }
            },
            {
                "$group": {
                    "_id": {
                        "selia": "$kompania.selia.slug",
                        "gjeresi": "$kompania.selia.kordinatat.gjeresi",
                        "gjatesi": "$kompania.selia.kordinatat.gjatesi",
                    },
                    "sumCmimi": {
                        "$sum": "$kontrata.qmimi"
                    },
                    "sumVlera": {
                        "$sum": "$kontrata.vlera"
                    },
                    "sumNumriKontratave": {
                        "$sum": 1
                    }
                }
            },
            {
                "$group": {
                    "_id": {},
                    "maxCmimi": {
                        "$max": "$sumCmimi"
                    },
                    "maxVlera": {
                        "$max": "$sumVlera"
                    },
                    "maxNumriKontratave": {
                        "$max": "$sumNumriKontratave"
                    },
                    "minCmimi": {
                        "$min": "$sumCmimi"
                    },
                    "minVlera": {
                        "$min": "$sumVlera"
                    },
                    "minNumriKontratave": {
                        "$min": "$sumNumriKontratave"
                    },

                }
            },
            {
                "$project": {
                    "_id": 0,
                    "vlera": {
                        "min": "$minVlera",
                        "max": "$maxVlera",
                    },
                    "cmimi": {
                        "min": "$minCmimi",
                        "max": "$maxCmimi",
                    },
                    "numriKontratave": {
                        "min": "$minNumriKontratave",
                        "max": "$maxNumriKontratave",
                    }
                }
            }
        ])

        #pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne  resp

        result_json = {};
        result_json['bounds'] = json_min_max['result'][0]
        result_json['result'] = json['result']

        resp = Response(
            response=json_util.dumps(result_json),
            mimetype='application/json')

        return resp
