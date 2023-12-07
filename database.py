import mysql.connector
from flask_login import UserMixin

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="vipticket"
)
cursor = db.cursor()

class User(UserMixin):
    pass

def load_user(user_id):
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