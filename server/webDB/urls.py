from apps.users.urls import urlpattern as user_urls
from apps.manager.urls import urlpattern as manager_urls
from webDB.handlers import MainHanler, MyStaticFileHandler


urlpattern = [
    (r'/?', MainHanler),
    (r'/media/(.*)', MyStaticFileHandler, {'path': 'media'})
]

urlpattern += user_urls
urlpattern += manager_urls
