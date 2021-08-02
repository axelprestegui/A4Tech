from flask import render_template, redirect, url_for, request, abort, jsonify
from models.Modelos import Producto,ProductoEsquema
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
    if request.method != 'POST':
        return render_template('producto/comprar_producto.html')
