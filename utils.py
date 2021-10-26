import re
from validate_email import validate_email

name_regex = "^[a-zA-Z]+$"

pass_regex = "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"

user_regex = "^[a-zA-Z0-9_.-]+$"

phone_regex = "^(\d{3}[\s*.-]?\d{3}[\s*.-]?\d{4})$"

mail_regex  = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-_]+\.?[a-zA-Z]+$"

private_mail_regex  = "^([a-zA-Z]+@hotelmarriot\.com)$"

F_ACTIVE = 'ACTIVE'
F_INACTIVE = 'INACTIVE'
EMAIL_APP = 'EMAIL_APP'
REQ_ACTIVATE = 'REQ_ACTIVATE'
REQ_FORGOT = 'REQ_FORGOT'
U_UNCONFIRMED = 'UNCONFIRMED'
U_CONFIRMED = 'CONFIRMED'


def isEmailValid(email):
    is_valid = validate_email(email)

    return is_valid

def isUsernameValid(user):
    if re.search(user_regex, user):
        return True
    else:
        return False

def isPasswordValid(password):
    if re.search(pass_regex, password):
        return True
    else:
        return False


def isMyPasswordValid(password):
    if re.search(r"^[a-z]{6,30}$", password): # Just letters in lowercase
        return True
    elif re.search(r"^[A-Z]{6,30}$", password): # Just in uppercase
        return True
    elif re.search(r"^[\d]{6,30}$", password): # Just numbers
        return True
    elif re.search(r"^[@$!%*#?&]{6,30}$", password): # Mix of characters
        return True
    elif re.search(r"^[A-Za-z\d@$!#%*?&]{6,30}$", password): # All possibles combinations
        return True
    else:
        return False



# Esta función permite la validacion de correos asignados a los 
# administradores que unicamente cumplan con '...@hotelmarriot.com'
def isPrivateEmailValid(private):
    if re.search(private_mail_regex, private):
        return True
    else:
        return False

# Esta funcion permite la validacion de numeros telefonicos que contengan
# la caracteristica: 3 digitos, 3digitos, 4 digitos que estén separados
# por espacios, guión o punto
def isMyPhoneNumber(phone):
    if re.match(phone_regex, phone):
        return True
    else:
        return False