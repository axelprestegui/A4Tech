from flask import render_template, flash, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from models.Modelos import Producto, Usuario
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required
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
                return render_template('usuario/inicio_usuario.html')
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
                return render_template('usuario/inicio_usuario.html')
        flash("Correo o contraseña incorrectos")
        return render_template('usuario/iniciar_sesion.html', error=True)
    else :
        return render_template('usuario/iniciar_sesion.html')

@login_required
def cerrar_sesion():
    logout_user()
    return render_template('index.html')

# Función para que te mande a la página de vendedor principal.
def vendedor_principal():
    return render_template('usuario/vendedor_principal.html')

@login_required
def inicio_usuario():
    productos = db.session.query(Producto).all()
    return render_template('usuario/inicio_usuario.html', productos=productos)
    
