from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import mysql.connector

app = Flask(__name__)
app.secret_key = 'djfljdfljfnkjsfhjfshjkfjfjfhjdhfdjhdfu'
bcrypt = Bcrypt(app)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="vipticket"
)
cursor = db.cursor()

def telefone_existente(telefone):
    query = "SELECT COUNT(*) FROM users WHERE Telefone = %s"
    cursor.execute(query, (telefone,))
    result = cursor.fetchone()
    return result[0] > 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
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
def dashboard():
    return render_template("dashboard.html")

if __name__ == '__main__':
    app.run(debug=True)
