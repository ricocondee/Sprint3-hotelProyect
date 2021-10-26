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

from werkzeug.utils import redirect
from flask.templating import render_template

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/')
def home():
    return render_template('index.html')

#== Error 404 (Muestra mensage de error si el usuario escribe 
# una url invalida o no autorizada)
@app.errorhandler(404) 
def internal_error(x):
    return render_template("redirect/404.html"), 404


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        
        error = None
        if request.method == 'POST':
            # register-form #
            name = request.form['name']
            passSignUp = request.form['pass-signup']
            emailSignUp = request.form['email-signup']

            if not name or not emailSignUp or not passSignUp:
                error = "Llena todos los campos."
                flash(error)
                return render_template('login.html')

            if not utils.isEmailValid(emailSignUp):
                error = "El email no es valido."
                flash(error)
                return render_template('login.html')

            if not utils.isPasswordValid(passSignUp):
                error = "Minimo 8 caracteres, usa mayusculas, minusculas y caracteres especiales."
                flash(error)
                return render_template('login.html')

        return render_template('login.html')
    except:
        return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email-login')
        password = request.form.get('pass-login')

        # Comprobar si el correo es de admin primero @hotelmarriot.com
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
                    # session['name']  = name
                    return redirect(url_for('dashboard',name = row))
                elif row in session:
                    #se puede crear una pagina para decir admin inabilitado
                    return redirect(url_for('dashboard',name = row))
                else:
                    return render_template('redirect/404.html')
        else:
            return 'Eres user'

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
# 1: 

@app.route('/<name>', methods=['GET','POST'])
def dashboard(name):
    if 'row' in session:
        return render_template('admin/dashboard.html')
    else:
        return render_template('redirect/404.html')
    


if __name__ == "__main__":
    app.run()
 
