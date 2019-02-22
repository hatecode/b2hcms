from flask import render_template,redirect,url_for,request,make_response,jsonify,current_app
from flask_login import login_required
from .forms import *
from . import operator
from ..models import *
from sqlalchemy import and_,or_

@operator.route('/hgstock')
@login_required
def hgstock():
    page = request.args.get('page', 1, type=int)
    pagination = HGStock.query.order_by(HGStock.lastupdate.desc()).paginate(
        page, per_page=current_app.config['FLASKY_LOG_PER_PAGE'], error_out=False)
    hgstocks = pagination.items
    return render_template('operator/hgstock/hgstock.html',pagination=pagination,hgstocks=hgstocks)

@operator.route('/addhgstock',methods=['GET','POST'])
@login_required
def addhgstock():
    form = AddHgstockForm()
    if form.validate_on_submit():
            hgstock = HGStock(hgstock=form.hgstock.data,
                              stkabbr=form.stkabbr.data,
                              hkstock=form.hkstock.data,
                              lastupdate=datetime.now())
            log = OperatorOperationLog(filetype='basictype',
                                       filename='hgstock',
                                       actiontype='create',
                                       actioncontent='create a hgstock:'+
                                                     ' hgstock='+form.hgstock.data +
                                                     ' stkabbr='+form.stkabbr.data +
                                                     ' hkstock='+form.hkstock.data ,
                                       actiontime=datetime.now(),
                                       user=current_user.username,
                                       remote_addr=request.remote_addr)
            try:
                db.session.add_all([log,hgstock])
                db.session.commit()
            except Exception,e:
                db.session.rollback()
                return str(e)
            return redirect(url_for('operator.hgstock'))
    return render_template('operator/hgstock/addhgstock.html',form=form)

@operator.route('/edithgstock',methods=['GET','POST'])
@login_required
def edithgstock():
    form = EditHgstockForm()
    req_hgstock = request.args.get('hgstock')
    db_hgstock = HGStock.query.filter_by(hgstock=req_hgstock).first()
    if form.validate_on_submit():
        log = OperatorOperationLog(filetype='basictype',
                                   filename='hgstock',
                                   actiontype='update',
                                   actioncontent='update a hgstock,new:' +
                                                 ' hgstock=' + form.hgstock.data +
                                                 ' stkabbr=' + form.stkabbr.data +
                                                 ' hkstock=' + form.hkstock.data +
                                                 ' old:'+
                                                 ' hgstock='+db_hgstock.hgstock +
                                                 ' stkabbr=' + db_hgstock.stkabbr +
                                                 ' hkstock='+db_hgstock.hkstock ,
                                   actiontime=datetime.now(),
                                   user=current_user.username,
                                   remote_addr=request.remote_addr)
        db_hgstock.hgstock = form.hgstock.data
        db_hgstock.stkabbr = form.stkabbr.data
        db_hgstock.hkstock = form.hkstock.data
        db_hgstock.lastupdate = datetime.now()
        try:
            db.session.add_all([log, db_hgstock])
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
        return redirect(url_for('operator.hgstock'))
    if db_hgstock is not None:
        form.hgstock.data = db_hgstock.hgstock
        form.stkabbr.data = db_hgstock.stkabbr
        form.hkstock.data = db_hgstock.hkstock
    else:
        return 'the hgstock record: %s doesn\'t exist' % req_hgstock
    return render_template('operator/hgstock/edithgstock.html',form=form)

@operator.route('/delhgstock')
@login_required
def delhgstock():
    req_hgstock = request.args.get('hgstock')
    db_hgstock = HGStock.query.filter_by(hgstock=req_hgstock).first()
    if db_hgstock is not None:
        log = OperatorOperationLog(filetype='basictype',
                                   filename='hgstock',
                                   actiontype='delete',
                                   actioncontent='delete a hgstock:' +
                                                 ' hgstock=' + db_hgstock.hgstock +
                                                 ' stkabbr=' + db_hgstock.stkabbr +
                                                 ' hkstock=' + db_hgstock.hkstock ,
                                   actiontime=datetime.now(),
                                   user=current_user.username,
                                   remote_addr=request.remote_addr)
        try:
            db.session.add(log)
            db.session.delete(db_hgstock)
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
        return redirect(url_for('operator.hgstock'))
    return 'the hgstock ; %s doesn\'t exist' % req_hgstock

