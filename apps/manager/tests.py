import requests
import json
from random import choice, sample, randint
import redis
from datetime import datetime
from webDB.settings import settings
import jwt
import asyncio
from time import sleep
from pymysql.err import InternalError, OperationalError, ProgrammingError
# from pymysql import err

website_url = 'http://127.0.0.1:8888'
current_time = datetime.utcnow()

tsessionid_data = jwt.encode({
    'name': 'zihuan',
    'id': 3,
    'exp': current_time,
}, settings['secret_key']).decode('utf8')

headers = {
        'tsessionid': tsessionid_data
}


def create_db_record():
    # 创建数据表记录
    data = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'db_type': 'MYSQL',
        'database': 'mysql',
        'note': '本地数据表',
    }
    resp = requests.post(f"{website_url}/DBRecord", headers=headers, json=data)
    print(resp.status_code)
    try:
        print(json.loads(resp.text))
    except json.decoder.JSONDecodeError as e:
        print(resp.text)


def get_db_record():
    resp = requests.get(f"{website_url}/DBRecord", headers=headers)
    print(resp.status_code)
    try:
        print(json.loads(resp.text))
    except json.decoder.JSONDecodeError as e:
        print(resp.text)


def del_record(record_id):
    resp = requests.get(f"{website_url}/DelRecord/{record_id}", headers=headers)
    print(resp.status_code)
    try:
        print(json.loads(resp.text))
    except json.decoder.JSONDecodeError as e:
        print(resp.text)


def connect_db(record_id):
    resp = requests.get(f"{website_url}/ConnectDB/{record_id}", headers=headers)
    print(resp.status_code)
    try:
        print(json.loads(resp.text))
    except json.decoder.JSONDecodeError as e:
        print(resp.text)


def operate_db(record_id):
    data = {
        'record_id': record_id,
        'command': 'show tables;'
    }
    resp = requests.post(f"{website_url}/OperateDB/", headers=headers, json=data)
    # resp = requests.get(f"{website_url}/OperateDB/{record_id}", headers=headers)
    print(resp.status_code)
    try:
        print(json.loads(resp.text))
    except json.decoder.JSONDecodeError as e:
        print(resp.text)


names = ["Steve", "Paula", "Jerome", "Mara", "Rihanna", "Harris", "Julien", "Marlene", "Thalia", "Chanel", "Nikita", "Celia", "Fraser", "Pearl", "Pamela", "Marquis", "Ciaran", "Gillian", "Terrence", "Gina", "Rhianna", "Eileen", "Todd", "Lilia", "Louisa", "Charity", "Keenan", "Corinne", "Alessandro", "Theresa"]
classNames = ['C++', 'Java', 'PHP', 'Python', 'Nodejs', 'MySQL', 'MongoDB', 'JavaScript', 'Html5', 'Css3', 'Nginx']
teachers = ['Alex', 'Neil', 'Wallen', 'Willen', 'Jordan', 'Papi', 'Eureka', 'Dako', 'Shine']
def gen_phone():
    prefixs = ["133","149","153","173","177","180","181","189","199","130","131","132","145","155","156","166","171","175","176","185","186","166"]
    prefix = choice(prefixs)
    s = '12345678'
    phone = prefix + ''.join(sample(s, 8))
    return phone


def gen_SQL():
    name = choice(classNames)
    score = randint(50, 100)
    teacher = choice(teachers)
    user_id = randint(1, 100)
    address = choice(['Guangdong', 'Beijing', 'Shanghai', 'Zhejiang', 'Nanjing'])
    return f"INSERT INTO test_db.tbl_score (class_name, score, teacher, user_id) VALUES ('{name}', '{score}', '{teacher}', '{user_id}');"


async def sql_test2():
    import aiomysql
    config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'db': 'testdb',
        'port': 3306
    }
    # conn = await aiomysql.connect(**config)
    try:
        conn = await aiomysql.connect(**config)
        async with conn.cursor() as cur:
            SQL = "INSERT INTO `test` (`id`, `name`, `phone`, `age`, `gender`) VALUES (NULL, 'Lingzihuan', '13725761132', '13', 'male')"
            await cur.execute(SQL)
            await conn.commit()

        conn.close()
    except ProgrammingError as e:
        print("ProgrammingError")
        print(e.args[1])
    except OperationalError as e:
        print("OperationalError")
        cause = e.__cause__.args
        print("Error reason: ", cause[1])



async def sql_test():
    import aiomysql
    config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'db': 'test_db',
        'port': 3306
    }
    # conn = await aiomysql.connect(**config)
    for i in range(100):
        try:
            conn = await aiomysql.connect(**config)
            async with conn.cursor() as cur:
                # SQL = "INSERT INTO mxforum.test (name, phone, age, gender) VALUES ('xiaolan', '13812523651', '32', 'male');"
                SQL = gen_SQL()
                await cur.execute(SQL)
                await conn.commit()
            # sleep(15)
            conn.close()
        except ProgrammingError as e:
            print("ProgrammingError")
            print(e.args[1])
        except OperationalError as e:
            print("OperationalError")
            cause = e.__cause__.args
            print("Error reason: ", cause[1])
        finally:
            print(f'{i} - DONE')


async def main():
    # 测试用hash密码来连接MySQL数据库
    from webDB.settings import database
    from peewee_async import Manager
    from apps.manager.models import UserDB
    from peewee_async import MySQLDatabase
    import aiomysql
    obj = Manager(database)
    record = await obj.get(UserDB, id=2, owner_id=1)
    print(record.host)
    print(record.password)
    config = {
        'host': record.host,
        'port': record.port,
        'user': record.user,
        'password': 'root',
        'db': record.database,
    }
    conn = await aiomysql.connect(**config)

    async with conn.cursor() as cur:
        await cur.execute('select host, password from userdb where id=1 and owner_id=1')
        r = await cur.fetchall()
        print(r)
    conn.close()


def encrypt_test():
    from Crypto.Cipher import AES
    from binascii import b2a_hex, a2b_hex

    def add_to_16(text):
        # 用于加密的字符不足16的倍数，用空格补足
        if len(text.encode('utf8')) % 16:
            add = 16 - (len(text.encode('utf8')) % 16)
        else:
            add = 0
        return (text + ('\0' * add)).encode('utf8')

    key = "9999999999999999".encode('utf8')
    iv = b'qqqqqqqqqqqqqqqq'
    mode = AES.MODE_CBC
    word = "My name is zihuan.Ling, friend."
    word = add_to_16(word)
    # 加密：
    crypto = AES.new(key, mode, iv)
    text_encrypt = crypto.encrypt(word)
    print("Encrypt word: ", b2a_hex(text_encrypt))
    # 解密
    text_decrypt = crypto.decrypt(a2b_hex(text_encrypt))
    text_decrypt = bytes.decode(text_decrypt).rstrip('\0')
    print("Decrypt word: ", text_decrypt)


if __name__ == '__main__':
    # create_db_record()
    # connect_db(5)
    # operate_db(6)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(sql_test())

    # from apps.utils.crypto import encrypt, decrypt, AES_params
    # params = AES_params()
    # import json
    # s = json.dumps(params)
    # print(str(params))
    # text = "Hello my little pony!"
    # en = encrypt(params, text)
    # print('en:', en)
    # de = decrypt(params, en)
    # print('de:', de)

#     encrypt_test()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
    # create_db_record()
    # get_db_record()
    # del_record(2)
    # connect_db(1)
    pass

