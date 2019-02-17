#encoding:utf-8
from datetime import datetime

from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,current_user

from . import db,login_manager

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),unique=True,index=True)
    password_hash = db.Column(db.String(128),nullable=False)
    is_admin = db.Column(db.Boolean,default=False)
    department = db.Column(db.String(32))
    email = db.Column(db.String(32))
    cellphone = db.Column(db.String(11))
    landline = db.Column(db.String(12))

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def reset_password(self,username,default_password='123456'):
        if current_user.is_admin:
            user = User.query(username=username).first()
            if user:
                user.password = default_password
                db.session.add(user)
            else:
                return False
            return True
        return False

    def __str__(self):
        return '[User]:{0}'.format(self.username)

    __repr__ = __str__

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class BaseConfig(db.Model):
    __tablename__ = "baseconfigs"
    id = db.Column(db.Integer,primary_key=True)
    baseconfigid = db.Column(db.String(10),unique=True,index=True)
    baseconfigname = db.Column(db.String(10),nullable=False)
    baseconfigcontent = db.Column(db.UnicodeText,nullable=False)
    lastupdate = db.Column(db.DateTime,default=datetime.utcnow)

class Dbfsync(db.Model):
    __tablename__ = "dbfsyncs"
    id = db.Column(db.Integer,primary_key=True)
    dbfsyncid = db.Column(db.String(10),default='dbfsyncid')
    dbfsynccontent = db.Column(db.UnicodeText,nullable=False)

class OperationLog(db.Model):
    __tablename__ = "operationlogs"
    id = db.Column(db.Integer,primary_key=True)
    filename = db.Column(db.String(15),nullable=False,index=True)
    actiontype = db.Column(db.String(10),nullable=False,index=True)
    actiontime = db.Column(db.DateTime,default=datetime.utcnow)
    actioncontent = db.Column(db.UnicodeText,nullable=True)
    user = db.Column(db.String(30),nullable=False,index=True)
    remote_addr = db.Column(db.String(20),index=True)

