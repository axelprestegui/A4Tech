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
        return render_template('usuario/registrar_usuario.html')
    
    # en otro caso, obtenemos la información enviada
    nombre_usuario = request.form['nombre_usuario']
    apellidoP = request.form['apellidoP']
    apellidoM = request.form['apellidoM']
    correo_usuario = request.form['correo_usuario']
    contrasenia = crear_contrasenia()
    telefono = request.form['telefono']
    tipo = True
    if request.form.get('type-user'):
        tipo = True
    else:
        tipo = False
    mensaje = ''
    
    try:
        usuarioRegistrado = db.session.query(Usuario).filter(Usuario.correo == request.form['correo_usuario']).one()
        flash('Este usaurio ya se encuentra registrado, por favor introduzca un correo diferente')
        return render_template('usuario/registrar_usuario.html')
    except Exception as e:
        
        nuevo_usuario = Usuario(correo_usuario,nombre_usuario,apellidoP,apellidoM,contrasenia,telefono,tipo)
    
        db.session.add(nuevo_usuario)
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
                        Nos complace que haya decidido formar parte de esta comunidad.<br>
                        Ha sido registrado exitosamente.<br>
                        Puede entrar a su cuenta usando su correo con la contraseña: {}<br>
                        Atentamente, el equipo de 4AT-ech.
                        </p>
                    </body>
                </html>
                """.format(nuevo_usuario.nombre,contrasenia)
                message['From'] = correo
                message['To'] = nuevo_usuario.correo
                message['Subject'] = 'Compra realizada en Am4zonas'
                message.attach(MIMEText(nuevo_mensaje, 'html'))
                server.sendmail(correo,nuevo_usuario.correo,message.as_string())
            except Exception as e:
                flash('No hemos podido enviar su correo con su contraseña. Sin embargo, su contraseña es: ' + contrasenia)
                # return render_template() podríamos mandarlo a la página principal o a la página del producto
        return redirect(url_for('index'))