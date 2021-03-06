from tornado.web import url
from apps.manager.handler import *

urlpattern = [
    url("/DBRecord/?", DBRecordHandler),
    url(r"/DelRecord/(\d+)/?", DelRecordHandler),
    url(r"/ConnectDB/(\d+)/?", DBConnectHandler),
    url(r"/OperateDB/?", DBOperateHandler),
]