@operator.route('/stock')
@login_required
def stock():
    page = request.args.get('page', 1, type=int)
    pagination = Stock.query.order_by(Stock.lastupdate.desc()).paginate(
        page, per_page=current_app.config['FLASKY_LOG_PER_PAGE'], error_out=False)
    stocks = pagination.items
    return render_template('operator/stock/stock.html', pagination=pagination, stocks=stocks)

@operator.route('/addstock',methods=['GET','POST'])
@login_required
def addstock():
    form = AddStockForm()
    if form.validate_on_submit():
            stock = Stock(zqdm=form.zqdm.data,
                          stkabbr=form.stkabbr.data,
                          biztype=form.biztype.data,
                          info = form.info.data,
                          lastupdate=datetime.now())
            log = OperatorOperationLog(filetype='basictype',
                                       filename='stock',
                                       actiontype='create',
                                       actioncontent='create a stock:' +
                                                     ' zqdm='+form.zqdm.data +
                                                     ' stkabbr='+form.stkabbr.data +
                                                     ' biztype='+form.biztype.data +
                                                     ' info='+form.info.data ,
                                       actiontime=datetime.now(),
                                       user=current_user.username,
                                       remote_addr=request.remote_addr)
            try:
                db.session.add_all([log,stock])
                db.session.commit()
            except Exception,e:
                db.session.rollback()
                return str(e)
            return redirect(url_for('operator.stock'))
    return render_template('operator/stock/addstock.html',form=form)

@operator.route('/editstock',methods=['GET','POST'])
@login_required
def editstock():
    form = EditStockForm()
    req_zqdm = request.args.get('zqdm')
    db_stock = Stock.query.filter_by(zqdm=req_zqdm).first()
    if form.validate_on_submit():
        log = OperatorOperationLog(filetype='basictype',
                                   filename='stock',
                                   actiontype='update',
                                   actioncontent='update a stock,new:' +
                                                 ' zqdm=' + form.zqdm.data +
                                                 ' stkabbr=' + form.stkabbr.data +
                                                 ' biztype=' + form.biztype.data +
                                                 ' info=' + form.info.data +
                                                 ' old:'+
                                                 ' zqdm='+db_stock.zqdm+
                                                 ' stkabbr=' + db_stock.stkabbr +
                                                 ' biztype='+db_stock.biztype +
                                                 ' info=' + db_stock.info ,
                                   actiontime=datetime.now(),
                                   user=current_user.username,
                                   remote_addr=request.remote_addr)
        db_stock.zqdm = form.zqdm.data
        db_stock.stkabbr = form.stkabbr.data
        db_stock.biztype = form.biztype.data
        db_stock.info = form.info.data
        db_stock.lastupdate = datetime.now()
        try:
            db.session.add_all([log, db_stock])
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
        return redirect(url_for('operator.stock'))
    if db_stock is not None:
        form.zqdm.data = db_stock.zqdm
        form.stkabbr.data = db_stock.stkabbr
        form.biztype.data = db_stock.biztype
        form.info.data = db_stock.info
    else:
        return 'the zqdm record: %s doesn\'t exist' % req_zqdm
    return render_template('operator/stock/editstock.html',form=form)

@operator.route('/delstock')
@login_required
def delstock():
    req_zqdm = request.args.get('zqdm')
    db_stock = Stock.query.filter_by(zqdm=req_zqdm).first()
    if db_stock is not None:
        log = OperatorOperationLog(filetype='basictype',
                                   filename='stock',
                                   actiontype='delete',
                                   actioncontent='delete a stock:' +
                                                 ' zqdm=' + db_stock.zqdm +
                                                 ' stkabbr=' + db_stock.stkabbr +
                                                 ' biztype=' + db_stock.biztype +
                                                 ' info=' + db_stock.info ,
                                   actiontime=datetime.now(),
                                   user=current_user.username,
                                   remote_addr=request.remote_addr)
        try:
            db.session.add(log)
            db.session.delete(db_stock)
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
        return redirect(url_for('operator.stock'))
    return 'the zqdm ; %s doesn\'t exist' % req_zqdm

@operator.route('/splitbase')
@login_required
def splitbase():
    page = request.args.get('page', 1, type=int)
    pagination = SplitBase.query.order_by(SplitBase.lastupdate.desc()).paginate(
        page, per_page=current_app.config['FLASKY_LOG_PER_PAGE'], error_out=False)
    splitbases = pagination.items
    return render_template('operator/splitbase/splitbase.html', pagination=pagination, splitbases=splitbases)

