import re
from flask import Flask, flash, request, redirect,session
# from flask.globals import session
from flask.helpers import url_for
import utils
import os
#================= Para la base de datos ============================#
import sqlite3
#================= Para cifrar las contraseñas ============================#
import hashlib
#==================== Hold the sessinon for more longer ===================
from datetime import timedelta

from werkzeug.utils import escape, redirect
from flask.templating import render_template

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=10)


@app.route('/')
def home():
    return render_template('index.html')

#== Error 404 (Muestra mensage de error si el usuario escribe 
# una url invalida o no autorizada)
@app.errorhandler(404) 
def internal_error(x):
    return render_template("redirect/404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("redirect/404.html"), 500


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # try:   
    error = None
    if request.method == 'POST':
        # register-form #
        name = request.form.get('name')
        passSignUp = request.form.get('pass-signup')
        emailSignUp = request.form.get('email-signup')

        encriptar = hashlib.sha256(passSignUp.encode('utf-8'))
        encriptado  = encriptar.hexdigest()

        if not name or not emailSignUp or not passSignUp:
            error = "Llena todos los campos."
            flash(error)
            return render_template('login.html')
        else:
            if not utils.isEmailValid(emailSignUp):
                error = "El email no es valido."
                flash(error)
                return render_template('login.html')

            if (len(passSignUp) <= 7) :
                error = "Contraseña debe ser superior a 8 carácteres"
                flash(error)
                return render_template('login.html')
            else:
                if not utils.isMyPasswordValid(passSignUp):
                    error = "Contraseña contiene caracteres invalidos."
                    flash(error)
                    return render_template('login.html')

            if len(name) <= 1:
                error = "Nombres no deben ser una letra."
                flash(error)
                return render_template('login.html')
            else:
                if not utils.isNameValid(name):
                    error = "Nombres no deben contener caracteres espaciales."
                    flash(error)
                    return render_template('login.html') 

        with sqlite3.connect('database/hotel.db') as connect: 
            # con.row_factory = sqlite3.Row
            cur = connect.cursor()
            cur.execute("INSERT INTO cliente (nombre_cliente,email_cliente,password) VALUES (?,?,?)",
            [name,emailSignUp,encriptado])
            # return 'va bien'
            connect.commit()
            return render_template("redirect/success.html")

    return render_template('login.html')
    # except:
    #     return render_template('login.html')


# ============================ LOGIN ====================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form.get('email-login')
        password = request.form.get('pass-login')

        # Comprobar si el correo es de admin que incluya @hotelmarriot.com
        if utils.isPrivateEmailValid(email) and utils.isMyPasswordValid(password):
            
            encrypt = hashlib.sha256(password.encode('utf-8'))
            encrypted = encrypt.hexdigest()

            with sqlite3.connect('database/hotel.db') as con:

                con.row_factory = sqlite3.Row
                cursor = con.cursor()
                # cursor.execute("INSERT INTO admin (nombre_admin,apellido_admin,telefono_admin,email_admin, password) VALUES (?,?,?,?,?)",
                cursor.execute("SELECT nombre_admin FROM admin WHERE email_admin=? AND password=?",
                [email,encrypted])
                # con.commit()
                row = cursor.fetchone()[0] #
                if row:
                    session.permanent = True
                    user = row
                    session['row'] = user
                    flash('Bienvenido, ','info')
                    return redirect(url_for('dashboard',name = row ))
                elif row in session:
                    #se puede crear una pagina para decir admin inabilitado
                    return redirect(url_for('dashboard',name = row))
                if not row:
                    return render_template('redirect/404.html')
        else:
            if utils.isPrivateEmailValid(email):
                error = "Correo no valido."
                flash(error)
                return render_template('login.html',
                passStatement = password,
                emailStatement = email)
            else:
                if utils.isEmailValid(email):
                    if (len(password) <= 7):
                        error = "La contraseña no debe ser menor de 8 caracteres."
                        flash(error)
                        return render_template('login.html',
                        passStatement = password,
                        emailStatement = email)
                    else:
                        if utils.isMyPasswordValid(password):
                            encrypt = hashlib.sha256(password.encode('utf-8'))
                            encrypted = encrypt.hexdigest()

                            with sqlite3.connect('database/hotel.db') as con:

                                con.row_factory = sqlite3.Row
                                cursor = con.cursor()
                                # cursor.execute("INSERT INTO admin (nombre_admin,apellido_admin,telefono_admin,email_admin, password) VALUES (?,?,?,?,?)",
                                cursor.execute("SELECT nombre_cliente FROM cliente WHERE email_cliente=? AND password=?",
                                [email,encrypted])
                                # con.commit()
                                # row = cursor.fetchone()[0]
                                row = cursor.fetchone()
                                if row is not None:
                                    row = row[0]
                                    session.permanent = True
                                    user = row
                                    session['row'] = user
                                    flash('Bienvenido, ','info')
                                    return redirect(url_for('profile',name = row ))
                                else:
                                    # mandar mensaje de cuenta no encontrada o no registrado
                                    return render_template('login.html')
                        else:
                            error = "Contraseña o correos invalidos."
                            flash(error)
                            return render_template('login.html',
                            passStatement = password,
                            emailStatement = email)           
                else:
                    error = "Correo no valido."
                    flash(error)
                    return render_template('login.html',
                    passStatement = password,
                    emailStatement = email)

            # return 'Eres user'

    return render_template('login.html')


    # Login-form #
    # if request.method == 'POST':
    #     emailLogIn = request.form['email-login']
    #     passLogIn = request.form['pass-login']

    #     # saved data #
    #     password = 'testApp1!'
    #     email = 'testemail@test.com'

    #     if not emailLogIn or not passLogIn:
    #         error = "Llena todos los campos."
    #         flash(error)
    #         return render_template('login.html')

    #     elif emailLogIn != email or passLogIn != password:
    #         print(email, password)
    #         error = "Credenciales incorrectas, intenta con estas. email: testemail@test.com contraseña: testApp1!"
    #         flash(error)
    #         return render_template('login.html')
    #     else:
    #         return redirect('/reservation')
    # return render_template('login.html')


@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    return render_template('reservation.html')



# ============ PRUEBA PARA EL DASHBOARD ================== 
@app.route('/<name>', methods=['GET','POST'])
def dashboard(name):
    if 'row' in session:
        return render_template('admin/dashboard.html',username = name)
    else:
        return render_template('redirect/404.html')

# ============ PRUEBA PARA EL PERFIL DE USUARIO ================== 
@app.route('/profile', methods=['GET','POST'])
def profile():
    # if 'row' in session:
    return render_template('users/user.html')
    # else:
    #     return render_template('redirect/404.html')

 # ===================== DESLOGUEO DEL USUARIO ==================   
@app.route("/logout")
def logout():
    session.pop('row', None)
    return redirect(url_for('home'))


# @app.route("/success", methods=["GET","POST"])
# def success():
#     return render_template("redirect/success.html")


if __name__ == "__main__":
    app.run()
 
