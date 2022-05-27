
from . import web_socket
from . import preview
from . import index
from . import userHandler

default_handlers = []
for mod in (web_socket,index,userHandler, preview):
    default_handlers.extend(mod.default_handlers)
