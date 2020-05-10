from peewee import MySQLDatabase

from webDB.settings import settings
from apps.users.models import *
from apps.manager.models import UserDB

database = MySQLDatabase(**settings['db'])


def init():
    database.create_tables([User])
    database.create_tables([UserDB])


if __name__ == '__main__':
    init()
