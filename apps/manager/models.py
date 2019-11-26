from datetime import datetime

from peewee import *
from webDB.models import BaseModel

from apps.users.models import PasswordField, User

__all__ = ['UserDB']

# 数据库类型
DB_TYPE = (
    ('MYSQL', 'MYSQL')
)


class UserDB(BaseModel):
    # 用户的数据库记录
    owner = ForeignKeyField(User, verbose_name='拥有者')           # 该数据库属于哪个用户
    host = CharField(max_length=60, verbose_name='主机')           # 主机地址
    port = IntegerField(default=3306, verbose_name='连接端口')      # 主机地址
    user = CharField(max_length=50, verbose_name='用户名')         # 数据库用户
    password = PasswordField(verbose_name='密码')                  # 连接数据库的密码
    db_type = CharField(max_length=50, choices=DB_TYPE, default='MYSQL')    # 数据库类型
    database = CharField(max_length=50, verbose_name='数据库')       # 连接到哪个数据库
    note = TextField(verbose_name='备注', null=True)               # 备注信息
    add_time = DateTimeField(default=datetime.now(), verbose_name='创建时间')
    last_login_time = DateTimeField(null=True, default=None, verbose_name='上次连接时间')
