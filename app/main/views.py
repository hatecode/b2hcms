#encoding:utf-8

from flask import render_template,redirect,url_for,request,make_response,jsonify,current_app
from flask_login import login_required
from .forms import *
from . import main
from ..models import *
from sqlalchemy import and_,or_

@main.route('/')
@main.route('/index')
@login_required
def index():
    #users = User.query.order_by(User.id).all()
    #return render_template('index.html',users=users)
    return render_template('index/index.html')

@main.route('/top')
@login_required
def top():
    return render_template('index/_top.html')

@main.route('/left')
@login_required
def left():
    baseconfigids = Dbfsync.query.first().dbfsynccontent.split(',')
    return render_template('index/_left.html',baseconfigids=baseconfigids)

@main.route('/right')
@login_required
def right():
    return render_template('index/_right.html')

@main.route('/footer')
@login_required
def footer():
    return render_template('index/_footer.html')

@main.route('/baseconfig')
@login_required
def baseconfig():
    page = request.args.get('page', 1, type=int)
    pagination = BaseConfig.query.order_by(BaseConfig.lastupdate.desc()).paginate(
        page, per_page=current_app.config['FLASKY_LOG_PER_PAGE'], error_out=False)
    baseconfigs = pagination.items
    return render_template('baseconfig/baseconfig.html', pagination=pagination, baseconfigs=baseconfigs)

@main.route('/baseconfig/<baseconfigid>',methods=['GET','POST'])
@login_required
def baseconfigids(baseconfigid):
    form = EditBaseConfigForm()
    db_baseconfig = BaseConfig.query.filter_by(baseconfigid=baseconfigid).first()
    if db_baseconfig:
        if form.validate_on_submit():
            log = OperatorOperationLog( filetype='基础配置',
                                        filename='baseconfig',
                                        actiontype='update',
                                        actioncontent='update baseconfig, old : ' +
                                                     ' baseconfigname = ' + db_baseconfig.baseconfigname +
                                                     ' baseconfigcontent = ' + db_baseconfig.baseconfigcontent +
                                                     ' new : ' + 'baseconfigname = ' + form.baseconfigname.data +
                                                     ' baseconfigcontent = ' + form.baseconfigcontent.data,
                                        actiontime=datetime.now(),
                                        user=current_user.username,
                                        remote_addr=request.remote_addr)
            db_baseconfig.baseconfigname = form.baseconfigname.data
            db_baseconfig.baseconfigcontent = form.baseconfigcontent.data
            try:
                db.session.add_all([log,db_baseconfig])
                db.session.commit()
            except Exception,e:
                db.session.rollback()
                return str(e )
            return redirect(url_for('main.right'))

        form.baseconfigid.data = db_baseconfig.baseconfigid
        form.baseconfigname.data = db_baseconfig.baseconfigname
        form.baseconfigcontent.data = db_baseconfig.baseconfigcontent
        return render_template('baseconfig/editconfig.html',form=form)
    else:
        return 'the baseconfigid %r doesn\'n exist, please check' % baseconfigid

@main.route('/addconfig',methods=['GET','POST'])
@login_required
def addconfig():
    form = AddBaseConfigForm()
    if form.validate_on_submit():
        req_baseconfigid = form.baseconfigid.data
        baseconfigid = BaseConfig.query.filter_by(baseconfigid=req_baseconfigid).first()
        if baseconfigid is None:
            baseconfig = BaseConfig(baseconfigid=form.baseconfigid.data,
                                    baseconfigname=form.baseconfigname.data,
                                    baseconfigcontent=form.baseconfigcontent.data,
                                    lastupdate=datetime.now())
            log = OperationLog(filename='baseconfig',
                               actiontype='create',
                               actioncontent='create a baseconfig:'+' id='+form.baseconfigid.data+
                                            ' name='+form.baseconfigname.data+
                                            ' content='+form.baseconfigcontent.data,
                               actiontime=datetime.now(),
                               user=current_user.username,
                               remote_addr=request.remote_addr)
            try:
                db.session.add_all([log,baseconfig])
                #db.session.add(baseconfig)
                db.session.commit()
            except Exception,e:
                db.session.rollback()
                return str(e)
            return redirect(url_for('main.baseconfig'))
        else:
            return 'the %s exitst, try another' % req_baseconfigid
    return render_template('baseconfig/addconfig.html',form=form)

