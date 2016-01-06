from flask import Response
from flask.views import View
from bson import json_util
from mcp import mongo


class VleraCmimi(View):
    def dispatch_request(self, komuna=None, viti=None, company_slug=None):

        aggegation = []

        # If a commune or year is specified, create a match operation
        if komuna != None and viti != None:
            match = {
                "$match": {
                    "komuna.slug": komuna,
                    "viti": viti
                }
            }
            aggegation.append(match)

            group = {
                "$group": {
                    '_id': {
                        'muaji': {
                            '$month': "$dataNenshkrimit"
                        }
                    },
                    "vlera": {
                        "$sum": "$kontrata.vlera"
                    },
                    "qmimi": {
                        "$sum": "$kontrata.qmimi"
                    }
                }
            }
            aggegation.append(group)

            project = {
                "$project": {
                    "muaji": "$_id.muaji",
                    "vlera": "$vlera",
                    "qmimi": "$qmimi",
                    "_id": 0
                }
            }
            aggegation.append(project)

            sort = {
                '$sort': {
                    'muaji': 1
                }
            }
            aggegation.append(sort)

        elif company_slug != None:
            match = {
                "$match": {
                    "kompania.slug": company_slug,
                }
            }
            aggegation.append(match)

            group = {
                "$group": {
                    '_id': {
                        'data': "$dataNenshkrimit"
                    },
                    "vlera": {
                        "$sum": "$kontrata.vlera"
                    },
                    "qmimi": {
                        "$sum": "$kontrata.qmimi"
                    },
                    "aneks": {
                        "$sum": "$kontrata.qmimiAneks"
                    }
                }
            }
            aggegation.append(group)

            project = {
                "$project": {
                    "data": "$_id.data",
                    "vlera": "$vlera",
                    "qmimi": "$qmimi",
                    "aneks": "$aneks",
                    "_id": 0
                }
            }
            aggegation.append(project)

            sort = {
                '$sort': {
                    'data': 1
                }
            }
            aggegation.append(sort)

        print(aggegation)
        json = mongo.db.procurements.aggregate(aggegation)


        # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne resp
        resp = Response(
            response=json_util.dumps(json['result']),
            mimetype='application/json')

        return resp