@operator.route('/addsplitbase',methods=['GET','POST'])
@login_required
def addsplitbase():
    form = AddSplitBasicForm()
    if form.validate_on_submit():
            splitbase = SplitBase(zqdm=form.zqdm.data,
                                  sendtocsdc=int(form.sendtocsdc.data),
                                  hassplitdetail=int(form.hassplitdetail.data),
                                  agentid = form.agentid.data,
                                  lastupdate=datetime.now())
            log = OperatorOperationLog(filetype='basictype',
                                       filename='splitbase',
                                       actiontype='create',
                                       actioncontent='create a splitbase:' +
                                                     ' zqdm='+form.zqdm.data +
                                                     ' sendtocsdc='+form.sendtocsdc.data +
                                                     ' hassplitdetail='+form.hassplitdetail.data +
                                                     ' agentid='+form.agentid.data ,
                                       actiontime=datetime.now(),
                                       user=current_user.username,
                                       remote_addr=request.remote_addr)
            try:
                db.session.add_all([log,splitbase])
                db.session.commit()
            except Exception,e:
                db.session.rollback()
                return str(e)
            return redirect(url_for('operator.splitbase'))
    return render_template('operator/splitbase/addsplitbase.html',form=form)

@operator.route('/editsplitbase',methods=['GET','POST'])
@login_required
def editsplitbase():
    form = EditSplitBasicForm()
    req_zqdm = request.args.get('zqdm')
    db_splitbase = SplitBase.query.filter_by(zqdm=req_zqdm).first()
    if form.validate_on_submit():
        log = OperatorOperationLog(filetype='basictype',
                                   filename='splitbase',
                                   actiontype='update',
                                   actioncontent='update a splitbase,new:' +
                                         ' zqdm=' + form.zqdm.data +
                                         ' sendtocsdc=' + form.sendtocsdc.data +
                                         ' hassplitdetail=' + form.hassplitdetail.data +
                                         ' agentid=' + form.agentid.data +
                                         ' old:'+
                                         ' zqdm='+db_splitbase.zqdm +
                                         ' sendtocsdc=' + db_splitbase.sendtocsdc +
                                         ' hassplitdetail='+db_splitbase.hassplitdetail +
                                         ' agentid=' + db_splitbase.agentid ,
                                   actiontime=datetime.now(),
                                   user=current_user.username,
                                   remote_addr=request.remote_addr)
        db_splitbase.zqdm = form.zqdm.data
        db_splitbase.sendtocsdc = form.sendtocsdc.data
        db_splitbase.hassplitdetail = form.hassplitdetail.data
        db_splitbase.agentid = form.agentid.data
        db_splitbase.lastupdate = datetime.now()
        try:
            db.session.add_all([log, db_splitbase])
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
        return redirect(url_for('operator.splitbase'))
    if db_splitbase is not None:
        form.zqdm.data = db_splitbase.zqdm
        form.sendtocsdc.data = db_splitbase.sendtocsdc
        form.hassplitdetail.data = db_splitbase.hassplitdetail
        form.agentid.data = db_splitbase.agentid
    else:
        return 'the zqdm record: %s doesn\'t exist' % req_zqdm
    return render_template('operator/splitbase/editsplitbase.html',form=form)

@operator.route('/delsplitbase')
@login_required
def delsplitbase():
    req_zqdm = request.args.get('zqdm')
    db_splitbase = SplitBase.query.filter_by(zqdm=req_zqdm).first()
    if db_splitbase is not None:
        log = OperatorOperationLog(filetype='basictype',
                                   filename='splitbase',
                                   actiontype='delete',
                                   actioncontent='delete a splitbase:' +
                                                 ' zqdm=' + db_splitbase.zqdm +
                                                 ' sendtocsdc=' + db_splitbase.sendtocsdc +
                                                 ' hassplitdetail=' + db_splitbase.hassplitdetail +
                                                 ' agentid=' + db_splitbase.agentid ,
                                   actiontime=datetime.now(),
                                   user=current_user.username,
                                   remote_addr=request.remote_addr)
        try:
            db.session.add(log)
            db.session.delete(db_splitbase)
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
        return redirect(url_for('operator.splitbase'))
    return 'the zqdm ; %s doesn\'t exist' % req_zqdm

@operator.route('/splitdetail')
@login_required
def splitdetail():
    page = request.args.get('page', 1, type=int)
    pagination = SplitDetail.query.order_by(SplitDetail.lastupdate.desc()).paginate(
        page, per_page=current_app.config['FLASKY_LOG_PER_PAGE'], error_out=False)
    splitdetails = pagination.items
    return render_template('operator/splitdetail/splitdetail.html', pagination=pagination, splitdetails=splitdetails)

