from logging import log
from flask import render_template, redirect, url_for, request, abort, jsonify
from flask_login import login_required, current_user
from flask.helpers import flash
from sqlalchemy.orm import query
from models.Modelos import *
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from functools import reduce
from werkzeug.utils import secure_filename
import os.path, sys, shutil

db = SQLAlchemy() # nuestro ORM

imagenes_validas = [".jpg",".gif",".png",".jpeg"] # las formatos de imágenes que permitimos


@login_required
def crear_producto():
    """
    Método que se ejecuta al entrar a la direccion "/producto/crea_producto", encargado
    de, ya sea devolver el formulario para la creacion de una nueva publicación de producto
    o de recibir la información que se haya mandado para intentar la creación de una nueva
    publicación de producto.
    """

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
    id_producto = producto_nuevo.id_producto
    producto = db.session.query(Producto).filter(Producto.id_producto == id_producto).one()
    #Una vez cargado el producto cargamos la imagen de este
    imagen = db.session.query(Imagen).filter(Imagen.id_producto == id_producto).first()
    return render_template('producto/ver_articulo_vendedor.html', producto = producto, compras = [], promedio_estrellas=0.0, url_img = imagen)

@login_required
def actualizar_producto():
    """
    Método que se ejecuta al entrar a la direccion "/producto/actualizar_producto", encargado
    de, ya sea devolver el formulario para la recabación de los nuevos datos o de recibir la
    información mandada por el usuario para la actualización del producto.
    """
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
        elimina_imagenes(imagenes, correo, id_producto)
        # subimos nuevas imágenes
        guarda_imagenes(imagenes, correo, id_producto)


    # hacemos commit para guardar los cambios
    db.session.commit()
    return redirect(url_for('producto.productos_vendedor')) # aquí debería ir algo del estilo render_template('ruta/mostrar_producto.html')

@login_required
def eliminar_producto():
    """
    Método que se ejecuta al entrar a la direccion "/producto/eliminar_producto", encargado
    de, ya sea devolver el formulario para la confirmación de la eliminación del producto o
    de recibir eliminar el producto.
    """
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
    
    return redirect(url_for('.productos_vendedor'))

###---------------------------------- MÉTODOS AUXILIARES ----------------------------------###

# Método auxiliar para guardar las imágenes de los productos. Se recibe las imágenes, el correo
# del vendedor para saber la dirección donde guardar las imágenes, y el id del producto
# para poder obtenerlas cuando sea necesario.
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
            imagen_name = secure_filename(imagen.filename.replace(' ',''))
            imagen.save(os.path.join(dir_vendedor_img, str(id_producto), imagen_name))
            
            """
        Una vez guardamos las imagenes indicamos en la tabla de Imagen la ruta, el id del producto y el correo del vendedor
        En este caso todas las imagenes se guardaran en ../../static/images/<correo>/<id_producto>
            """ 
            nueva_imagen = Imagen(str(correo_vendedor),str(id_producto), '../../static/images/'+str(correo_vendedor)+'/'+str(id_producto)+'/'+ imagen_name )
            try:
                db.session.query(Imagen).filter_by(id_producto=id_producto).delete()
                db.session.add(nueva_imagen)
                db.session.commit()
            except:
                pass

# Método auxiliar que elimina todas las imágenes asociadas a un producto.
def elimina_imagenes(imagenes, correo_vendedor, id_producto):
    # checamos que sí debemos eliminar imagenes
    for imagen in imagenes:
        # si lo que nos mandaron no es de tipo imagen
        if '.' + imagen.content_type.split('/')[1] not in imagenes_validas:
            return
    # creamos dirección donde deben estar guardadas las imágenes del vendedor
    dir_vendedor_img = str(Path(__file__).parent.parent / ('static/images/' + correo_vendedor))
    # checamos si el directorio existe, en otro caso, no existen fotos
    if os.path.isdir(os.path.join(dir_vendedor_img, str(id_producto))):
        # eliminamos el directorio donde están guardadas las fotos
        shutil.rmtree(os.path.join(dir_vendedor_img, str(id_producto)))

# Método auxiliar para obtener el formulario de actualización de un producto específico.
def get_actualizar_formulario():
    producto = db.session.query(Producto).filter(Producto.id_producto == request.form['id_producto']).one()
    return render_template('producto/actualizar_producto.html', producto=producto)
