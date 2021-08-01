from flask import render_template, redirect, url_for, request, abort, jsonify
from models.Modelos import Producto,ProductoEsquema
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from werkzeug.utils import secure_filename
import os.path
import shutil

db = SQLAlchemy() # nuestro ORM

def iniciar_sesion():
    if request.method == 'POST':
        print("Hola")
    else :
        return render_template('usuario/iniciar_sesion.html')

def cerrar_sesion():
    pass
