from flask import Blueprint, redirect, url_for, flash
from flask_login import logout_user

logout = Blueprint("logout", __name__)

@logout.route("/logout")
def logout_page():
    logout_user()
    flash("success", "Sessão terminada!")
    return redirect(url_for("index"))