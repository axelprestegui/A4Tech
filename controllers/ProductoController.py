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
    return redirect(url_for('.productos_vendedor'))


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

            nueva_imagen = Imagen(str(correo_vendedor),str(id_producto), '../../static/images/'+str(correo_vendedor)+'/'+str(id_producto)+'/'+ imagen.filename )
            try:
                db.session.add(nueva_imagen)
                db.session.commit()
            except:
                jsonify('Algo salio mal')

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

def get_actualizar_formulario():
    producto = db.session.query(Producto).filter(Producto.id_producto == request.form['id_producto']).one()
    return render_template('producto/actualizar_producto.html', producto=producto)

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
    return redirect(url_for('producto.productos_vendedor')) # aquí debería ir algo del estilo render_template('ruta/mostrar_producto.html')

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
    
    return redirect(url_for('.productos_vendedor'))

def get_producto(nombre):
    producto = db.session.query(Producto).filter(Producto.nombre.like('%'+nombre+'%')).all()
    return producto

@login_required
def buscar_producto():
    if request.method != 'POST':
        return render_template('usuario/inicio_usuario.html')

    producto = get_producto(request.form['search'])

    if producto == []:
        flash("No se encontró ningún producto con esas características")
        return render_template('usuario/inicio_usuario.html')
    else:
        return render_template('usuario/resultado_busqueda.html')

@login_required
def resultado_busqueda():
    return render_template('producto/resultado_busqueda.html', resultados=get_producto(request.form['search']))

@login_required
def ver_articulo_buscado():
    return render_template('producto/ver_articulo_buscado.html', producto=get_producto(request.form['search']))

@login_required
def ver_articulo_comprador():
    # obtenemos información del producto
    id_producto = request.form['id_producto']
    # y del comprador que está observando el producto
    try:
        correo_comprador = request.form['correo_comprador']
        # si se mandó una reseña del producto, la intentamos guardar
        guarda_resenia(request.form['resenia'], correo_comprador, id_producto)
    except:
        pass
    #Se hace la busqueda del producto deseado
    producto = db.session.query(Producto).filter(Producto.id_producto == id_producto).one()
    imagen = db.session.query(Imagen).filter(Imagen.id_producto == id_producto).first()
    # y de los compras para obtener las reseñas y calificación
    (compras,promedio_estrellas) = get_compras_con_reseña(id_producto)
    return render_template('producto/ver_articulo_comprador.html', producto = producto, compras = compras, promedio_estrellas=promedio_estrellas, imagen = imagen)

def ver_articulo_vendedor():
    # obtenemos información del producto
    id_producto = request.form['id_producto']
    #Se hace la busqueda del producto deseado
    producto = db.session.query(Producto).filter(Producto.id_producto == id_producto).one()
    # y de los compras para obtener las reseñas y calificación
    (compras,promedio_estrellas) = get_compras_con_reseña(id_producto)
    imagen = db.session.query(Imagen).filter(Imagen.id_producto == id_producto).first()
    return render_template('producto/ver_articulo_vendedor.html', producto = producto, compras = compras, promedio_estrellas=promedio_estrellas, url_img = imagen)

def get_compras_con_reseña(id_producto):
    compras = db.session.query(Compra, Usuario).join(Usuario, Compra.correo_comprador == Usuario.correo)\
                                                .filter(Compra.id_producto == id_producto).all()
    compras_con_opinion = list(filter(lambda compra: compra.Compra.comentario != None, compras))
    promedio_estrellas = 0
    if len(compras_con_opinion) != 0:
        promedio_estrellas = reduce(lambda acc, compra: compra.Compra.numero_estrellas + acc
                                                        if compra.Compra.numero_estrellas != None
                                                        else acc, compras, 0)/len(compras_con_opinion)
    return (compras_con_opinion,promedio_estrellas)

# Función auxiliar para guardar reseñas
def guarda_resenia(comentario, correo_comprador, id_producto):
    # buscamos todas las posibles compras que haya hecho el vendedor del producto
    compras = db.session.query(Compra).filter_by(correo_comprador=correo_comprador,id_producto=id_producto).all()
    for compra in compras:
        # las iteramos para buscar alguna que no contenga comentario
        if not compra.comentario:
            # en tal caso, agregamos la reseña y terminamos
            compra.comentario = comentario
            db.session.commit()
            return
    flash('Por favor, compre el producto')

def mostrar_todos():
    producto = db.session.query(Producto).order_by(Producto.nombre).limit(10)
    if request.method != 'POST':
        
        #enviamos
        return render_template('producto/mostrar_todos.html', producto = producto) 

@login_required
def productos_vendedor():
    id_vendedor = current_user.correo
    # si se usa  natural join, aquellos productos sin imagen no apareceran,
    # creo que además esto tendrá problemas cuando un producto tenga más de una imagnes
    # productos = db.engine.execute("SELECT * FROM producto NATURAL JOIN imagen WHERE correo_vendedor = '"+str(id_vendedor)+"'")
    # dejo por lo mientras esta que sí nos deja ver productos aunque no tengan imagen
    productos = db.session.query(Producto).filter(Producto.correo_vendedor == Usuario.correo, Usuario.correo == id_vendedor , Usuario.tipo == True)
    return render_template('producto/productos_vendedor.html', producto = productos)
    