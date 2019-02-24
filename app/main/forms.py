#encoding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Regexp,EqualTo,Email

class AddBaseConfigForm(FlaskForm):
    baseconfigid = StringField('配置文件id',validators=[DataRequired()])
    baseconfigname = StringField('配置文件名称',validators=[DataRequired()])
    baseconfigcontent = TextAreaField('配置文件内容',validators=[DataRequired()])
    submit = SubmitField('提交')

class EditBaseConfigForm(AddBaseConfigForm):
    submit = SubmitField('更新')

class DbfsyncForm(FlaskForm):
    id = StringField('文件id',default='dbfsyncid')
    content = TextAreaField('文件内容',validators=[DataRequired()])
    submit = SubmitField('提交')

class SearchForm(FlaskForm):
    filename = SelectField(choices=[('','请选择'),('dbfsync','dbfsync'),('baseconfig','baseconfig'),('user','user')],
                         label='文件名称')

    actiontype = SelectField(choices=[('','请选择'),('create','create'),('update','update'),('delete','delete')],
                             label='操作类型')
    user = StringField(label='用户')
    ip = StringField(label='ip地址')
    submit = SubmitField('查询')
