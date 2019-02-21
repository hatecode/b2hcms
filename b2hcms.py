import os
from flask_migrate import Migrate
from flask import Flask
from app import create_app,db
from app.models import *

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User,BaseConfig=BaseConfig,Dbfsync=Dbfsync,OperationLog=OperationLog,Stock=Stock,
                SplitBase=SplitBase,SplitDetail=SplitDetail,Agent=Agent,OperatorOperationLog=OperatorOperationLog,
                TWUser=TWUser,HGStock=HGStock)