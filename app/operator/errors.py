from flask import render_template
from . import operator

@operator.app_errorhandler(403)
def forbidden(e):
    render_template('403.html'),403

@operator.app_errorhandler(404)
def page_not_found(e):
    render_template('404.html'),404

@operator.app_errorhandler(500)
def internal_server_error(e):
    render_template('500.html'),500