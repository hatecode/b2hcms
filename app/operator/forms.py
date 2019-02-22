#encoding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Regexp

class AddHgstockForm(FlaskForm):
    hgstock = StringField('B/H股代码'.decode('utf-8'), validators=[DataRequired(),Regexp('[0-9]{6}',message='必须为6位数字'.decode('utf-8'))])
    stkabbr = StringField('证券简称'.decode('utf-8'), validators=[DataRequired()])
    hkstock = StringField('香港股票代码'.decode('utf-8'), validators=[DataRequired(),Regexp('[0-9]{6}',message='必须为6位数字'.decode('utf-8'))])
    submit = SubmitField('submit')

class EditHgstockForm(AddHgstockForm):
    submit = SubmitField('edit')

class AddStockForm(FlaskForm):
    zqdm = StringField('证券代码'.decode('utf-8'), validators=[DataRequired(),Regexp('[0-9]{6}',message='必须为6位数字'.decode('utf-8'))])
    stkabbr = StringField('证券简称'.decode('utf-8'), validators=[DataRequired()])
    biztype = SelectField('业务类别'.decode('utf-8'), choices=[('','请选择'.decode('utf-8')),\
                         ('b2h','b转h'.decode('utf-8')),('hg','h股全流通'.decode('utf-8'))], validators=[DataRequired()])
    info = StringField('其他信息'.decode('utf-8'), default='there are some defaulted infos here', validators=[DataRequired()])
    submit = SubmitField('submit')

class EditStockForm(AddStockForm):
    submit = SubmitField('edit')

class AddSplitBasicForm(FlaskForm):
    zqdm = StringField('证券代码'.decode('utf-8'), validators=[DataRequired(),Regexp('[0-9]{6}',message='必须位6位数字'.decode('utf-8'))])
    sendtocsdc = SelectField('是否发送结算'.decode('utf-8'), choices=[('1','Y'),('0','N')])
    hassplitdetail = SelectField('是否配置详细路由'.decode('utf-8'), choices=[('1','Y'),('0','N')])
    agentid = StringField('代理券商id'.decode('utf-8'), validators=[DataRequired()])
    submit = SubmitField('submit')

class EditSplitBasicForm(AddSplitBasicForm):
    submit = SubmitField('edit')

class AddSplitDetailForm(FlaskForm):
    zqdm = StringField('证券代码'.decode('utf-8'), validators=[DataRequired(),Regexp('[0-9]{6}',message='必须位6位数字'.decode('utf-8'))])
    agentid = StringField('代理券商id'.decode('utf-8'), validators=[DataRequired()])
    broker = StringField('交易单元'.decode('utf-8'), validators=[DataRequired()])
    submit = SubmitField('submit')

class EditSplitDetailForm(AddSplitDetailForm):
    submit = SubmitField('edit')

class AddAgentForm(FlaskForm):
    agentid = StringField('代理券商id'.decode('utf-8'), validators=[DataRequired()])
    agentname = StringField('代理券商名称'.decode('utf-8'), validators=[DataRequired()])
    submit = SubmitField('submit')

class EditAgentForm(AddAgentForm):
    submit = SubmitField('edit')

class AddTWUserForm(FlaskForm):
    clientid = StringField('小站号'.decode('utf-8'), validators=[DataRequired()])
    groupid = StringField('组id'.decode('utf-8'), validators=[DataRequired()])
    istestuser = SelectField('是否位测试用户'.decode('utf-8'), choices=[('1','YES'),('0','NO')])
    ekey = StringField('EKEY序列号'.decode('utf-8'), validators=[DataRequired()])
    password = StringField('密码'.decode('utf-8'), validators=[DataRequired()])
    broker = TextAreaField('席位号'.decode('utf-8'), validators=[DataRequired()])
    submit = SubmitField('submit')

class EditTWUserForm(AddTWUserForm):
    submit = SubmitField('edit')

class AddBasicConfigForm(FlaskForm):
    baseconfigid = StringField('配置文件id'.decode('utf-8'), validators=[DataRequired()])
    baseconfigname = StringField('配置文件名称'.decode('utf-8'), validators=[DataRequired()])
    baseconfigcontent = TextAreaField('配置文件内容'.decode('utf-8'), validators=[DataRequired()])
    submit = SubmitField('submit')

class EditBasicConfigForm(AddBasicConfigForm):
    submit = SubmitField('edit')

class SearchForm(FlaskForm):
    filetype = SelectField(choices=[('','请选择'.decode('utf-8')),('basictype','基础配置'.decode('utf-8')),('biztype','业务配置'.decode('utf-8'))],
                           label='文件类型'.decode('utf-8'))
    filename = StringField(label='请输入文件名称'.decode('utf-8'),description='hgstock,stock,splitbasic,splitdetail,twuser,agent')

    actiontype = SelectField(choices=[('','请选择'.decode('utf-8')),('create','create'),('update','update'),('delete','delete'),('filedist','filedist')],
                             label='操作类型'.decode('utf-8'))
    user = StringField(label='用户'.decode('utf-8'))
    ip = StringField(label='用户ip'.decode('utf-8'))
    submit = SubmitField('submit')