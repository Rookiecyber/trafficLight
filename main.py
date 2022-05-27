
import os.path

import tornado.web
import tornado.ioloop
import tornado.websocket

import handlers

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from orm import Base


if __name__ == '__main__':
    db_url = 'mysql+mysqlconnector://kratos:123456@localhost/traffic?charset=utf8&autocommit=true'
    engine = create_engine(db_url,encoding='utf-8',echo=True)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    db = session_factory()

    app = tornado.web.Application(
          handlers=handlers.default_handlers,
          debug=True,
          template_path=os.path.join(os.path.dirname(__file__), "templates"),
          static_path=os.path.join(os.path.dirname(__file__), "static"),
          db=db
        )

    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

