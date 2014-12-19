from flask import Flask
from flask import Response
from flask.views import View
from bson import json_util, SON
from mcp import mongo
from pymongo import MongoClient
import argparse


class VleraCmimi(View):
    def dispatch_request(self, komuna, viti):
        ''' permes app.route caktojme URL ne te cilen do te kthejme rezultatin
            qe na nevojitet, dhe permes <string:komuna> kerkojme nga databaza
            te dhenat per komunen e caktuar dhe me <int:viti> kerkojme qe te 
            caktojme vitin ne URL per te kerkuar nga databaza te dhenat 
            perkatese te atij viti
            Shembull : http://127.0.0.1:5000/komuna/monthly-summary/viti
        '''
        json = mongo.db.procurements.aggregate([
            {
                "$match": {
                    "city": komuna,
                    "viti": viti
                }
            },
            {
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
                },
            },
            {
                "$project": {
                    "muaji": "$_id.muaji",
                    "vlera": "$vlera",
                    "qmimi": "$qmimi",
                    "_id": 0
                }
            },
            {
                '$sort':{
                            'muaji': 1
                        }
            }
        ])
        # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne  resp
        resp = Response(
            response=json_util.dumps(json['result']),
            mimetype='application/json')

        return resp