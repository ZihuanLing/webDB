from tornado.web import Application
from tornado.ioloop import IOLoop
from peewee_async import Manager

from webDB.urls import urlpattern
from webDB.settings import database, settings

if __name__ == '__main__':
    # 集成json到wtforms
    import wtforms_json
    wtforms_json.init()

    app = Application(urlpattern, debug=True, **settings)
    app.listen(8888)

    database.set_allow_sync(False)
    objects = Manager(database)

    app.objects = objects

    io_loop = IOLoop()
    io_loop.current().start()
