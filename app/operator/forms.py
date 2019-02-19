#encoding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Regexp

class HgstockForm(FlaskForm):
    b2hstock = StringField('B/H股代码', validators=[DataRequired(),Regexp('[0-9]{6}',message='必须为6位数字')])
    stkabbr = StringField('证券简称', validators=[DataRequired()])
    hkstock = StringField('香港股票代码', validators=[DataRequired])
    submit = SubmitField('submit')

class StockForm(FlaskForm):
    zqdm = StringField('证券代码', validators=[DataRequired(),Regexp('[0-9]{6}',message='必须为6位数字')])
    stkabbr = StringField('证券简称', validators=[DataRequired()])
    biztype = SelectField('业务类别', choices=[('','请选择'),('b2h','b转h'),('hg','h股全流通')], validators=[DataRequired()])
    info = StringField('其他信息', default='there are some defaulted infos here', validators=[DataRequired()])
    submit = SubmitField('submit')

class SplitBasicForm(FlaskForm):
    zqdm = StringField('证券代码', validators=[DataRequired(),Regexp('[0-9]{6}',message='必须位6位数字')])
    sendtocsdc = SelectField('是否发送结算', choices=[('Y','Y'),('N','N')])
    hassplitdetail = SelectField('是否配置详细路由', choices=[('Y','Y'),('N','N')])
    agentid = StringField('代理券商id', validators=[DataRequired()])
    submit = SubmitField('submit')

class SplitDetailForm(FlaskForm):
    zqdm = StringField('证券代码', validators=[DataRequired(),Regexp('[0-9]{6}',message='必须位6位数字')])
    agentid = StringField('代理券商id', validators=[DataRequired()])
    tradeunit = StringField('交易单元', validators=[DataRequired(),Regexp('[0-9]{6}',message='必须位6位数字')])
    submit = SubmitField('submit')

class AgentForm(FlaskForm):
    agentid = StringField('代理券商id', validators=[DataRequired()])
    agentname = StringField('代理券商名称', validators=[DataRequired()])
    submit = SubmitField('submit')

class TWUserForm(FlaskForm):
    clientid = StringField('小站号', validators=[DataRequired()])
    groupid = StringField('组id', validators=[DataRequired()])
    istestuser = SelectField('是否位测试用户', choices=[('Y','Y'),('N','N')])
    Ekey = StringField('EKEY序列号', validators=[DataRequired()])
    password = StringField('密码', validators=[DataRequired()])
    broker = TextAreaField('席位号', validators=[DataRequired()])
    submit = SubmitField('submit')

class BasicConfigForm(FlaskForm):
    baseconfigid = StringField('configid', validators=[DataRequired()])
    baseconfigname = StringField('configname', validators=[DataRequired()])
    baseconfigcontent = TextAreaField('configcontent', validators=[DataRequired()])
    submit = SubmitField('submit')