@main.route('/editconfig',methods=['GET','POST'])
@login_required
def editconfig():
    form = EditBaseConfigForm()
    req_baseconfigid = request.args.get('baseconfigid')
    db_baseconfig = BaseConfig.query.filter_by(baseconfigid=req_baseconfigid).first()
    if form.validate_on_submit():
        log = OperationLog(filename='baseconfig',
                           actiontype='update',
                           actioncontent='update a baseconfig,new:' +
                                         ' name=' + form.baseconfigname.data +
                                         ' content=' + form.baseconfigcontent.data +
                                        ' old: '+'name='+db_baseconfig.baseconfigname+
                                        ' content='+db_baseconfig.baseconfigcontent,
                           actiontime=datetime.now(),
                           user=current_user.username,
                           remote_addr=request.remote_addr)
        db_baseconfig.baseconfigname = form.baseconfigname.data
        db_baseconfig.baseconfigcontent = form.baseconfigcontent.data
        db_baseconfig.lastupdate = datetime.now()
        try:
            db.session.add_all([log, db_baseconfig])
            #db.session.add(db_baseconfig)
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
        return redirect(url_for('main.baseconfig'))
    if db_baseconfig is not None:
        form.baseconfigid.data = db_baseconfig.baseconfigid
        form.baseconfigname.data = db_baseconfig.baseconfigname
        form.baseconfigcontent.data = db_baseconfig.baseconfigcontent
    else:
        return 'the req_baseconfigid record: %s does\'nt exist' % req_baseconfigid
    return render_template('baseconfig/editconfig.html',form=form)

@main.route('/delconfig')
@login_required
def delconfig():
    req_baseconfigid = request.args.get('baseconfigid')
    db_baseconfig = BaseConfig.query.filter_by(baseconfigid=req_baseconfigid).first()
    if db_baseconfig is not None:
        log = OperationLog(filename='baseconfig',
                           actiontype='delete',
                           actioncontent='delete a baseconfig:' +
                                         ' id=' + db_baseconfig.baseconfigid +
                                         ' name=' + db_baseconfig.baseconfigname +
                                         ' content=' + db_baseconfig.baseconfigcontent ,
                           actiontime=datetime.now(),
                           user=current_user.username,
                           remote_addr=request.remote_addr)
        try:
            db.session.add(log)
            db.session.delete(db_baseconfig)
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
        return redirect(url_for('main.baseconfig'))
    return 'the baseconfigid ; %s doesn\'t exist' % req_baseconfigid

@main.route('/sysusers')
@login_required
def sysusers():
    users = User.query.order_by(User.id).all()
    return render_template('admin/sysusers.html',users=users)

@main.route('/dbfsync',methods=['GET','POST'])
@login_required
def dbfsync():
    form = DbfsyncForm()
    db_dbfsync = Dbfsync.query.first()
    if form.validate_on_submit():
        log = OperationLog(filename='dbfsync',
                           actiontype='update',
                           actioncontent=' update dbfsync:' +
                                         ' old: id=' + db_dbfsync.dbfsyncid +
                                         ' content=' + db_dbfsync.dbfsynccontent +
                                         ' new: id=' + form.id.data +
                                         ' content=' + form.content.data ,
                           actiontime=datetime.now(),
                           user=current_user.username,
                           remote_addr=request.remote_addr)

        raw_data_list = form.content.data.split(',')
        #print 'data_list: %r' % raw_data_list
        data_list = [data.strip() for data in raw_data_list if data.strip()]
        #print('data_list: ',data_list)

        db_baseconfigs = BaseConfig.query.all()
        db_baseconfigids = [db_baseconfig.baseconfigid for db_baseconfig in db_baseconfigs]
        #print db_baseconfigids
        #print(set(db_baseconfigids) >= set(data_list))

        if set(db_baseconfigids) >= set(data_list):
            db_dbfsync.dbfsynccontent = ','.join(data_list)
            try:
                db.session.add(log)
                db.session.add(db_dbfsync)
                db.session.commit()
            except Exception,e:
                db.session.rollback()
                return str(e)
            return '添加成功'.decode('utf-8')
        else:
            return '您添加的内容不在基础配置文件的ID中，请检查后添加'.decode('utf-8')

    if db_dbfsync:
        form.id.data = db_dbfsync.dbfsyncid
        form.content.data = db_dbfsync.dbfsynccontent
    else:
        try:
            db.session.add(Dbfsync(dbfsyncid='syncid'))
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
    return render_template('admin/dbfsync.html',form=form)

@main.route('/oprationlog',methods=['GET','POST'])
@login_required
def oprationlog():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        filename = form.filename.data
        actiontype = form.actiontype.data
        user = form.user.data
        ip = form.ip.data
        #print(filename,actiontype,user,ip)
        pagination = OperationLog.query.filter(OperationLog.filename==filename if filename else OperationLog.filename.isnot(None),\
                                               OperationLog.actiontype==actiontype if actiontype else OperationLog.actiontype.isnot(None),\
                                               OperationLog.user==user if user else OperationLog.user.isnot(None),\
                                               OperationLog.remote_addr==ip if ip else OperationLog.remote_addr.isnot(None))\
                                               .order_by(OperationLog.actiontime.desc()).paginate(
                                               page, per_page=current_app.config['FLASKY_LOG_PER_PAGE'],error_out=False)
    else:
        pagination = OperationLog.query.order_by(OperationLog.actiontime.desc()).paginate(
            page, per_page=current_app.config['FLASKY_LOG_PER_PAGE'],error_out=False)
    logs = pagination.items
    return render_template('admin/oprationlog.html',pagination=pagination,logs=logs,form=form)