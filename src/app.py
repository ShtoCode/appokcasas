import functools
from flask import Flask, jsonify, redirect, render_template, request, flash, session, url_for
import cx_Oracle
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash

import cgi


#Models
from models import ModelUsuario
from models.entities import Usuario



app = Flask(__name__)
key = Fernet.generate_key()
app.secret_key = "secret_key"


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

@app.route('/registrar', methods = ['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        conn = connection()
        cur = conn.cursor()
        new_user = request.get_json()
        nombre = new_user['nombre']
        apellido = new_user['apellido']
        email = new_user['email']
        password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))
        error = None
        cur.execute("SELECT id_usuario FROM usuario WHERE email = (:1)", [email])
        if not nombre:
            error = "Nombre es requerido"
        
        if not apellido:
            error = "Apellido es requerido"
        
        if not email:
            error = "Email es requerido"
        
        if not password:
            error = "Password es requerido"

        elif cur.fetchone() is not None:
            error = "Usuario {} se encuentra registrado.".format(email)

        if error is None:
            rows = (nombre, apellido, email, password)
            statement = "SP_AGREGAR_USUARIO"
            cur.callproc(statement, rows)
            conn.commit()
            conn.close()
            return redirect('login')

        cur.close()

        flash(error)       

    return render_template('registrarU.html')

@app.route('/servicios', methods=['GET', 'POST'])
def servicios():
    if request.method == 'POST':
        conn = connection()
        new_servicio = request.get_json()
        instalacionesVal = new_servicio['instalacionesVal']
        metrosVal = new_servicio['metrosVal']
        luzVal = new_servicio['luzVal']
        termografiaVal = new_servicio['termografiaVal']
        instalaciones = None
        metros = None
        luz = None
        termografia = None
        valorInstalaciones = None
        valorMetros = None
        valorLuz = None
        valorTermografia = None


        #Comprobar si checkbox está seleccionado
        if instalacionesVal == True:
            instalaciones = new_servicio['lblInstalaciones']
            valorInstalaciones = new_servicio['valorInstalaciones']
            cur = conn.cursor()
            rows = (instalaciones, valorInstalaciones)
            statement = "SP_AGREGAR_SERVICIO"
            cur.callproc(statement, rows)
            print("Servicio guardado")
            conn.commit()
            conn.close()

        if metrosVal == True:
            metros = new_servicio['lblMetros']
            valorMetros = new_servicio['valorMetros']
            cur = conn.cursor()
            rows = (metros, valorMetros)
            statement = "SP_AGREGAR_SERVICIO"
            cur.callproc(statement, rows)
            print("Servicio guardado")
            conn.commit()
            conn.close()
 
#        if luzVal == True:        
#            luz = new_servicio['lblLuz']

#        if luzVal == True:        
#            termografia = new_servicio['lblTermografia']


#        termografia = new_servicio['lblTermografia']
#        valorInstalaciones = new_servicio['valorInstalaciones']
#        valorMetros = new_servicio['valorMetros']
#        valorLuz = new_servicio['valorLuz']
#        valorTermografia = new_servicio['valorTermografia']

        return render_template('servicios.html')

    print('nofunco')


    return render_template('servicios.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
     
    if request.method == 'POST':
        email = request.form['email-login']
        password = request.form['password'] 
        conn = connection()
        c = conn.cursor()
        c.execute("SELECT * FROM usuario WHERE email = (:1)", [email])
        u = c.fetchone()
        if u is None:
            flash('Usuario y/o contraseña invalida')

        print(u[0])
        
        user = Usuario.Usuario(id_usario=0, nombre="", apellido="", email=email, password=password)
        logged_user = ModelUsuario.ModelUsuario.login(con=conn, usuario=user) 
        
        if logged_user != None:
            if logged_user.password:
                return redirect('/')
            else:
                flash('Usuario y/o contraseña invalida')
        else:
            flash('Usuario No encontrado')

    else:
        return render_template('login.html')






if __name__ == '__main__':
    app.run(debug=True)
