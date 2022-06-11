import functools
from re import X
from flask import Flask, jsonify, redirect, render_template, request, flash, session, url_for, g
import cx_Oracle
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash





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
        password = new_user['password']
        password_hash = generate_password_hash(password)
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
            return redirect('registrar')

        if error is None:
            rows = (nombre, apellido, email, password_hash)
            statement = "SP_AGREGAR_USUARIO"
            cur.callproc(statement, rows)
            conn.commit()
            conn.close()
            return redirect('login')
        cur.close()
        conn.close()

        print(error)       

        return redirect('registrar')        
        
    return render_template('registrarU.html')




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
        if usuario is None:
            error = "Usuario y/o contraseña incorrecta1."
        if not check_password_hash(usuario[4], password):
            error = "Usuario y/o contraseña incorrecta2."

        if error is None:
            session.clear()
            print("HELLO")
            session['id_usuario'] = usuario[0]
            session['nombre'] = usuario[1]
            session['apellido'] = usuario[2]
            session['email'] = usuario[3]
            return redirect('/')


#        error = None
#        if usuario is not None:
#            if password == usuario[4]:
#                session['id_usuario'] = usuario[0]
#                session['nombre'] = usuario[1]
#                session['apellido'] = usuario[2]
#                session['email'] = usuario[3]
#                login_user(usuario)
#                return redirect('/')
#            else:
#                error = "Correo y/o contraseña invalida"
#                print("error aqui")
#        else:
#            error = "Correo y/o contraseña invalida"
#            print("Error en otro aqui")
        
        print(error)
        flash(error)
        return render_template('login.html')
        


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.usuario = None
    else:
        conn = connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario WHERE id_usuario = (:0)", [user_id])
        g.usuario = cur.fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.usuario is None:
            return redirect('login')

        return view(**kwargs)     

    return wrapped_view


@app.route('/servicios', methods=['GET', 'POST'])
@login_required
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
 
        if luzVal == True:        
            luz = new_servicio['lblLuz']
            valorLuz = new_servicio['valorLuz']
            print(luz, valorLuz)

            cur = conn.cursor()
            rows = (luz, valorLuz)
            statement = "SP_AGREGAR_SERVICIO"
            cur.callproc(statement, rows)
            print("Servicio guardado")
            conn.commit()
            conn.close()


        if termografiaVal == True:        
            termografia = new_servicio['lblTermografia']
            valorTermografia = new_servicio['valorTermografia']
            cur = conn.cursor()
            rows = (termografia, valorTermografia)
            statement = "SP_AGREGAR_SERVICIO"
            cur.callproc(statement, rows)
            print("Servicio guardado")
            conn.commit()
            conn.close()


        return render_template('servicios.html')
        
        


    return render_template('servicios.html')

@app.route('/seguimiento')
def seguimiento():
    return render_template("seguimiento.html")



if __name__ == '__main__':
    app.run(debug=True)
