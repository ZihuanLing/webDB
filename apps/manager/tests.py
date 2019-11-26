import requests
import json
import redis
from datetime import datetime
from webDB.settings import settings
import jwt


website_url = 'http://127.0.0.1:8888'
current_time = datetime.utcnow()

tsessionid_data = jwt.encode({
    'name': 'zihuan',
    'id': 2,
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


if __name__ == '__main__':
    create_db_record()
