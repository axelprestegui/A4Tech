from flask import render_template
from flask import flash
from flask import request
from flask import url_for
from werkzeug.utils import redirect
from models.Modelos import Vendedor
from models.Modelos import Comprador
from flask_sqlalchemy import SQLAlchemy
import sys

db = SQLAlchemy()

def iniciar_sesion():
    if request.method != 'POST':
        return render_template('usuario/iniciar_sesion.html')
        
    correo = request.form['correo']
    contrasenia = request.form['contrasenia']
    tipo_de_usuario = request.form.get('type-user')
    
    if tipo_de_usuario == 'comprador':
        usuario = db.session.query(Comprador).filter_by(correo=correo).first()
    else:
        usuario = db.session.query(Vendedor).filter_by(correo=correo).first()

    contrasenia_usuario = usuario.contrasenia.replace(" ","")
    contrasenia_ingresada = contrasenia.replace(" ","")

    if not usuario or contrasenia_usuario != contrasenia_ingresada:
        flash("Usuario o contraseña incorrectos")
        return render_template('usuario/iniciar_sesion.html', error=True)

    # Esto lo cambiamos por la página principal del comprador
    return redirect(url_for('producto.crear_producto'))

def cerrar_sesion():
    print("Hola, hola", file=sys.stderr)
    db.session.close()
    return redirect(url_for('index'))
