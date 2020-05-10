from wtforms_tornado import Form
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Regexp, AnyOf, IPAddress
# from apps.users.models import PasswordField


class DBRecordForm(Form):
    host = StringField("主机", validators=[
        DataRequired(message="请输入主机ip"), IPAddress(message="请输入合法ip地址")
    ])
    port = IntegerField("端口", validators=[DataRequired(message="请输入端口号")])
    user = StringField("用户名", validators=[DataRequired(message="请输入用户名")])
    password = StringField("密码", validators=[DataRequired(message="请输入密码")])
    db_type = StringField("数据库类型", validators=[DataRequired(message="请输入数据库类型")])
    database = StringField("数据库")
    note = TextAreaField("备注信息")