@operator.route('/addsplitdetail',methods=['GET','POST'])
@login_required
def addsplitdetail():
    form = AddSplitDetailForm()
    if form.validate_on_submit():
        splitdetail = SplitDetail(zqdm=form.zqdm.data,
                                  broker=form.broker.data,
                                  agentid = form.agentid.data,
                                  lastupdate=datetime.now())
        log = OperatorOperationLog(filetype='basictype',
                                   filename='splitdetail',
                                   actiontype='create',
                                   actioncontent='create a splitdetail:' +
                                                 ' zqdm='+form.zqdm.data +
                                                 ' broker='+form.broker.data +
                                                 ' agentid='+form.agentid.data ,
                                   actiontime=datetime.now(),
                                   user=current_user.username,
                                   remote_addr=request.remote_addr)
        try:
            db.session.add_all([log,splitdetail])
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
        return redirect(url_for('operator.splitdetail'))
    return render_template('operator/splitdetail/addsplitdetail.html',form=form)

@operator.route('/editsplitdetail',methods=['GET','POST'])
@login_required
def editsplitdetail():
    form = EditSplitDetailForm()
    req_zqdm = request.args.get('zqdm')
    db_splitdetail = SplitDetail.query.filter_by(zqdm=req_zqdm).first()
    if form.validate_on_submit():
        log = OperatorOperationLog(filetype='basictype',
                                   filename='splitdetail',
                                   actiontype='update',
                                   actioncontent='update a splitdetail,new:' +
                                                 ' zqdm=' + form.zqdm.data +
                                                 ' broker=' + form.broker.data +
                                                 ' agentid=' + form.agentid.data +
                                                 ' old:'+
                                                 ' zqdm='+db_splitdetail.zqdm +
                                                 ' broker=' + db_splitdetail.broker +
                                                 ' agentid=' + db_splitdetail.agentid ,
                                   actiontime=datetime.now(),
                                   user=current_user.username,
                                   remote_addr=request.remote_addr)
        db_splitdetail.zqdm = form.zqdm.data
        db_splitdetail.broker = form.broker.data
        db_splitdetail.agentid = form.agentid.data
        db_splitdetail.lastupdate = datetime.now()
        try:
            db.session.add_all([log, db_splitdetail])
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
        return redirect(url_for('operator.splitdetail'))
    if db_splitdetail is not None:
        form.zqdm.data = db_splitdetail.zqdm
        form.broker.data = db_splitdetail.broker
        form.agentid.data = db_splitdetail.agentid
    else:
        return 'the zqdm record: %s doesn\'t exist' % req_zqdm
    return render_template('operator/splitdetail/editsplitdetail.html',form=form)

@operator.route('/delsplitdetail')
@login_required
def delsplitdetail():
    req_zqdm = request.args.get('zqdm')
    db_splitdetail = SplitDetail.query.filter_by(zqdm=req_zqdm).first()
    if db_splitdetail is not None:
        log = OperatorOperationLog(filetype='basictype',
                                   filename='splitdetail',
                                   actiontype='delete',
                                   actioncontent='delete a splitdetail:' +
                                                 ' zqdm=' + db_splitdetail.zqdm +
                                                 ' broker=' + db_splitdetail.broker +
                                                 ' agentid=' + db_splitdetail.agentid ,
                                   actiontime=datetime.now(),
                                   user=current_user.username,
                                   remote_addr=request.remote_addr)
        try:
            db.session.add(log)
            db.session.delete(db_splitdetail)
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
        return redirect(url_for('operator.splitdetail'))
    return 'the zqdm ; %s doesn\'t exist' % req_zqdm

@operator.route('/agent')
@login_required
def agent():
    page = request.args.get('page', 1, type=int)
    pagination = Agent.query.order_by(Agent.lastupdate.desc()).paginate(
        page, per_page=current_app.config['FLASKY_LOG_PER_PAGE'], error_out=False)
    agents = pagination.items
    return render_template('operator/agent/agent.html', pagination=pagination, agents=agents)

