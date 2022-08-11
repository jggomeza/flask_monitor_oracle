# Librerias de Formularios
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class FormRestartPasword(FlaskForm):
    user = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Nueva contraseña', validators=[DataRequired()])
    verify_password = PasswordField('Verificar nueva contraseña', validators=[DataRequired()])
    expire = BooleanField('Contraseña caducada (el usuario debe cambiar la contraseña en el próximo inicio de sesión).')
    locked = BooleanField('La cuenta está bloqueada')
    submit = SubmitField('Submit')