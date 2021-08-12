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
import re

# para enviar correos
port = 465  # For SSL
correo = '4atech.am4zonas@gmail.com' # nuestro correo
password = 'am4zonas123' # la contraseña de nuestro correo
context = ssl.create_default_context() # creamos un ssl
message = MIMEMultipart("alternative") # el correo a enviar

db = SQLAlchemy() # nuestro ORM

#Datos para hacer revisiones
#Letras Minusculas
LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k','l', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y','z']
#Letras Mayusculas
UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L','M', 'N', 'O', 'p', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
#Digitos
DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  
#symbolos        
SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',  '*', '(', ')', '<']
#Expresion regular para correo
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

"""
Funcion encargada del registro de los usuarios para el sistema
"""
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
    # Hacemos una revision de que tanto nombre y apellidos contengan unicamente letras
    if(not check_no_symbols(nombre_usuario) or not check_no_symbols(apellidoM) or not check_no_symbols(apellidoP)):
        flash('El nombre y/o apellidos no pueden llevar números o símbolos.')
        return render_template('usuario/registrar_usuario.html')
    # Revisamos que el correo tenga un formato valido
    if(not check_mail(correo_usuario)):
        flash('Correo electrónico con un formato invalido.')
        return render_template('usuario/registrar_usuario.html')
    # Revisamos que el numero sea valido
    if(not (1000000000 <= telefono and telefono <10000000000)):
        flash('El número telefónico debe tener una longitud de 10 números.')
        return render_template('usuario/registrar_usuario.html')


     # El tipo corresponde a si un usuario  es comprador o vendedor, 
     # por defecto el valor es False lo cual indica que se trata de un usuario comprador
    tipo = False
    # Si se selecciona la opcion de vendedor entonces el valor cambiara a True
    if request.form.get('type-user') == 'vendedor': tipo = True
    mensaje = ''

    # Una vez obtenemos los datos de nuestro formulario haremos la
    #  inserscion de la informacion en nuestra tabla de Usuario
    try:
        #Si el usuario ya se encuentra registrado la consulta se completara y volvera a cargar la pagina
        usuarioRegistrado = db.session.query(Usuario).filter(Usuario.correo == request.form['correo_usuario']).one()
        flash('Este usaurio ya se encuentra registrado, por favor introduzca un correo diferente')
        return render_template('usuario/registrar_usuario.html')
    except Exception as e:
        # En caso de que no ocurra entonces podemos hacer la insercion de datos
        nuevo_usuario = Usuario(correo_usuario,nombre_usuario,apellidoP,apellidoM,contrasenia,telefono,tipo)
    
        db.session.add(nuevo_usuario)
        db.session.commit()
    
        # Envíamos el correo de que se ha realizado la compra exitosamente, 
        # en este correo incluiremos la contraseña del usuario 
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
                message['Subject'] = 'Registro exitoso en Am4zonas'
                message.attach(MIMEText(nuevo_mensaje, 'html'))
                server.sendmail(correo,nuevo_usuario.correo,message.as_string())
            except Exception as e:
                flash('No hemos podido enviar su correo con su contraseña. Sin embargo, su contraseña es: ' + contrasenia)
                # Una vez enviado el correo, lo que haremos sera regresar al inicio
                # para que el usuario se pueda logear su contraseña
        return redirect(url_for('index'))

#----------------------------------Funciones auxiliares-----------------------------------------------------

#Funcion auxiliar que ayuda en la creacion de una contraseña segura
def crear_contrasenia():
    # Longitud maxima de la contraseña, puede cambiarse el tamaño en cualquier momento
    MAX_LEN = 12
    
    # Creamos los arreglos de caracteres que queremos usar
    
    # Juntamos todos los caracteres de arriba en un solo arreglo
    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
    
    # Seleccinamos por lo menos un caracter de los arreglos de arriba
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)
    
    # combinamos los caracteres que generamos
    # sin embargo solo contamos con 4, pero queremos 
    # que nuestra contraseña tenga 12 caracteres
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
    
    
    # Ahora que tenemos un arreglo con cuatro caracteres 
    # lo que haremos sera tomar los ultimos max_len -4 faltantes
    # En este caso serian 8
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)
    
        # Convertimos de manera temporal nuestra contraseña en un arreglo
        # y mezclamos con el fin de evitar asi algun patron
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)
    
    # Una vez tenemos este arreglo solo queda concatenar 
    # la lista y devolver nuestra contraseña
    contrasenia = ""
    for x in temp_pass_list:
            contrasenia = contrasenia + x

    return contrasenia

#Funcion para revisar que una cadena tenga unicamente letras y no simbolos
def check_no_symbols(campo):
    
    campo = split(campo)
    for char in campo:
            if char not in LOCASE_CHARACTERS and char not in UPCASE_CHARACTERS:
            	print(char)
            	return False
    return True

#Funcion auxiliar para convertir un string en un arreglo de chars
def split(word):
    return [char for char in word]



#funcion auxiliar para revisar que un correo electronico este bien escrito
def check_mail(email):
    
    #Revisamos que la cadena cumpla con la expresion regular
    if(re.fullmatch(regex, email)):
        return True
    return False