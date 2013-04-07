from tornado.web import RequestHandler
import simplejson as json


class SignupHandler(RequestHandler):

    def post(self):
        #self.render("about.html")
        body = json.loads(self.request.body)
        user = body["user"]
        if self.add_user(user):
            self.write({"success": "true"})
        else:
            self.write({"success": "false"})
        self.finish()

    def add_user(self, user):
        # check if the user alredy exists
        # return false if user already exists
        # else add to the database
        return True
