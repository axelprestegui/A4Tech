from flask import render_template, redirect, url_for, request, abort, jsonify
from flask_login import login_required
from flask.helpers import flash
from sqlalchemy.orm import query
from models.Modelos import Producto,ProductoEsquema, Usuario
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from werkzeug.utils import secure_filename
import os.path, sys, shutil

db = SQLAlchemy() # nuestro ORM

imagenes_validas = [".jpg",".gif",".png",".jpeg"] # las formatos de imágenes que permitimos


"""
Método que es llamado al entrar a ".../producto/crea_producto" será ejecutado, encargado
de ya sea devolver el formulario para la creacion de una nueva publicación de producto
o de recibir la información que se haya mandado para intentar la creación de una nueva
publicación de producto
"""
@login_required
def crear_producto():
    # si no recibimos una solicitud post, mostramos el formulario
    if request.method != 'POST':
        return render_template('producto/crear_producto.html')
    
    # en otro caso, obtenemos la información enviada
    correo_vendedor = request.form['correo_vendedor']
    nombre = request.form['nombre']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    detalles = request.form['detalles']
    descripcion = request.form['descripcion']
    estado = True
    imagenes = request.files.getlist("imagenes")
    try:
        request.form['estado']
    except:
        estado = False
    
    # creamos nuestro producto
    producto_nuevo = Producto(correo_vendedor, nombre, precio, cantidad, detalles, descripcion, estado)
    # guardamos nuestro producto en la bd
    db.session.add(producto_nuevo)
    db.session.commit()
    
    # si recibimos imágenes, las guardamos
    if imagenes != []:
        guarda_imagenes(imagenes, correo_vendedor, producto_nuevo.id_producto)
    
    # cuando la vista de mostrar producto esté terminada, aquí debería ir render_template('ruta/mostrar_producto.html')
    return jsonify({'msg':'producto registrado!'})


"""
Función auxiliar para guardar las imágenes de los productos. Se recibe las imágenes, el correo
del vendedor para saber la dirección donde guardar las imágenes, y el id del producto
para poder obtenerlas cuando sea necesario.
"""
def guarda_imagenes(imagenes, correo_vendedor, id_producto):
    # creamos dirección donde deben estar guardadas las imágenes del vendedor
    dir_vendedor_img = str(Path(__file__).parent.parent / ('static/images/' + correo_vendedor))
    # checamos si dicho directorio ya existe, en otro caso, lo creamos
    if not os.path.isdir(dir_vendedor_img):
        os.mkdir(dir_vendedor_img)
    #c hecamos si el directorio del prodcuto ya existe, en otro caso, lo creamos
    if not os.path.isdir(os.path.join(dir_vendedor_img, str(id_producto))):
        os.mkdir(os.path.join(dir_vendedor_img, str(id_producto)))
    # para cada imagen, la guardamos en el directorio del producto
    for imagen in imagenes:
        # si la imagen es del tipo permitido, la agregamos
        if '.' + imagen.content_type.split('/')[1] in imagenes_validas:
            imagen_name = secure_filename(imagen.filename)
            imagen.save(os.path.join(dir_vendedor_img, str(id_producto), imagen_name.strip()))

"""
Función auxiliar que elimina todas las imágenes asociadas a un producto.
"""
def elimina_imagenes(correo_vendedor, id_producto):
    # creamos dirección donde deben estar guardadas las imágenes del vendedor
    dir_vendedor_img = str(Path(__file__).parent.parent / ('static/images/' + correo_vendedor))
    # checamos si el directorio existe, en otro caso, no existen fotos
    if os.path.isdir(os.path.join(dir_vendedor_img, str(id_producto))):
        # eliminamos el directorio donde están guardadas las fotos
        shutil.rmtree(os.path.join(dir_vendedor_img, str(id_producto)))

