#encoding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Regexp

class AddHgstockForm(FlaskForm):
    hgstock = StringField('B/H股代码', validators=[DataRequired(),Regexp('[0-9]{6}',message='必须为6位数字')])
    stkabbr = StringField('证券简称', validators=[DataRequired()])
    hkstock = StringField('香港股票代码', validators=[DataRequired(),Regexp('[0-9]{6}',message='必须为6位数字')])
    submit = SubmitField('提交')

class EditHgstockForm(AddHgstockForm):
    submit = SubmitField('更新')

class AddStockForm(FlaskForm):
    zqdm = StringField('证券代码', validators=[DataRequired(),Regexp('[0-9]{6}',message='必须为6位数字')])
    stkabbr = StringField('证券简称', validators=[DataRequired()])
    biztype = SelectField('业务类别', choices=[('','请选择'),\
                         ('b2h','b转h'),('hg','h股全流通')], validators=[DataRequired()])
    info = StringField('其他信息', default='there are some default infos here', validators=[DataRequired()])
    submit = SubmitField('提交')

class EditStockForm(AddStockForm):
    submit = SubmitField('更新')

class AddSplitBasicForm(FlaskForm):
    zqdm = StringField('证券代码', validators=[DataRequired(),Regexp('[0-9]{6}',message='必须位6位数字')])
    sendtocsdc = SelectField('是否发送结算', choices=[('1','Y'),('0','N')])
    hassplitdetail = SelectField('是否配置详细路由', choices=[('1','Y'),('0','N')])
    agentid = StringField('代理券商id', validators=[DataRequired()])
    submit = SubmitField('提交')

class EditSplitBasicForm(AddSplitBasicForm):
    submit = SubmitField('更新')

class AddSplitDetailForm(FlaskForm):
    zqdm = StringField('证券代码', validators=[DataRequired(),Regexp('[0-9]{6}',message='必须位6位数字')])
    agentid = StringField('代理券商id', validators=[DataRequired()])
    broker = StringField('交易单元', validators=[DataRequired()])
    submit = SubmitField('提交')

class EditSplitDetailForm(AddSplitDetailForm):
    submit = SubmitField('更新')

class AddAgentForm(FlaskForm):
    agentid = StringField('代理券商id', validators=[DataRequired()])
    agentname = StringField('代理券商名称', validators=[DataRequired()])
    submit = SubmitField('提交')

class EditAgentForm(AddAgentForm):
    submit = SubmitField('更新')

class AddTWUserForm(FlaskForm):
    clientid = StringField('小站号', validators=[DataRequired()])
    groupid = StringField('组id', validators=[DataRequired()])
    istestuser = SelectField('是否位测试用户', choices=[('1','YES'),('0','NO')])
    ekey = StringField('EKEY序列号', validators=[DataRequired()])
    password = StringField('密码', validators=[DataRequired()])
    broker = TextAreaField('席位号', validators=[DataRequired()])
    submit = SubmitField('提交')

class EditTWUserForm(AddTWUserForm):
    submit = SubmitField('更新')

class AddBasicConfigForm(FlaskForm):
    baseconfigid = StringField('配置文件id', validators=[DataRequired()])
    baseconfigname = StringField('配置文件名称', validators=[DataRequired()])
    baseconfigcontent = TextAreaField('配置文件内容', validators=[DataRequired()])
    submit = SubmitField('提交')

class EditBasicConfigForm(AddBasicConfigForm):
    submit = SubmitField('更新')

class SearchForm(FlaskForm):
    filetype = SelectField(choices=[('','请选择'),('基础配置','基础配置'),('业务配置','业务配置')],
                           label='文件类型')
    filename = StringField(label='请输入文件名称',description='文件有：hgstock,stock,splitbasic,splitdetail,twuser,agent,dbfsync')

    actiontype = SelectField(choices=[('','请选择'),('create','create'),('update','update'),('delete','delete'),('filedist','filedist')],
                             label='操作类型')
    user = StringField(label='用户')
    ip = StringField(label='用户ip')
    submit = SubmitField('查询')