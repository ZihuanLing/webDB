import json

import aiomysql
from pymysql.err import OperationalError, ProgrammingError, InternalError

from apps.utils.util_func import json_serial2
from apps.utils.crypto import encrypt, decrypt
from webDB.handlers import RedisHandler
from apps.manager.models import UserDB, User
from apps.utils.webDB_decorators import authenticated_async
from apps.manager.forms import DBRecordForm


class DBRecordHandler(RedisHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        # 获取用户的数据库记录
        re_data = []
        records_query = UserDB.filter(UserDB.owner == self.current_user)
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
                'db': 'mysql'
            }
            if data.get('database'):
                db_config['db'] = data['database']
            # 测试配置是否正确
            try:
                conn = await aiomysql.connect(**db_config)
                # 测试连接成功，创建数据库记录
                # 拿到用户的独立秘钥
                user = await self.application.objects.get(User, id=self.current_user)
                aes_params = json.loads(user.secret_params)
                data['password'] = encrypt(aes_params, data['password'])
                record = await self.application.objects.create(UserDB,
                                                               owner=self.current_user, **data)
                re_data['record_id'] = record.id
                re_data['msg'] = '创建成功'
                conn.close()
            except ProgrammingError as e:
                # 一般为Mysql语句错误
                self.set_status(403)
                re_data['err_code'] = e.args[0]
                re_data['err_msg'] = e.args[2]
            except OperationalError as e:
                # 操作错误，可以是密码、端口号、数据库不存在等错误
                self.set_status(403)
                cause = e.__cause__.args
                re_data['err_code'] = cause[0]
                re_data['err_msg'] = cause[1]
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


class DBConnectHandler(RedisHandler):
    @authenticated_async
    async def get(self, record_id, *args, **kwargs):
        re_data = {}
        # 连接数据库
        try:
            record = await self.application.objects.get(UserDB, id=record_id, owner_id=self.current_user.id)
            user = await self.application.objects.get(User, id=self.current_user.id)
            aes_params = json.loads(user.secret_params)
            record.password = decrypt(aes_params, record.password)
            host = record.host
            password = record.password
            re_data['msg'] = 'Record OK'
        except UserDB.DoesNotExist as e:
            self.set_status(404)
            re_data['msg'] = '数据不存在'
        self.finish(re_data)


class DBOperateHandler(RedisHandler):
    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}
        param = json.loads(self.request.body.decode('utf8'))
        record = await self.application.objects.get(UserDB, id=param["record_id"],
                                                    owner_id=self.current_user.id)
        user = await self.application.objects.get(User, id=self.current_user.id)
        aes_params = json.loads(user.secret_params)
        record.password = decrypt(aes_params, record.password)
        password = record.password
        db_config = {
            'password': password,
            'host': record.host,
            'user': record.user,
            'port': record.port,
            'db': record.database
        }
        command = param['command']
        try:
            conn = await aiomysql.connect(**db_config)
            async with conn.cursor() as cur:
                await cur.execute(command)
                r = await cur.fetchall()
                await conn.commit()
                re_data['description'] = cur.description
                re_data['result'] = r
        except ProgrammingError as e:
            # 一般为Mysql语句错误
            self.set_status(403)
            re_data['err_code'] = e.args[0]
            re_data['err_msg'] = e.args[1]
        except OperationalError as e:
            # 操作错误，可以是密码、端口号、数据库不存在等错误
            self.set_status(403)
            cause = e.__cause__.args
            re_data['err_code'] = cause[0]
            re_data['err_msg'] = cause[1]
        except InternalError as e:
            # 一般为Mysql语句错误
            self.set_status(403)
            re_data['err_code'] = e.args[0]
            re_data['err_msg'] = e.args[1]
        conn.close()

        self.finish(json.dumps(re_data, default=json_serial2))
