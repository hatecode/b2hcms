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
    baseconfigid = db.Column(db.String(24),unique=True,index=True)
    baseconfigname = db.Column(db.String(24),nullable=False)
    baseconfigcontent = db.Column(db.UnicodeText,nullable=False)
    lastupdate = db.Column(db.DateTime,default=datetime.utcnow)

class Dbfsync(db.Model):
    __tablename__ = "dbfsyncs"
    id = db.Column(db.Integer,primary_key=True)
    dbfsyncid = db.Column(db.String(24),default='dbfsyncid')
    dbfsynccontent = db.Column(db.UnicodeText)

class OperationLog(db.Model):
    __tablename__ = "operationlogs"
    id = db.Column(db.Integer,primary_key=True)
    filename = db.Column(db.String(15),nullable=False,index=True)
    actiontype = db.Column(db.String(10),nullable=False,index=True)
    actiontime = db.Column(db.DateTime,default=datetime.now)
    actioncontent = db.Column(db.UnicodeText,nullable=True)
    user = db.Column(db.String(30),nullable=False,index=True)
    remote_addr = db.Column(db.String(20),index=True)

class HGStock(db.Model):
    __tablename__ = 'hgstocks'
    id = db.Column(db.Integer, primary_key=True)
    hgstock = db.Column(db.String(6), unique=True)
    stkabbr = db.Column(db.String(10))
    hkstock = db.Column(db.String(6), unique=True)
    lastupdate = db.Column(db.DateTime, default=datetime.utcnow)

class TWUser(db.Model):
    __tablename__ = 'twusers'
    id = db.Column(db.Integer, primary_key=True)
    clientid = db.Column(db.String(10), unique=True, index=True)
    groupid = db.Column(db.String(10))
    istestuser = db.Column(db.Boolean)
    ekey = db.Column(db.String(15))
    password = db.Column(db.String(20))
    broker = db.Column(db.String(50))
    lastupdate = db.Column(db.DateTime, default=datetime.utcnow)

class OperatorOperationLog(db.Model):
    __tablename__ = 'operatorslogs'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(15), nullable=False, index=True)
    actiontype = db.Column(db.String(10), nullable=False, index=True)
    actioncontent = db.Column(db.UnicodeText, nullable=True)
    user = db.Column(db.String(30), nullable=False, index=True)
    remote_addr = db.Column(db.String(20), index=True)
    filetype = db.Column(db.String(10), nullable=False, index=True)
    actiontime = db.Column(db.DateTime, default=datetime.now)

class Stock(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    zqdm = db.Column(db.String(6), unique=True, nullable=False)
    stkabbr = db.Column(db.String(12))
    biztype = db.Column(db.String(4))
    info = db.Column(db.String(128))
    lastupdate = db.Column(db.DateTime, default=datetime.utcnow)

    splitbases = db.relationship('SplitBase', uselist=False, backref='stock', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Stock %r>' % self.zqdm

    __str__ = __repr__

class SplitBase(db.Model):
    __tablename__ = 'splitbases'
    id = db.Column(db.Integer, primary_key=True)
    zqdm = db.Column(db.String(6), db.ForeignKey('stocks.zqdm', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, unique=True)
    sendtocsdc = db.Column(db.Boolean)
    hassplitdetail = db.Column(db.Boolean)
    agentid = db.Column(db.String(16), db.ForeignKey('agents.agentid', ondelete='CASCADE', onupdate='CASCADE'),nullable=False)
    lastupdate = db.Column(db.DateTime, default=datetime.utcnow)

    splitdetails = db.relationship('SplitDetail', uselist=False, backref='splitbase', cascade='all, delete-orphan')
    def __repr__(self):
        return '<SplitBase %r>' % self.zqdm

    __str__ = __repr__

class SplitDetail(db.Model):
    __tablename__ = 'splitdetails'
    id = db.Column(db.Integer, primary_key=True)
    zqdm = db.Column(db.String(6), db.ForeignKey('splitbases.zqdm', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    agentid = db.Column(db.String(16),nullable=False)
    broker = db.Column(db.String(64))
    lastupdate = db.Column(db.DateTime, default=datetime.utcnow)

class Agent(db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    agentid = db.Column(db.String(16), unique=True, nullable=False)
    agentname = db.Column(db.String(24))
    lastupdate = db.Column(db.DateTime, default=datetime.utcnow)

    splitbases = db.relationship('SplitBase', backref='agent',lazy='dynamic', cascade='all, delete-orphan')