@operator.route('/addagent',methods=['GET','POST'])
@login_required
def addagent():
    form = AddAgentForm()
    if form.validate_on_submit():
            agent = Agent(agentid=form.agentid.data,
                          agentname=form.agentname.data,
                          lastupdate=datetime.now())
            log = OperatorOperationLog(filetype='basictype',
                                       filename='agent',
                                       actiontype='create',
                                       actioncontent='create a agent:'+
                                                     ' agentid='+form.agentid.data +
                                                     ' agentname='+form.agentname.data ,
                                       actiontime=datetime.now(),
                                       user=current_user.username,
                                       remote_addr=request.remote_addr)
            try:
                db.session.add_all([log,agent])
                db.session.commit()
            except Exception,e:
                db.session.rollback()
                return str(e)
            return redirect(url_for('operator.agent'))
    return render_template('operator/agent/addagent.html',form=form)

@operator.route('/editagent',methods=['GET','POST'])
@login_required
def editagent():
    form = EditAgentForm()
    req_agentid = request.args.get('agentid')
    db_agent = Agent.query.filter_by(agentid=req_agentid).first()
    if form.validate_on_submit():
        log = OperatorOperationLog(filetype='basictype',
                                   filename='agent',
                                   actiontype='update',
                                   actioncontent='update a agent,new:' +
                                                 ' agentid=' + form.agentid.data +
                                                 ' agentname=' + form.agentname.data +
                                                 ' old:'+
                                                 ' agentid='+db_agent.agentid +
                                                 ' agentname=' + db_agent.agentname ,
                                   actiontime=datetime.now(),
                                   user=current_user.username,
                                   remote_addr=request.remote_addr)
        db_agent.agentid = form.agentid.data
        db_agent.agentname = form.agentname.data
        db_agent.lastupdate = datetime.now()
        try:
            db.session.add_all([log, db_agent])
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
        return redirect(url_for('operator.agent'))
    if db_agent is not None:
        form.agentid.data = db_agent.agentid
        form.agentname.data = db_agent.agentname
    else:
        return 'the agentid record: %s doesn\'t exist' % req_agentid
    return render_template('operator/agent/editagent.html',form=form)

@operator.route('/delagent')
@login_required
def delagent():
    req_agentid = request.args.get('agentid')
    db_agent = Agent.query.filter_by(agentid=req_agentid).first()
    if db_agent is not None:
        log = OperatorOperationLog(filetype='basictype',
                                   filename='agent',
                                   actiontype='delete',
                                   actioncontent='delete a agent:' +
                                                 ' agentid=' + db_agent.agentid +
                                                 ' agentname=' + db_agent.agentname ,
                                   actiontime=datetime.now(),
                                   user=current_user.username,
                                   remote_addr=request.remote_addr)
        try:
            db.session.add(log)
            db.session.delete(db_agent)
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
        return redirect(url_for('operator.agent'))
    return 'the agentid ; %s doesn\'t exist' % req_agentid

@operator.route('/twuser')
@login_required
def twuser():
    page = request.args.get('page', 1, type=int)
    pagination = TWUser.query.order_by(TWUser.lastupdate.desc()).paginate(
        page, per_page=current_app.config['FLASKY_LOG_PER_PAGE'], error_out=False)
    twusers = pagination.items
    return render_template('operator/twuser/twuser.html', pagination=pagination, twusers=twusers)

@operator.route('/addtwuser',methods=['GET','POST'])
@login_required
def addtwuser():
    form = AddTWUserForm()
    if form.validate_on_submit():
            twuser = TWUser(clientid=form.clientid.data,
                            groupid=form.groupid.data,
                            istestuser=int(form.istestuser.data),
                            ekey=form.ekey.data,
                            password=form.password.data,
                            broker=form.broker.data,
                            lastupdate=datetime.now())
            log = OperatorOperationLog(filetype='basictype',
                                       filename='twuser',
                                       actiontype='create',
                                       actioncontent='create a twuser:'+
                                                     ' clientid='+form.clientid.data +
                                                     ' groupid='+form.groupid.data +
                                                     ' istestuser=' + form.istestuser.data +
                                                     ' ekey=' + form.ekey.data +
                                                     ' password=' + form.password.data +
                                                     ' broker=' + str(form.broker.data) ,
                                       actiontime=datetime.now(),
                                       user=current_user.username,
                                       remote_addr=request.remote_addr)
            try:
                db.session.add_all([log,twuser])
                db.session.commit()
            except Exception,e:
                db.session.rollback()
                return str(e)
            return redirect(url_for('operator.twuser'))
    return render_template('operator/twuser/addtwuser.html',form=form)

