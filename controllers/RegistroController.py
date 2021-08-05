from os import error
from flask import Flask, flash
from flask import render_template, redirect, url_for, request, abort, jsonify
from models.Modelos import *
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from werkzeug.utils import secure_filename
import os.path
import sys
import shutil
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import random
import array

# para enviar correos
port = 465  # For SSL
correo = '4atech.am4zonas@gmail.com' # nuestro correo
password = 'am4zonas123' # la contraseña de nuestro correo
context = ssl.create_default_context() # creamos un ssl
message = MIMEMultipart("alternative") # el correo a enviar

db = SQLAlchemy() # nuestro ORM

"""
Funcion encargada del registro de los usuarios para el sistema
"""

def crear_contrasenia():
    # maximum length of password needed
    # this can be changed to suit your password length
    MAX_LEN = 12
    
    # declare arrays of the character that we need in out password
    # Represented as chars to enable easy string concatenation
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']
    
    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 
                        'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']
    
    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', 
            '*', '(', ')', '<']
    
    # combines all the character arrays above to form one array
    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
    
    # randomly select at least one character from each character set above
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)
    
    # combine the character randomly selected above
    # at this stage, the password contains only 4 characters but 
    # we want a 12-character password
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
    
    
    # now that we are sure we have at least one character from each
    # set of characters, we fill the rest of
    # the password length by selecting randomly from the combined 
    # list of character above.
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)
    
        # convert temporary password into array and shuffle to 
        # prevent it from having a consistent pattern
        # where the beginning of the password is predictable
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)
    
    # traverse the temporary password array and append the chars
    # to form the password
    contrasenia = ""
    for x in temp_pass_list:
            contrasenia = contrasenia + x

    return contrasenia

def registrar_usuario():
    # si no recibimos una solicitud post, mostramos el formulario
    if request.method != 'POST':
        return render_template('producto/registrar_usuario.html')
    
    # en otro caso, obtenemos la información enviada
    nombre_usuario = request.form['nombre_usuario']
    apellidoP = request.form['apellidoP']
    apellidoM = request.form['apellidoM']
    correo_usuario = request.form['correo_usuario']
    contrasenia = crear_contrasenia()
    telefono = request.form['telefono']
    isComprador = request.form.get("comprador")
    isVendedor = request.form.get("vendedor")
    mensaje = None
    
    try:
        usuarioRegistrado = db.session.query(Usuario).filter(Usuario.correo == request.form['correo_usuario']).one()
        return jsonify('Usuario ya registrado como vendedor')
    except:
        flash('Este usaurio ya se encuentra registrado, por favor introduzca un correo diferente')
        
    
    if (isComprador == 'comprador') and (isVendedor == 'vendedor') or isComprador == isVendedor:
        return error
    elif isComprador == 'comprador':
        
        mensaje = 'Registrado el comprador :' 
        nuevo_usuario = Usuario(correo_usuario,nombre_usuario,apellidoP, apellidoM,contrasenia,telefono, True)
        mensaje += str(nombre_usuario) + ' ' + str (apellidoP)
    else:
        mensaje = 'Registrado el vendedor :'
        nuevo_usuario = Usuario(correo_usuario,nombre_usuario,apellidoP,apellidoM,contrasenia,telefono, False)
        mensaje += str(nombre_usuario) + ' ' + str (apellidoP)
    
    
    db.session.add(nuevo_usuario)
    db.session.commit()
    

    mensaje += ' su contrasenia es: '+ str(contrasenia)            
    return jsonify(mensaje)
