from flask import Response
from flask.views import View
from bson import json_util
from mcp import mongo


class BudgetType(View):
    # /<string:komuna>/budget-type/<int:year>

    # /budget-type/<string:komuna>/<int:year>
    # /budget-type/<string:company_slug>
    def dispatch_request(self, komuna=None, year=None, company_slug=None):
        ''' Ruajme rezultatin qe na kthehet nga databaza permes ekzekutimit
            te kerkeses(Query) ne json.
        '''
        aggegation = []

        # If a commune or year is specified, create a match operation
        if komuna != None and year != None:
            match = {
                "$match": {
                    "komuna.slug": komuna,
                    "viti": year
                }
            }
            aggegation.append(match)
        # else do the match for company_slug, create a match operation
        elif company_slug != None:
            match = {
                "$match": {
                    "kompania.slug": company_slug,
                }
            }
            aggegation.append(match)

        # Create and add group aggregation operation
        group = {
                "$group": {
                    "_id": {
                        "tipi": "$tipiBugjetit"
                    },
                    "vlera": {
                        "$sum": "$kontrata.vlera"
                    },
                    "cmimi": {
                        "$sum": "$kontrata.qmimi"
                    },
                    "numriKontratave": {
                        "$sum": 1
                    }
                }
            }
        aggegation.append(group)

        # Create and add sort aggregation operation
        sort = {
            "$sort": {
                "_id.tipi": 1
            }
        }
        aggegation.append(sort)


        # Create and add project aggregation operation
        project = {
                "$project": {
                    "tipi": "$_id.tipi",
                    "vlera": "$vlera",
                    "cmimi": "$cmimi",
                    "nrKontratave": "$numriKontratave",
                    "_id": 0
                }
        }
        aggegation.append(project)


        # Execute aggregation
        json = mongo.db.procurements.aggregate(aggegation)

        resp = Response(
            response=json_util.dumps(json['result']),
            mimetype='application/json')

        return resp
