#encoding:utf-8

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Regexp,EqualTo,Email

class LoginForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('submit')

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(),Regexp('^[A-Za-z_][A-Za-z0-9._]*$',0,'the username \
            must compose of letters,numbers,dot,underline')])
    department = StringField('department') #,validators=[DataRequired()])
    email = StringField('email') #,validators=[Email()])
    landline = StringField('landline') #,validators=[Regexp('[0-9|-]{4,16}',0,'the length of landline must between 4-16')])
    cellphone = StringField('cellphone') #,validators=[Regexp('[0-9]{11}',0,'the length must be 11')])
    password_first = PasswordField('password', validators=[DataRequired(),EqualTo('password_second',message='password doesn\'t match')])
    password_second = PasswordField('confirm password',validators=[DataRequired()])
    submit = SubmitField('Register')

class EditProfileForm(FlaskForm):
    department = StringField('department', validators=[DataRequired()])
    email = StringField('email') #, validators=[Email()])
    landline = StringField('landline') #,validators=[Regexp('[0-9|-]{1,}', 0, )])
    cellphone = StringField('cellphone') #, validators=[Regexp('[0-9]{1,}', 0, )])
    submit = SubmitField('submit')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('old password',validators=[DataRequired()])
    new_password_first = PasswordField('new password',validators= [
                DataRequired(),EqualTo('new_password_second',message='password doesn\'t match')])
    new_password_second = PasswordField('confirm password',validators=[DataRequired()])
    submit = SubmitField('submit')
