from flask import Flask, flash, request, render_template, session
import sqlite3

from flask.helpers import url_for
import utils
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key = os.urandom(64)


def sqlConnection():
    conexion = sqlite3.connect('JWDATABASE.db')
    return conexion


@app.route('/')
def home():
    return render_template('index.html')

# == Error 404 (Muestra mensage de error si el usuario escribe
# una url invalida o no autorizada)


@app.errorhandler(404)
def internal_error(x):
    return render_template("redirect/404.html"), 404


@app.route('/signup', methods=['POST'])
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

            hashWord = generate_password_hash(passSignUp)
            conexion = sqlConnection()
            cur = conexion.cursor()
            sqlrt = 'INSERT INTO registerdata (nombre, email, password) VALUES(?,?,?)'
            cur.execute(sqlrt, [name, emailSignUp, hashWord])
            conexion.commit()
            menssage = "Ya puedes logearte."
            flash(menssage)

        return render_template('login.html')
    except:
        return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    # Login-form #
    if request.method == 'POST':
        emailLogIn = request.form['email-login']
        passLogIn = request.form['pass-login']

        conexion = sqlConnection()
        cur = conexion.cursor()
        sqlrt = 'SELECT * FROM registerdata WHERE email = ?'
        cur.execute(sqlrt, [emailLogIn])
        cur = cur.fetchone()

        if not emailLogIn or not passLogIn:
            error = "Llena todos los campos."
            flash(error)
            return render_template('login.html')
        elif cur is None:
            error = "Email incorrecto."
            flash(error)

        elif check_password_hash(cur[3], passLogIn):
            session.clear()
            session['email'] = cur[2]
            if 'email' in session:
                return redirect(url_for('reservation'))
        else:
            error = "Contraseña incorrecta"
            flash(error)
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        confirmeEmail = request.form['confirm-email']
        phoneNumber = request.form['phone-number']
        checkin = request.form['check-in']
        checkout = request.form['check-out']
        language = request.form['list-languages']
        country = request.form['list-countries']
        adultsQuantity = request.form['number-of-adults']
        kidsQuantity = request.form['number-of-kids']
        petition = request.form['petitions']
        policies = request.form.get('policies')

        def returned():
            return render_template('reservation.html',
                                   nameStatement=name,
                                   lastnameStatement=lastname,
                                   emailStatement=email,
                                   confirmeEmailStatement=confirmeEmail,
                                   phoneStatement=phoneNumber,
                                   checkinStatement=checkin,
                                   checkoutStatement=checkout,
                                   languageStatement=language,
                                   countryStatement=country,
                                   adultsQuantityStatement=adultsQuantity,
                                   kidsQuantityStatement=kidsQuantity,
                                   petitionStatement=petition)

        if not name or not lastname or not email or not confirmeEmail or not phoneNumber or not checkin or not checkout or not language or not country or not adultsQuantity or not kidsQuantity:
            error = 'Los campos marcados con (*) son obligatorios.'
            flash(error)
            return returned()
        else:
            if not utils.isEmailValid(email):
                error = "El email no es valido."
                flash(error)
                return returned()
            elif email != confirmeEmail:
                error = "El email no coincide."
                flash(error)
                return returned()
            elif not kidsQuantity or not adultsQuantity:
                error = "Almenos 1 adulto, si no hay niños coloque 0."
                flash(error)
                return returned()
            elif policies == None:
                error = "Debe aceptar los terminos y condiciones."
                flash(error)
                return returned()
            elif not petition:
                petition = "Sin peticiones especiales."

        conexion = sqlConnection()
        cur = conexion.cursor()
        sqlrt = 'INSERT INTO reserva (nombres, apellidos, check_in, check_out, adultos, menores, email, telefono, idioma, pais, peticiones) VALUES (?,?,?,?,?,?,?,?,?,?,?);'
        cur.execute(sqlrt, [name, lastname, checkin, checkout, adultsQuantity, kidsQuantity, email, phoneNumber, language, country, petition])
        conexion.commit()
        return render_template('redirect/success.html')
    return render_template('reservation.html')


if __name__ == "__main__":
    app.run(debug=True)
