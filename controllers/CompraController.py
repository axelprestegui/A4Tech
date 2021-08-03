from flask import render_template, redirect, url_for, request, abort, jsonify
from models.Modelos import Producto,ProductoEsquema, Compra, CompraEsquema
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from werkzeug.utils import secure_filename
import os.path
import sys
import shutil

db = SQLAlchemy() # nuestro ORM

imagenes_validas = [".jpg",".gif",".png",".jpeg"] # las formatos de imágenes que permitimos

"""
Método que dará acceso a '.../producto/compra_producto' la cual será una vista encargada de recabar 
la información necesaria para llevar a cabo la compra del producto.
"""
def comprar_producto():
    # Si no recibimos un post, mostramos el formulario.
    if request.method != 'POST':
        return render_template('producto/comprar_producto.html')
    else:
        correo_comprador = request.form['correo_comprador']
        correo_vendedor = request.form['correo_vendedor']
        id_producto = request.form['id_producto']
        forma_pago = request.form['forma_pago']
        cantidad = request.form['cantidad']
        costo_total = request.form['costo_total']
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

        # Creamos la compra
        compra = Compra(correo_comprador, correo_vendedor, id_producto, forma_pago, cantidad, costo_total, estado, ciudad,
        alcaldia,colonia,calle, numero_ext, numero_int, codigo_postal, comentario, numero_estrellas)
        # Guardamos en la BD
        db.session.add(compra)
        db.session.commit()

