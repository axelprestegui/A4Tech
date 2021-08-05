from flask import render_template, redirect, url_for, request, abort, jsonify
from models.Modelos import Producto,ProductoEsquema, Compra, CompraEsquema
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from werkzeug.utils import secure_filename
import os.path
import sys
import shutil

db = SQLAlchemy() # nuestro ORM

"""
Método que dará acceso a '.../producto/compra_producto' la cual será una vista encargada de recabar 
la información necesaria para llevar a cabo la compra del producto.
"""
def evaluar_producto():
    if request.method != 'POST':
        return render_template('evaluacion/evaluacion_producto.html')
    else: 
        # Se supone que ya guarda el comentario en la BD y ahora lo posteará en la vista xd
        return render_template('evaluacion/evaluacion_producto.html')