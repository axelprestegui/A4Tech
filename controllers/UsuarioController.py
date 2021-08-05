from flask import render_template, flash, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from models.Modelos import Usuario
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

db = SQLAlchemy() # nuestro ORM

def iniciar_sesion():
    if request.method == 'POST':
        if current_user.is_authenticated:
            print('holi')
            return render_template('index.html') # falta poner a dónde mandarlo dependiendo del tipo de usuario
        correo = request.form.get('correo')
        contrasenia = request.form.get('contrasenia')
        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario is not None and usuario.check_contrasenia(contrasenia):
            login_user(usuario)
            return render_template('index.html') # Esto lo cambiamos por la página principal del comprador o vendedor
        flash("Correo o contraseña incorrectos")
        return render_template('usuario/iniciar_sesion.html', error=True)
    else :
        return render_template('usuario/iniciar_sesion.html')

def cerrar_sesion():
    logout_user()
    return render_template('index.html')
