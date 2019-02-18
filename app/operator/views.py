from flask import render_template,redirect,url_for,request,make_response,jsonify,current_app
from flask_login import login_required
from .forms import *
from . import operator
from ..models import *
from sqlalchemy import and_,or_

@operator.route('/hgstock')
@login_required
def hgstock():
    return render_template('operator/hgstock.html')

@operator.route('/stock')
@login_required
def stock():
    return render_template('oprator/stock.html')

@operator.route('/agent')
@login_required
def agent():
    return render_template('operator/agent.html')

@operator.route('/twuser')
@login_required
def twuser():
    return render_template('operator/twuser.html')

@operator.route('/operationlog')
@login_required
def operationlog():
    return render_template('operator/operationlog.html')