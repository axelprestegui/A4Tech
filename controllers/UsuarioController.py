from flask import render_template
from flask import flash
from flask import request
from models.Modelos import Vendedor
from models.Modelos import Comprador
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

db = SQLAlchemy() # nuestro ORM

def iniciar_sesion():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasenia = request.form.get('contrasenia')
        usuario = Comprador.query.filter_by(correo=correo).first()

        if not usuario or not check_password_hash(usuario.contrasenia, contrasenia):
            flash("Usuario o contraseña incorrectos")
            return render_template('usuario/iniciar_sesion.html', error=True)

        return render_template('/') # Esto lo cambiamos por la página principal del comprador
    else :
        return render_template('usuario/iniciar_sesion.html')

def cerrar_sesion():
    if request.method == 'POST':
        pass
    else :
        return render_template('usuario/cerrar_sesion.html')
