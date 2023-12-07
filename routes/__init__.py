from flask import Blueprint

index = Blueprint("index", __name__)
login = Blueprint("login", __name__)
dashboard = Blueprint("dashboard", __name__)
logout = Blueprint("logout", __name__)

from . import index, login, dashboard, logout
