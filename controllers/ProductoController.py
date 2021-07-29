import sys
from flask import render_template, redirect, url_for, request, abort, jsonify
from models.Modelos import Producto,ProductoEsquema
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # nuestro ORM

"""
Método que es llamado al entrar a ".../producto/crea_producto" será ejecutado, encargado
de ya sea devolver el formulario para la creacion de una nueva publicación de producto
o de recibir la información que se haya mandado para intentar la creación de una nueva
publicación de producto
"""
def crear_producto():
    #si recibimos una solicitud post
    if request.method == 'POST':
        correo_vendedor = request.form['correo_vendedor']
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        detalles = request.form['detalles']
        descripcion = request.form['descripcion']
        estado = True
        try:
            request.form['estado']
        except:
            estado = False
        #imagenes
        
        producto_nuevo = Producto(correo_vendedor, nombre, precio, cantidad, detalles, descripcion, estado)

        db.session.add(producto_nuevo)
        db.session.commit()
        return jsonify({'msg':'producto registrado!'}) #cuando la vista de mostrar producto esté terminada, aquí debería ir render_template('ruta/mostrar_producto.html')
    # en otro caso, aún no recibimos solicitus, por lo que mostramos formulario
    return render_template('producto/crear_producto.html')

def actualizar_producto():
    data = request.get_json()
    correo_vendedor = data['correo_vendedor']
    nombre = data['nombre']
    precio = data['precio']
    cantidad = data['cantidad']
    detalles = data['detalles']
    descripcion = data['descripcion']
    estado = data['estado']

    
def eliminar_producto():
    ...