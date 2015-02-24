from flask import Response
from flask.views import View
from bson import json_util
from mcp import mongo
import pymongo


class CompanyDetails(View):
    def dispatch_request(self, kompania_slug):

        json = mongo.db.procurements.find({"kompania.slug": kompania_slug}).sort('dataNenshkrimit', pymongo.DESCENDING)

        resp = Response(
            response=json_util.dumps(json),
            mimetype='application/json')

        return resp
