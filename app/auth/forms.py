#encoding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Regexp,EqualTo,Email

class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登陆')

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(),Regexp('^[A-Za-z_][A-Za-z0-9._]*$',0,'用户名由字母、数字、下划线组成')])
    department = StringField('所在部门') #,validators=[DataRequired()])
    email = StringField('电子邮件') #,validators=[Email()])
    landline = StringField('固定电话') #,validators=[Regexp('[0-9|-]{4,16}',0,'the length of landline must between 4-16')])
    cellphone = StringField('移动电话') #,validators=[Regexp('[0-9]{11}',0,'the length must be 11')])
    password_first = PasswordField('密码', validators=[DataRequired(),EqualTo('password_second',message='两次输入的密码不一致')])
    password_second = PasswordField('确认密码',validators=[DataRequired()])
    submit = SubmitField('注册用户')

class EditProfileForm(FlaskForm):
    department = StringField('所在部门', validators=[DataRequired()])
    email = StringField('电子邮件') #, validators=[Email()])
    landline = StringField('固定电话') #,validators=[Regexp('[0-9|-]{1,}', 0, )])
    cellphone = StringField('移动电话') #, validators=[Regexp('[0-9]{1,}', 0, )])
    submit = SubmitField('更新')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码',validators=[DataRequired()])
    new_password_first = PasswordField('新密码',validators= [
                DataRequired(),EqualTo('new_password_second',message='两次输入的密码不一致')])
    new_password_second = PasswordField('确认密码',validators=[DataRequired()])
    submit = SubmitField('更新')

class AddUserForm(RegistrationForm):
    submit = SubmitField('添加用户')