"""
Método que se encarga de actualizar un producto de la bd.
"""
def actualizar_producto():
    # si no recibimos una solicitud post, mostramos el formulario
    if request.method != 'POST':
        return render_template('producto/actualizar_producto.html')
    # en otro caso, obtenemos la información enviada
    campos = ['correo_vendedor',
                'id_producto',
                'nombre',
                'precio',
                'cantidad',
                'detalles',
                'descripcion']
    data = []
    # añadimos a data todos los campos modificados
    for campo in campos:
        nueva_info = request.form[campo]
        if nueva_info != '':
            data.append((campo,nueva_info))
    try:
        request.form['estado']
        data.append(('estado',True))
    except:
        data.append(('estado',False))
   
    # obtenemos nuestro producto a modificar de la bd
    producto = db.session.query(Producto).filter(Producto.id_producto == request.form['id_producto']).one()
    # para cada campo modificado mandado, lo modificamos en nuestro producto
    for (campo,nueva_info) in data:
        setattr(producto, campo, nueva_info)
    
    # revisamos si recibimos imágenes nuevas, y en tal caso actualizamos
    imagenes = request.files.getlist("imagenes")
    if imagenes != []:
        correo = request.form['correo_vendedor']
        id_producto = request.form['id_producto']
        # eliminamos las fotos viejas, si es que había
        elimina_imagenes(correo, id_producto)
        # subimos nuevas imágenes
        guarda_imagenes(imagenes, correo, id_producto)


    # hacemos commit para guardar los cambios
    db.session.commit()
    return jsonify({'msg': 'todo ok'}) # aquí debería ir algo del estilo render_template('ruta/mostrar_producto.html')

"""
Método que se encarga de eliminar un producto de la bd.
"""
@login_required
def eliminar_producto():
    if request.method != 'POST':
        return render_template('producto/eliminar_producto.html')
    
    id_producto = request.form['id_producto']
    # obtenemos el producto
    producto = db.session.query(Producto).filter_by(id_producto=id_producto).one()
    # eliminamos sus imágenes si es que existen
    dir_vendedor_img = str(Path(__file__).parent.parent / ('static/images/' + producto.correo_vendedor))
    imagenes = os.path.join(dir_vendedor_img, str(id_producto))
    if os.path.isdir(imagenes):
        shutil.rmtree(imagenes)
    # eliminamos al producto
    db.session.query(Producto).filter_by(id_producto=id_producto).delete()
    db.session.commit()
    
    return jsonify({'msg': 'todo ok'})

@login_required
def buscar_producto():
    if request.method != 'POST':
        return render_template('producto/buscar_producto.html')

    busqueda = db.session.query(Producto).filter(Producto.nombre.like('%'+request.form['search']+'%')).all()

    if busqueda == []:
        return render_template('producto/buscar_producto.html')
    else:
        return render_template('producto/resultado_busqueda.html') # aquí llamamos a la función que nos devuelve la lista de productos

@login_required
def resultado_busqueda():
    return render_template('producto/resultado_busqueda.html')

def ver_articulo():
    #Esta parte debe modificarse para poder cargar un producto en especifico
    id_producto = '4'

    #Se hace la busqueda del producto deseado
    producto = db.session.query(Producto).filter(Producto.id_producto == id_producto).one()
    if request.method != 'POST':
        
        #enviamos
        return render_template('producto/ver_articulo.html', producto = producto)
    return jsonify('Algo')

def mostrar_todos():
    producto = db.session.query(Producto).order_by(Producto.nombre).limit(10)
    if request.method != 'POST':
        
        #enviamos
        return render_template('producto/mostrar_todos.html', producto = producto) 

def productos_vendedor():
    id_vendedor = 'axelprestegui@ciencias.unam.mx'
    productos = db.session.query(Producto).filter(Producto.correo_vendedor == Usuario.correo, Usuario.correo == id_vendedor , Usuario.tipo == True)
    return render_template('producto/productos_vendedor.html', producto = productos)
    