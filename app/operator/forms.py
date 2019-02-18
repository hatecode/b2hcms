#encoding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Regexp,EqualTo,Email

class HgstockForm(FlaskForm):
    b2hstock = StringField('B/H股代码')
    stkabbr = StringField('证券简称')
    hkstock = StringField('香港股票代码')