from flask import Response
from flask.views import View
from bson import json_util


from mcp import mongo


class Piechart(View):
    def dispatch_request(self, komuna, viti):
        ''' permes app.route caktojme URL ne te cilen do te kthejme rezultatin
            qe na nevojitet, dhe permes <int:viti> kerkojme qe te caktojme vitin
            ne URL per te kerkuar nga databaza te dhenat perkatese te atij viti
            Shembull : http://127.0.0.1:5000/piechart/2011
        '''
        # ruajme rezultatin qe na kthehet nga databaza permes ekzekutimit te kerkeses(Query) ne json.
        json = mongo.db.procurements.aggregate([
            {
                "$match": {
                    "city": komuna,
                    #bejme match ne baze te vitit te cilin e kemi marre nga URL, <int:viti>
                    "viti": viti
                }
            },
            {
                "$group": {
                    "_id": {
                        "tipi": "$tipi"
                    },
                    "shuma": {
                        "$sum": "$kontrata.vlera"
                    }
                }
            },
            {
                "$sort": {
                    "_id.tipi": 1
                }
            },
            {
                "$project": {
                    "tipi": "$_id.tipi",
                    "shuma": "$shuma",
                    "_id": 0
                }
            }
        ])
        # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne resp
        resp = Response(
            response=json_util.dumps(json['result']),
            mimetype='application/json')

        # ne momentin kur hapim  sh.: http://127.0.0.1:5000/piechart/2011 duhet te kthejme JSON, ne rastin tone resp.
        return resp
