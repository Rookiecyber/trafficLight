import tornado.web
import tornado.ioloop


class PreviewHandler(tornado.web.RequestHandler):

    def get(self):

      name = self.get_arguments('name')
      if name == 'universe':
          universe = self.get_arguments('universe')

      self.render("preview.html")

default_handlers = [
    (r"/preview", PreviewHandler),
]
