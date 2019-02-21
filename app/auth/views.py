#encoding:utf-8

from flask import render_template,redirect,flash,url_for,request
from flask_login import current_user,login_user,logout_user,login_required

from . import auth
from .forms import *
from .. import db
from ..models import User

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user,form.remember_me.data)
            flash('login in success')
            return redirect(url_for('main.index'))
        else:
            #flash('invalid username or password')
            return 'invalid username or password'
    return render_template('auth/login.html',form=form)

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is  None:
            new_user = User(username=form.username.data,
                            password=form.password_second.data,
                            email=form.email.data,
                            landline=form.landline.data,
                            cellphone=form.cellphone.data,
                            department=form.department.data)
            try:
                db.session.add(new_user)
                db.session.commit()
                #flash('register in success')
            except Exception,e:
                db.session.rollback()
                return str(e)
            return redirect(url_for('auth.login'))
        else:
            #flash('the username has been registered,please use another one')
            return 'the username has been registered,please use another one'

    '''
    tips = '***选填项***'.decode('utf-8')
    form.email.data= tips
    form.landline.data = tips
    form.cellphone.data = tips
    form.department.data = tips
    '''
    return render_template('auth/registration.html',form=form)

@auth.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    #flash('logout in success')
    return redirect(url_for('auth.login'))

@auth.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.landline = form.landline.data
        current_user.cellphone = form.cellphone.data
        current_user.department = form.department.data
        try:
            db.session.add(current_user)
            db.session.commit()
            #flash('eidt profile in success')
        except Exception,e:
            db.session.rollback()
            return str(e)
        return redirect(url_for('main.right'))
    form.department.data = current_user.department
    form.email.data = current_user.email
    form.cellphone.data = current_user.cellphone
    form.landline.data = current_user.landline
    return render_template('auth/edit_profile.html',form=form)

@auth.route('/change_password',methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if current_user.check_password(str(form.old_password.data)):
        current_user.password = form.new_password_first.data
        try:
            db.session.add(current_user)
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
        #flash('change password in success')
    else:
        #flash('invalid old password')
        return 'invalid old password'
    return render_template('auth/change_password.html',form=form)

@auth.route('/adduser',methods=['GET','POST'])
@login_required
def adduser():
    form = AddUserForm()
    if form.validate_on_submit():
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None:
                new_user = User(username=form.username.data,
                                password=form.password_second.data,
                                email=form.email.data,
                                landline=form.landline.data,
                                cellphone=form.cellphone.data,
                                department=form.department.data)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    #flash('adduser in success')
                except Exception,e:
                    db.session.rollback()
                    return str(e)
                return redirect(url_for('main.sysusers'))
            else:
                #flash('the username has been registered,please use another one')
                return 'the username has been registered,please use another one'
    return render_template('auth/adduser.html',form=form)

@auth.route('/deluser',methods=['GET','POST'])
@login_required
def deluser():
    username = request.args.get("username")
    user = User.query.filter_by(username=username).first()
    if user.is_admin:
        #flash('can not delete the admin')
        return redirect(url_for('main.sysusers'))
    elif user:
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception,e:
            db.session.rollback()
            return str(e)
    else:
        #flash('user not eixst')
        return render_template('404.html')
    return redirect(url_for('main.sysusers'))