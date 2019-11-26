from tornado.web import url
from apps.manager.handler import *

urlpattern = [
    url("/DBRecord/?", CreateDBRecordHandler),
]