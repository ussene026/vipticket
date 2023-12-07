from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from extensions import app, bcrypt, mysql
from database import User, cursor

login = Blueprint("login", __name__)

@login.route("/login", methods=["GET", "POST"])
def login_route():
    if request.method == "POST":
        telefone = request.form["telefone"]
        password = request.form["password"]

        query = "SELECT * FROM users WHERE Telefone = %s"
        cursor.execute(query, (telefone,))
        user_data = cursor.fetchone()

        if user_data and bcrypt.check_password_hash(user_data[3], password):
            user = User()
            user.id = user_data[0]
            user.nome = user_data[1]
            user.telefone = user_data[2]
            user.password = user_data[3]

            login_user(user)
            flash("success", "Autenticado com sucesso!")
            return redirect(url_for("dashboard.dashboard_page"))
        else:
            flash("danger", "Credenciais inválidas. Tente novamente.")

    return render_template("login.html")
