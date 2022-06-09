from flask import Flask, jsonify, redirect, render_template, request, flash, session, url_for
import cx_Oracle
from cryptography.fernet import Fernet
from werkzeug.security import check_password_hash, generate_password_hash


import functools

app = Flask(__name__)
key = Fernet.generate_key()

#Conexion bd
def connection():
    host = 'localhost'
    port = 1521
    user = 'okcasas'
    password = 'okcasas'
    sid = 'xe' #Cambiar segun sid de oracle (xe - orcl)
    d = cx_Oracle.makedsn(host, port, sid=sid)
 
    conn = cx_Oracle.connect(
    user=user,
    password=password,
    dsn=d,
    encoding="UTF-8")
    return conn
 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email-login']
        password = request.form['password']
        conn = connection()
        cur = conn.cursor()
        error = None
        cur.execute("SELECT * FROM usuario WHERE email = (:1)", [email])
        usuario = cur.fetchone()
        print(usuario)
        if usuario is None:
            error = "Usuario y/o contraseña incorrecta."
        elif not check_password_hash(usuario['password'], password):
            error = "Usuario y/o contraseña incorrecta."
        
        if error is None:
            session.clear()
            session['user_id'] = usuario['id_usuario']
            return redirect(url_for('/'))

        return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/registrar')
def registrar():
    return render_template('registrarU.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')



@app.get('/api/users')
def get_users():
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuario")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)


@app.post('/api/users')
def create_user():
    conn = connection()
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
    conn = connection()
    cur = conn.cursor()
    statement = "SP_LISTAR_USUARIOS"
    cur.execute(statement)



if __name__ == '__main__':
    app.run(debug=True)
