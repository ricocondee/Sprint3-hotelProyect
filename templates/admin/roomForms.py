from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,IntegerField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, NumberRange
import sqlite3


def show_type():
    # List of data
    with sqlite3.connect('database/hotel.db') as Connect:
        cur = Connect.cursor()
        cur.execute("SELECT * FROM tipo_habitacion WHERE id_tipo > 0")
        row = cur.fetchall()
        return row

class addRoom(FlaskForm):
    h = show_type()
    num_room = IntegerField('Número de habitación',validators=[DataRequired()])
    price_room = StringField('Asignar precio',validators=[DataRequired()])
    prueba = show_type() # [(1, 'sencilla'), (2, 'doble')]
    # status_room = SelectField('Estado',coerce=int,validators=[DataRequired()])
    # choices=[("0","-Seleccione-"),("1","Active"),("2","Inactive")],validators=[DataRequired()])
    
    guardar  = SubmitField("Agregar")


# h = show_type()
# for x in h:
#     print(x)