@operator.route('/edittwuser',methods=['GET','POST'])
@login_required
def edittwuser():
    form = EditTWUserForm()
    req_clientid = request.args.get('clientid')
    db_twuser = TWUser.query.filter_by(clientid=req_clientid).first()
    if form.validate_on_submit():
        log = OperatorOperationLog(filetype='basictype',
                                   filename='twuser',
                                   actiontype='update',
                                   actioncontent='update a twuser,new:' +
                                                 ' clientid=' + form.clientid.data +
                                                 ' groupid=' + form.groupid.data +
                                                 ' istestuser=' + form.istestuser.data +
                                                 ' ekey=' + form.ekey.data +
                                                 ' password=' + form.password.data +
                                                 ' broker=' + form.broker.data +
                                                 ' old:'+
                                                 ' clientid='+db_twuser.clientid +
                                                 ' groupid=' + db_twuser.groupid +
                                                 ' istestuser='+db_twuser.istestuser +
                                                 ' ekey=' + db_twuser.ekey +
                                                 ' password=' + db_twuser.password +
                                                 ' broker=' + str(db_twuser.broker) ,
                                   actiontime=datetime.now(),
                                   user=current_user.username,
                                   remote_addr=request.remote_addr)
        db_twuser.clientid = form.clientid.data
        db_twuser.groupid = form.groupid.data
        db_twuser.istestuser = int(form.istestuser.data)
        db_twuser.ekey = form.ekey.data
        db_twuser.password = form.password.data
        db_twuser.broker = form.broker.data
        db_twuser.lastupdate = datetime.now()
        try:
            db.session.add_all([log, db_twuser])
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
        return redirect(url_for('operator.twuser'))
    if db_twuser is not None:
        form.clientid.data = db_twuser.clientid
        form.groupid.data = db_twuser.groupid
        form.istestuser.data = db_twuser.istestuser
        form.ekey.data = db_twuser.ekey
        form.password.data = db_twuser.password
        form.broker.data = db_twuser.broker
    else:
        return 'the clientid record: %s doesn\'t exist' % req_clientid
    return render_template('operator/twuser/edittwuser.html',form=form)

@operator.route('/deltwuser')
@login_required
def deltwuser():
    req_clientid = request.args.get('clientid')
    db_twuser = TWUser.query.filter_by(clientid=req_clientid).first()
    if db_twuser is not None:
        log = OperatorOperationLog(filetype='basictype',
                                   filename='twuser',
                                   actiontype='delete',
                                   actioncontent='delete a twuser:' +
                                                 ' clientid=' + db_twuser.clientid +
                                                 ' groupid=' + db_twuser.groupid +
                                                 ' istestuser=' + db_twuser.istestuser +
                                                 ' ekey=' + db_twuser.ekey +
                                                 ' password=' + db_twuser.password +
                                                 ' broker=' + db_twuser.broker ,
                                   actiontime=datetime.now(),
                                   user=current_user.username,
                                   remote_addr=request.remote_addr)
        try:
            db.session.add(log)
            db.session.delete(db_twuser)
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
        return redirect(url_for('operator.agent'))
    return 'the clientid ; %s doesn\'t exist' % req_clientid

@operator.route('/operatorlog',methods=['GET','POST'])
@login_required
def operatorlog():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        filetype = form.filetype.data
        filename = form.filename.data
        actiontype = form.actiontype.data
        user = form.user.data
        ip = form.ip.data
        # print(filename,actiontype,user,ip)
        pagination = OperatorOperationLog.query.filter(
            OperatorOperationLog.filename == filename if filename else OperatorOperationLog.filename.isnot(None), \
            OperatorOperationLog.actiontype == actiontype if actiontype else OperatorOperationLog.actiontype.isnot(None), \
            OperatorOperationLog.user == user if user else OperatorOperationLog.user.isnot(None), \
            OperatorOperationLog.filetype == filetype if filetype else OperatorOperationLog.filetype.isnot(None), \
            OperatorOperationLog.remote_addr == ip if ip else OperatorOperationLog.remote_addr.isnot(None)) \
            .order_by(OperatorOperationLog.actiontime.desc()).paginate(
            page, per_page=current_app.config['FLASKY_LOG_PER_PAGE'], error_out=False)
    else:
        pagination = OperatorOperationLog.query.order_by(OperatorOperationLog.actiontime.desc()).paginate(
            page, per_page=current_app.config['FLASKY_LOG_PER_PAGE'], error_out=False)
    logs = pagination.items
    return render_template('operator/log/operatorlog.html',pagination=pagination,logs=logs,form=form)