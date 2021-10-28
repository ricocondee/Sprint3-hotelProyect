import re
from flask import Flask, flash, request, redirect, session
# from flask.globals import session
from flask.helpers import url_for
import utils
import os
#================= Para la base de datos ============================#
import sqlite3
#================= Para cifrar las contraseñas ============================#
import hashlib
# ==================== Hold the sessinon for more longer ===================
from datetime import timedelta, datetime

from werkzeug.utils import escape, redirect
from flask.templating import render_template
#  ARCHIVOS DE FORMULARIO
from templates.admin import roomForms


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=10)

@app.route('/')
def home():
    return render_template('index.html')

# == Error 404 (Muestra mensage de error si el usuario escribe
# una url invalida o no autorizada)
@app.errorhandler(404)
def internal_error(x):
    return render_template("redirect/404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("redirect/500.html"), 500


@app.errorhandler(403)
def page_forbidden(e):
    return render_template('redirect/403.html'), 403

@app.route('/signup', methods=['POST'])
def signup():
    # try:
    error = None
    if request.method == 'POST':
        # register-form #
        name = escape(request.form.get('name'))
        passSignUp = escape(request.form.get('pass-signup'))
        emailSignUp = escape(request.form.get('email-signup'))

        encriptar = hashlib.sha256(passSignUp.encode('utf-8'))
        encriptado = encriptar.hexdigest()

        if not name or not emailSignUp or not passSignUp:
            error = "Llena todos los campos."
            flash(error)
            return render_template('login.html')
        else:
            if not utils.isEmailValid(emailSignUp):
                error = "El email no es valido."
                flash(error)
                return render_template('login.html')

            if (len(passSignUp) <= 7):
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
                    error = "Nombres no deben contener caracteres especiales."
                    flash(error)
                    return render_template('login.html')

        with sqlite3.connect('database/hotel.db') as connect:
            # con.row_factory = sqlite3.Row
            cur = connect.cursor()
            cur.execute("INSERT INTO cliente (nombre_cliente,email_cliente,password) VALUES (?,?,?)",
                        [name, emailSignUp, encriptado])
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

        email = escape(request.form.get('email-login'))
        password = escape(request.form.get('pass-login'))

        # Comprobar si el correo es de admin que incluya @hotelmarriot.com
        if utils.isPrivateEmailValid(email) and utils.isMyPasswordValid(password):

            encrypt = hashlib.sha256(password.encode('utf-8'))
            encrypted = encrypt.hexdigest()

            with sqlite3.connect('database/hotel.db') as con:

                con.row_factory = sqlite3.Row
                cursor = con.cursor()
                # cursor.execute("INSERT INTO admin (nombre_admin,apellido_admin,telefono_admin,email_admin, password) VALUES (?,?,?,?,?)",
                cursor.execute("SELECT nombre_admin FROM admin WHERE email_admin=? AND password=?",
                               [email, encrypted])
                # con.commit()
                row = cursor.fetchone()[0]
                if row:
                    session.permanent = True
                    user = row
                    session['row'] = user
                    flash('Bienvenido, ', 'info')
                    return redirect(url_for('dashboard', name=row))
                elif row in session:
                    # se puede crear una pagina para decir admin inabilitado
                    return redirect(url_for('dashboard', name=row))
                if not row:
                    return render_template('redirect/404.html')
        else:
            if utils.isPrivateEmailValid(email):
                error = "Correo no valido."
                flash(error)
                return render_template('login.html',
                                       passStatement=password,
                                       emailStatement=email)
            else:
                if utils.isEmailValid(email):
                    if (len(password) <= 7):
                        error = "La contraseña no debe ser menor de 8 caracteres."
                        flash(error)
                        return render_template('login.html',
                                               passStatement=password,
                                               emailStatement=email)
                    else:
                        if utils.isMyPasswordValid(password):
                            encrypt = hashlib.sha256(password.encode('utf-8'))
                            encrypted = encrypt.hexdigest()

                            with sqlite3.connect('database/hotel.db') as con:

                                con.row_factory = sqlite3.Row
                                cursor = con.cursor()
                                # cursor.execute("INSERT INTO admin (nombre_admin,apellido_admin,telefono_admin,email_admin, password) VALUES (?,?,?,?,?)",
                                cursor.execute("SELECT nombre_cliente FROM cliente WHERE email_cliente=? AND password=?",
                                               [email, encrypted])
                                # con.commit()
                                # row = cursor.fetchone()[0]
                                row = cursor.fetchone()
                                if row is not None:
                                    client = row[0]
                                    session.permanent = True
                                    user = client
                                    session['client'] = user
                                    flash('Bienvenido, ', 'info')
                                    return redirect(url_for('profile', name=client))
                                else:  # ()
                                    # mandar mensaje de cuenta no encontrada o no registrado
                                    return render_template('login.html')
                        else:
                            error = "Contraseña o correos invalidos."
                            flash(error)
                            return render_template('login.html',
                                                   passStatement=password,
                                                   emailStatement=email)
                else:
                    error = "Correo no valido."
                    flash(error)
                    return render_template('login.html',
                                           passStatement=password,
                                           emailStatement=email)

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


def sqlConnection():  # conexion con la base de datos
    con = sqlite3.connect('database/hotel.db')
    return con


@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if 'client' in session:
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

            if not name or not lastname or not email or not confirmeEmail or not phoneNumber or not checkin or not checkout or not language or not country or not adultsQuantity:
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
                elif not adultsQuantity:
                    error = "Almenos 1 adulto"
                    flash(error)
                    return returned()

                elif policies == None:
                    error = "Debe aceptar los terminos y condiciones."
                    flash(error)
                    return returned()

                elif not petition:
                    petition = "Sin peticiones especiales."

                if not kidsQuantity:
                    kidsQuantity = 0

            fechaReserva = datetime.now().strftime('%d-%m-%Y | %H:%M:%S')
            con = sqlConnection()
            cur = con.cursor()
            sqlrt = 'INSERT INTO reserva (nombre, apellido, fecha_inicio, fecha_fin, adultos, menores, email, telefono, idioma, pais, peticiones, fecha_solicitud) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'# query consult
            cur.execute(sqlrt, [name, lastname,  checkin, checkout, adultsQuantity, kidsQuantity, email, phoneNumber, language, country, petition, fechaReserva])  # execute query
            con.commit()  # Guarda los cambios
    else:
        error = "Debes loguearte primero"
        flash(error)
        return redirect(url_for('login'))

    return render_template('reservation.html')


# ============ PRUEBA PARA EL DASHBOARD ==================
@app.route('/<name>', methods=['GET', 'POST'])
def dashboard(name):
    if 'row' in session:
        return render_template('admin/dashboard.html', username=name)
    else:
        return render_template('redirect/403.html')

# ======================= Formularios =============================
@app.route('/rooms', methods=['GET','POST']) 
def addRooms():
    form = roomForms.addRoom()

    with sqlite3.connect('database/hotel.db') as Connect:
        # Para que me devuelva la lisca como un diccionari de datos
        Connect.row_factory = sqlite3.Row
        lCursor = Connect.cursor()
        #  Prepara la sentencia SQL
        lCursor.execute("SELECT numero_habitacion, tipo, precio FROM habitacion INNER JOIN tipo_habitacion ON id_tipo = tipo_habitacion_fk")
        rows = lCursor.fetchall()

        # return render_template("listar-usuario.html", var_rows = rows)

    
    if 'row' in session:
        if request.method == 'POST':
            number = form.num_room.data
            # dropDown = form.prueba[0]
            dropDown = request.form.get('tipo')
            price = form.price_room.data
            # stts = form.status_room.data
            
            # return dropDown
            if not number or not dropDown or not price:
                error = 'Los campos deben ser completados'
                flash(error)
                return render_template('admin/create.html', frm=form, prueba = dropDown,var_rows = rows) 
            else:
                if number >= 1: 
                    with sqlite3.connect('database/hotel.db') as connect: 
                        cur = connect.cursor()
                        cur.execute("SELECT * FROM habitacion WHERE numero_habitacion=?",[number])
                        
                        if cur.fetchone():
                            error = 'Numero de habitación ya existe'
                            flash(error)
                            return render_template('admin/create.html',
                            frm=form,
                            prueba = dropDown,
                            var_rows = rows) 

                    if dropDown:
                        if len(price) >= 2:
                            with sqlite3.connect('database/hotel.db') as connect: 
                            # con.row_factory = sqlite3.Row
                                cur = connect.cursor()
                                cur.execute("INSERT INTO habitacion (numero_habitacion,tipo_habitacion_fk,precio) VALUES (?,?,?)",
                                [number,dropDown,price])
                                # return 'va bien'
                                connect.commit()
                                exito = 'Formulario registrado con exito'
                                flash(exito)
                                return render_template('admin/create.html',
                                frm=form,
                                prueba = dropDown,
                                var_rows = rows)      
                        else:
                            error = 'Dato no valido'
                            flash(error)
                            return render_template('admin/create.html',
                            frm=form,
                            prueba = dropDown,
                            var_rows = rows) 
                else:
                    error = 'Debe ser mayor a uno'
                    flash(error)
                    return render_template('admin/create.html', frm=form, prueba = dropDown) 
            if form.validate_on_submit():
                return render_template('admin/create.html', frm=form, prueba = dropDown) 
    else:
        error = "Ingresa como administrador."
        flash(error)
        return redirect(url_for('login'))
    return render_template('admin/create.html',frm=form, var_rows = rows)

# ============ PRUEBA PARA EL PERFIL DE USUARIO ================== 
@app.route('/profile/<name>', methods=['GET','POST'])
def profile(name):
    if 'client' in session:
        message = "Vuelve al home para reservar."
        flash(message)
        return render_template('users/user.html', username=name)
    else:
        return render_template('redirect/403.html')

 # ===================== DESLOGUEO DEL USUARIO ==================


@app.route("/logout")
def logout():
    if 'client' in session:
        session.pop('client', None)
        return redirect(url_for('home'))
    if 'row' in session:
        session.pop('row', None)
        return redirect(url_for('home'))


# @app.route("/success", methods=["GET","POST"])
# def success():
#     return render_template("redirect/success.html")


if __name__ == "__main__":
    app.run(debug=True)
