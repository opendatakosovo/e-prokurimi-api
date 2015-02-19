from flask import Response
from flask.views import View
from bson import json_util
from mcp import mongo


class CompanyDetails(View):
    def dispatch_request(self, kompania_slug):

        #marrin te gjitha dokumentet per kompanine e caktuar
        json = mongo.db.procurements.find({"kompania.slug": kompania_slug})
        #pergjigjen e kthyer dhe te konvertuar ne JSON ne baze te json_util.dumps() e ruajme ne  resp
        resp = Response(
            response=json_util.dumps(json),
            mimetype='application/json')

        return resp
