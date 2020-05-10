import os

import peewee_async

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = {
    'static_url_prefix': '/static/',                # 静态文件的访问前缀 - localhost:8888/static
    'template_path': 'templates',                   # 模板路径 - 使用相对路径
    'secret_key': 'PG9M72exnaisrSVR',
    'jwt_expire': 24*3600,                          # jwt过期时间为一天
    'code_expire': 10*60,                              # 验证码过期时间为10分钟
    'MEDIA_ROOT': os.path.join(BASE_DIR, 'media'),
    'SITE_URL': 'http://127.0.0.1:8888',
    'db': {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'database': 'web_db',
        'port': 3306
    },
    'redis': {
        'host': '127.0.0.1',
    },
}

database = peewee_async.MySQLDatabase(**settings['db'])
