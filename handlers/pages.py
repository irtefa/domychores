from tornado.web import RequestHandler


class Index(RequestHandler):

    def get(self):
        self.render('index.html')
