from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,IntegerField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, NumberRange


class addRoom(FlaskForm):
    
    num_room = IntegerField('Número de habitación',validators=[DataRequired()])
    type_room = SelectField('Tipo de habitación',coerce=int,validators=[DataRequired()])
    price_room = StringField('Asignar precio',validators=[DataRequired()])
    # status_room = SelectField('Estado',coerce=int,
    # choices=[("0","-Seleccione-"),("1","Active"),("2","Inactive")],validators=[DataRequired()])
    
    guardar  = SubmitField("Agregar")