#encoding:utf-8

from flask import render_template,redirect
from . import auth

@auth.route('/login',methods=['GET','POST'])
def login():