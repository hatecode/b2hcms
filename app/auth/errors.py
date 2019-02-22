from flask import render_template
from . import auth

@auth.app_errorhandler(403)
def forbidden(e):
    render_template('error/403.html'),403

@auth.app_errorhandler(404)
def page_not_found(e):
    render_template('error/404.html'),404

@auth.app_errorhandler(500)
def internal_server_error(e):
    render_template('error/500.html'),500