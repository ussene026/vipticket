from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user, current_user
import mysql.connector

app = Flask(__name__)
app.secret_key = 'djfljdfljfnkjsfhjfshjkfjfjfhjdhfdjhdfu'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="vipticket"
)
cursor = db.cursor()

class User(UserMixin):
    pass

def telefone_existente(telefone):
    query = "SELECT COUNT(*) FROM users WHERE Telefone = %s"
    cursor.execute(query, (telefone,))
    result = cursor.fetchone()
    return result[0] > 0

@login_manager.user_loader
def load_user(user_id):
    # Função para carregar usuário pelo ID
    query = "SELECT * FROM users WHERE ID = %s"
    cursor.execute(query, (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        user = User()
        user.id = user_data[0]
        user.nome = user_data[1]
        user.telefone = user_data[2]
        user.password = user_data[3]
        return user
    return None

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("danger", "Ocorreu um erro. Faça login para continuar.")
    return redirect(url_for("login"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
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
            return redirect(url_for("dashboard"))
        else:
            flash("danger", "Credenciais inválidas. Tente novamente.")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        password = request.form["password"]

        if telefone_existente(telefone):
            flash("danger", "Desculpe, o telefone selecionado não está disponível. Escolha outro número e tente novamente.")
            return redirect(url_for("register"))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        query = "INSERT INTO users (Nome, Telefone, Password) VALUES (%s, %s, %s)"
        values = (nome, telefone, hashed_password)
        cursor.execute(query, values)
        db.commit()

        flash("success", "Conta criada com sucesso! Faça login para continuar.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("success", "Sessão terminada!")
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
