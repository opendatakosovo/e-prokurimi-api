from flask import Response
from flask.views import View
from bson import json_util
from mcp import mongo


class CompanyDirectory(View):
    def dispatch_request(self, kompania):
        json = mongo.db.procurements.aggregate([
            {
                "$match": {
                    "kompania.slug": {'$regex': kompania}
                }
            },
            {
                "$group": {
                    '_id': {
                        'kompania_slug': '$kompania.slug',
                        "emri": "$kompania.emri",
                    },
                    "saHereFitoiTenderin": {
                        "$sum": 1
                    },
                    "cmimi": {
                        "$sum": "$kontrata.qmimi"
                    },
                    "aneks": {
                        "$sum": "$kontrata.qmimiAneks"
                    }
                }
            },
            {
                '$sort': {
                        '_id.kompania_slug': 1
                    }
            },
            {
                "$project": {
                    "_id": 0,
                    "emri": "$_id.emri",
                    "slug": "$_id.kompania_slug",
                    "cmimi": "$cmimi",
                    "aneks": "$aneks",
                    "count": "$saHereFitoiTenderin"
                }
            }
        ])


        json_result = mongo.db.procurements.aggregate([
            {
                "$group": {
                    '_id': {
                        'kompania_slug': '$kompania.slug',
                        "emri": "$kompania.emri",
                    },
                    "saHereFitoiTenderin": {
                        "$sum": 1
                    },
                    "cmimi": {
                        "$sum": "$kontrata.qmimi"
                    },
                    "aneks": {
                        "$sum": "$kontrata.qmimiAneks"
                    }
                }
            },
            {
                '$sort': {
                        '_id.kompania_slug': 1
                    }
            },
            {
                "$project": {
                    "_id": 0,
                    "emri": "$_id.emri",
                    "slug": "$_id.kompania_slug",
                    "cmimi": "$cmimi",
                    "aneks": "$aneks",
                    "count": "$saHereFitoiTenderin"
                }
            }
        ])

        result_json = {}
        result_json['bounds'] = json_result['result']
        result_json['result'] = json['result']

        #pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne  resp
        resp = Response(
            response=json_util.dumps(result_json),
            mimetype='application/json')

        #ne momentin kur hapim  sh.: http://127.0.0.1:5000/treemap duhet te kthejme JSON, ne rastin tone resp.
        return resp
