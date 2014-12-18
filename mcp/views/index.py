from flask.views import View

class Index(View):
    def dispatch_request(self):
        return "Welcome to Municipality Procurement API."
