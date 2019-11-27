import json

from peewee_async import MySQLDatabase
import peewee

from apps.utils.util_func import json_serial2
from webDB.handlers import RedisHandler
from webDB.settings import settings
from apps.manager.models import UserDB
from apps.utils.webDB_decorators import authenticated_async
from apps.manager.forms import DBRecordForm


class DBRecordHandler(RedisHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        # 获取用户的数据库记录
        re_data = []
        records_query = UserDB.filter(UserDB.owner==self.current_user)
        records = await self.application.objects.execute(records_query)
        for record in records:
            item = {
                'id': record.id,
                'owner_id': record.owner_id,
                'host': record.host,
                'port': record.port,
                'user': record.user,
                'db_type': record.db_type,
                'database': record.database,
                'note': record.note,
                'add_time': record.add_time,
                'last_login_time': record.last_login_time,
            }
            # print(record.host)
            re_data.append(item)
        self.finish(json.dumps(re_data, default=json_serial2))

    @authenticated_async
    async def post(self, *args, **kwargs):
        """
        创建一条数据库记录
        """
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


class DelRecordHandler(RedisHandler):
    @authenticated_async
    async def get(self, record_id, *args, **kwargs):
        # 删除数据库连接记录表
        re_data = {}
        try:
            record = await self.application.objects.get(UserDB, id=record_id, owner_id=self.current_user.id)
            await self.application.objects.delete(record)
            re_data['msg'] = 'OK'
        except UserDB.DoesNotExist as e:
            # 记录不存在
            self.set_status(404)
            re_data['error'] = "您所请求的数据不存在"
        self.finish(re_data)
