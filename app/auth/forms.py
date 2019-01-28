#encoding:utf-8

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length

class LoginForm(FlaskForm):
    name = StringField('name',validators=[DataRequired(),Length(1,20)])
    password = PasswordField('password',validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('submit')