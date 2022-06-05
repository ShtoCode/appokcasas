from flask import Flask, jsonify, request
import cx_Oracle
from cryptography.fernet import Fernet

app = Flask(__name__)
key = Fernet.generate_key()

host = 'localhost'
user = 'okcasas'
password = 'okcasas'
tsname = 'xe'

try:
    conexion = cx_Oracle.connect(user, password, host+'/'+tsname)
    print('Conexion establecida!')
except Exception as e:
    print("No se pudo conectar a la base de datos. Error : " + e)


@app.get('/')
def home():
    return 'Hello World'


@app.get('/api/users')
def get_users():
    conn = conexion
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuario")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)


@app.post('/api/users')
def create_user():
    conn = conexion
    cur = conn.cursor()
    new_user = request.get_json()
    nombre = new_user['nombre']
    apellido = new_user['apellido']
    email = new_user['email']
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))
    rows = (nombre, apellido, email, password)
    statement = "SP_AGREGAR_USUARIO"
    cur.callproc(statement, rows)
    conn.commit()
    conn.close()

    return ('new_created_user')


@app.put('/api/users/1')
def update_user():
    return 'updating users'


@app.delete('/api/users/1')
def delete_user():
    return 'deleting users'

@app.get('/api/users/<id>')
def get_user():
    conn = conexion
    cur = conn.cursor()
    statement = "SP_LISTAR_USUARIOS"
    cur.execute(statement)



if __name__ == '__main__':
    app.run(debug=True)
