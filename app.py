from flask import Flask, render_template, flash, request, redirect
import utils
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def home():
    return render_template('index.html')


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
    # Login-form #
    if request.method == 'POST':
        emailLogIn = request.form['email-login']
        passLogIn = request.form['pass-login']

        # saved data #
        password = 'testApp1!'
        email = 'testemail@test.com'

        if not emailLogIn or not passLogIn:
            error = "Llena todos los campos."
            flash(error)
            return render_template('login.html')

        elif emailLogIn != email or passLogIn != password:
            print(email, password)
            error = "Credenciales incorrectas, intenta con estas. email: testemail@test.com contraseña: testApp1!"
            flash(error)
            return render_template('login.html')
        else:
            return redirect('/reservation')
    return render_template('login.html')


@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    return render_template('reservation.html')