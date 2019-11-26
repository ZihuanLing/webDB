from peewee import MySQLDatabase

from webDB.settings import settings
from apps.users.models import *


database = MySQLDatabase(**settings['db'])


def init():
    database.create_tables([User])


if __name__ == '__main__':
    init()
