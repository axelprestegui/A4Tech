from flask import render_template, redirect, url_for, request, abort, jsonify, flash
from flask_login import login_required
from models.Modelos import Producto,ProductoEsquema, Compra, CompraEsquema, Usuario
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from werkzeug.utils import secure_filename
import os.path, sys, shutil, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

db = SQLAlchemy() # nuestro ORM

# para enviar correos
port = 465  # For SSL
correo = '4atech.am4zonas@gmail.com' # nuestro correo
password = 'am4zonas123' # la contraseña de nuestro correo
context = ssl.create_default_context() # creamos un ssl
message = MIMEMultipart("alternative") # el correo a enviar


def get_comprar_formulario():
    producto = db.session.query(Producto).filter(Producto.id_producto == request.form['id_producto']).one()
    return render_template('producto/comprar_producto.html', producto=producto)

"""
Método que dará acceso a '.../producto/compra_producto' la cual será una vista encargada de recabar 
la información necesaria para llevar a cabo la compra del producto.
"""
@login_required
def comprar_producto():
    correo_comprador = request.form['correo_comprador']
    correo_vendedor = request.form['correo_vendedor']
    id_producto = request.form['id_producto']
    forma_pago = request.form['forma_pago']
    cantidad = int(request.form['cantidad'])
    estado = request.form['estado']
    ciudad = request.form['ciudad']
    alcaldia = request.form['alcaldia']
    colonia = request.form['colonia']
    calle = request.form['calle']
    numero_ext = request.form['numero_ext']
    numero_int = request.form['numero_int']
    codigo_postal = request.form['codigo_postal']
    comentario = None
    numero_estrellas = None

    # obtenemos el comprador
    comprador = db.session.query(Usuario).filter_by(correo=correo_comprador).one()
    # obtenemos el producto comprado
    producto = db.session.query(Producto).filter_by(id_producto=id_producto).one()
    # checamos que haya stock suficiente

    if cantidad > producto.cantidad:
        flash('Lo sentimos, no existen tantos productos en stock. Cantidad máxima para comprar de momento: {}'.format(producto.cantidad))
        return render_template('producto/comprar_producto.html')
    # actualizamos el stock actual del producto
    producto.cantidad = producto.cantidad - cantidad
    db.session.commit()
    # obtenemos el costo total
    costo_total = cantidad * producto.precio
    # Creamos la compra
    compra = Compra(correo_comprador, correo_vendedor, id_producto, forma_pago, cantidad, costo_total, estado, ciudad,
    alcaldia,colonia,calle, numero_ext, numero_int, codigo_postal, comentario, numero_estrellas)
    # Guardamos y actualizamos en la BD
    db.session.add(compra)
    db.session.commit()

    # envíamos el correo de que se ha realizado la compra exitosamente
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("4atech.am4zonas@gmail.com", password)
        try:
            server.login(correo,password)

            nuevo_mensaje = """\
            <html>
                <body>
                    <p>¡Hola, {}!<br>
                    Agradecemos su compra en Am4zonas del producto {}.<br>
                    Su costo total ha sido de ${}.<br>
                    ¡Gracias por su preferencia!<br>
                    Atentamente, el equipo de 4AT-ech.
                    </p>
                </body>
            </html>
            """.format(comprador.nombre,producto.nombre,costo_total)
            message['From'] = correo
            message['To'] = comprador.correo
            message['Subject'] = 'Compra realizada en Am4zonas'
            message.attach(MIMEText(nuevo_mensaje, 'html'))
            server.sendmail(correo,comprador.correo,message.as_string())
        except Exception as e:
            flash('No hemos podido enviar su correo de confirmación. Sin embargo, la compra ha sido completada con éxito.')
            # return render_template() podríamos mandarlo a la página principal o a la página del producto
    return jsonify({'msg':'Compra realizada!'})