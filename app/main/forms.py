#encoding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Regexp,EqualTo,Email

class AddBaseConfigForm(FlaskForm):
    baseconfigid = StringField('configid',validators=[DataRequired()])
    baseconfigname = StringField('configname',validators=[DataRequired()])
    baseconfigcontent = TextAreaField('configcontent',validators=[DataRequired()])
    submit = SubmitField('submit')

class EditBaseConfigForm(AddBaseConfigForm):
    submit = SubmitField('edit')

class DbfsyncForm(FlaskForm):
    dbfsyncid = StringField('dbfsyncid')
    dbfsynccontent = TextAreaField('dbfsynccontent',validators=[DataRequired()])
    submit = SubmitField('submit')

class SearchForm(FlaskForm):
    filename = SelectField(choices=[('',''),('dbfsync','dbfsync'),('baseconfig','baseconfig'),('filedist','filedist')],
                         label='filename')

    actiontype = SelectField(choices=[('',''),('create','create'),('update','update'),('delete','delete'),('filedist','filedist')],
                             label='actiontype')
    user = StringField(label='user')
    ip = StringField(label='ip')
    submit = SubmitField('submit')
