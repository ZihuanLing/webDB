import json

from peewee_async import MySQLDatabase
import peewee

from apps.users.forms import *
from webDB.handlers import RedisHandler
from webDB.settings import settings
from apps.manager.models import UserDB
from apps.utils.webDB_decorators import authenticated_async
from apps.manager.forms import DBRecordForm


class CreateDBRecordHandler(RedisHandler):
    """
    创建一条数据库记录
    """
    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}
        param = json.loads(self.request.body.decode('utf8'))
        form = DBRecordForm.from_json(param)
        if form.validate():
            # 获取表单数据
            data = form.data
            db_config = {
                'host': data['host'],
                'user': data['user'],
                'password': data['password'],
                'port': data['port'],
                'database': 'mysql'
            }
            if data.get('database'):
                db_config['database'] = data['database']
            test_db = MySQLDatabase(**db_config)
            # 测试配置是否正确
            try:
                state = await test_db.connect_async()
                re_data['connect_state'] = state
                await test_db.close_async()
                # 测试连接成功，创建数据库记录
                record = await self.application.objects.create(UserDB,
                                                      owner=self.current_user, **data)
                re_data['record_id'] = record.id
                re_data['msg'] = '创建成功'
            except peewee.InternalError as e:
                self.set_status(400)
                re_data['error'] = e.__str__()
            except peewee.OperationalError as e:
                self.set_status(403)
                re_data['error'] = "连接失败，请检查您的用户名或密码"
        else:
            for field in form.errors:
                re_data[field] = form.errors[field][0]

        self.finish(re_data)

