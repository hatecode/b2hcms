from flask import Blueprint

operator = Blueprint('operator',__name__)

from . import views,errors