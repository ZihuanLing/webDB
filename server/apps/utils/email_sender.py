# 异步发送邮件
import asyncio
import json
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.header import Header
import aiosmtplib
import logging
from webDB.settings import BASE_DIR
# print(BASE_DIR + "/apps/utils/smtp_config.json")
config_filename = BASE_DIR + "/apps/utils/smtp_config.json"

__all__ = ['send_email', ]

"""
smtp_config.json
----------------
{
  "from_addr" : "neil.ling@qq.com",
  "password" : "your password",
  "smtp_config" : {
    "hostname": "smtp.qq.com",
    "port": 465,
    "use_tls": 1
  }
}
"""


with open(config_filename, "r") as fp:
    config = json.load(fp)

from_addr = config['from_addr']
password = config['password']
smtp_config = config['smtp_config']


def _format_addr(s):
    # 格式化地址 也方便发送中文
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


async def send_email(to_addr, code, expire):
    """发送邮件，主要参数为：
    to_addr: 目标邮件地址
    code: 验证码
    expire: 验证码过期时间
    """
    html = f"""
    <html>
    <body>
    <h3>亲爱的<a data-auto-link="1" href="mailto:{to_addr}" target="_blank">{to_addr}</a>,您好:</h3>
    您本次的注册验证码为：<br><p style="
    background-color: #cbd4d3;
    width: auto;
    display: inline-block;
    padding: 5px 10px;
    border-radius: 10px;
    font-weight: bold;
    color: #292424;
    ">{code}</p><br>
    请在<span style="font-weight:bold">{expire}</span>分钟内输入。
    <p>如非本人操作，可能是其他用户误输入了您的邮箱地址，请忽略此封邮件。</p>
    </body>
    </html>
    """

    msg = MIMEText(html, 'html', 'utf-8')
    msg['From'] = _format_addr('web database <%s>' % from_addr)
    msg['To'] = _format_addr('尊敬的用户 <%s>' % to_addr)
    msg['Subject'] = Header('注册验证码', 'utf-8').encode()

    try:
        async with aiosmtplib.SMTP(**smtp_config) as smtp:
            await smtp.login(from_addr, password)
            res = await smtp.send_message(msg)
    except aiosmtplib.SMTPException as e:
        logging.error('sendemail:%s' % e)


if __name__ == '__main__':
    pass
    to_addr = "16zhling@stu.edu.cn"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_email(to_addr, '1234', 10))
