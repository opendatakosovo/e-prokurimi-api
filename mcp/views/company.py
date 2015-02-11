from flask import Response
from flask.views import View
from bson import json_util
from mcp import mongo


class CompanyDetails(View):
#@app.route("/<string:komuna>/company/<string:name>")
    def dispatch_request(self, komuna, name):
        json = mongo.db.procurements.find(
            {
                "komuna.slug": komuna,
                "kompania.slug": name

            }
        )
        # pergjigjen e kthyer dhe te konvertuar ne JSON ne baze
        #te json_util.dumps() e ruajme ne  resp
        resp = Response(
            response=json_util.dumps(json),
            mimetype='application/json')

        # ne momentin kur hapim  sh.: http://127.0.0.1:5000/treemap
        # duhet te kthejme JSON, ne rastin tone resp.
        return resp
