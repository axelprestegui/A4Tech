from flask import render_template, flash, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from models.Modelos import Usuario
from flask_sqlalchemy import SQLAlchemy
import sys

db = SQLAlchemy()

def iniciar_sesion():
    if request.method == 'POST':
        # checamos si ya hay un usuario en sesión
        if current_user.is_authenticated:
            # si es vendedor lo redireccionamos a la página correspondiente
            if current_user.tipo:
                return render_template('usuario/vendedor_principal.html')
            else:
                return render_template('index.html') # aquí va la página del comprador
        # en otro caso, intentamos iniciar sesión
        correo = request.form.get('correo')
        contrasenia = request.form.get('contrasenia')
        usuario = Usuario.query.filter_by(correo=correo).first()

        # checamos si encontramos un usuario y las contraseñas coinciden
        if usuario is not None and usuario.check_contrasenia(contrasenia):
            login_user(usuario)
            # si es vendedor lo redireccionamos a la página correspondiente
            if usuario.tipo:
                return render_template('usuario/vendedor_principal.html')
            else:
                return render_template('index.html') # aquí va la página del comprador
        flash("Correo o contraseña incorrectos")
        return render_template('usuario/iniciar_sesion.html', error=True)
    else :
        return render_template('usuario/iniciar_sesion.html')

def cerrar_sesion():
    logout_user()
    return render_template('index.html')
