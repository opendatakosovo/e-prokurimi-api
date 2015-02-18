from flask import Response
from flask.views import View
from bson import json_util
from mcp import mongo


class CompanyDirectory(View):
    def dispatch_request(self, kompania=None):

        # The aggregation pipeline list
        aggegation = []

        # If a company slug is specified, create a match operation
        if kompania != None:
            match = {
                "$match": {
                    "kompania.slug": {'$regex': kompania}
                }
            }
            aggegation.append(match)


        # Create and add group aggregation operation
        group = {
            "$group": {
                '_id': {
                    'kompania_slug': '$kompania.slug'
                },
                "emrat": {
                    "$addToSet": "$kompania.emri" 
                },
                "saHereFitoiTenderin": {
                    "$sum": 1
                },
                "klientet": {
                    "$addToSet": "$komuna.emri" 
                },
                "cmimi": {
                    "$sum": "$kontrata.qmimi"
                },
                "aneks": {
                    "$sum": "$kontrata.qmimiAneks"
                }
            }
        }
        aggegation.append(group)

        # Create and add sort aggregation operation
        sort = {
            '$sort': {
                    '_id.kompania_slug': 1
                }
        }
        aggegation.append(sort)

        # Create and add project aggregation operation
        project = {
            "$project": {
                "_id": 0,
                "slug": "$_id.kompania_slug",
                "emrat": "$emrat",
                "klientet": "$klientet",
                "cmimi": "$cmimi",
                "aneks": "$aneks",
                "count": "$saHereFitoiTenderin"
            }
        }
        aggegation.append(project)

        # Execute aggregation
        json = mongo.db.procurements.aggregate(aggegation)

        #pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne  resp
        resp = Response(
            response=json_util.dumps(json['result']),
            mimetype='application/json')

        #ne momentin kur hapim  sh.: http://127.0.0.1:5000/treemap duhet te kthejme JSON, ne rastin tone resp.
        return resp
