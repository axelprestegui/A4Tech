from flask import render_template, request
from flask_login import login_required, current_user
from flask.helpers import flash
from sqlalchemy.orm import query
from models.Modelos import *
from flask_sqlalchemy import SQLAlchemy
from functools import reduce
import os.path, sys, shutil

db = SQLAlchemy() # nuestro ORM

'''
Función que se ejecuta al momento de presionar el botón de búsqueda. Se encarga
de buscar los productos que coincidan con el nombre ingresado por el usuario.
'''
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

# Redirecciona a la página con los resultados de la búsqueda.
@login_required
def resultado_busqueda():
    return render_template('producto/resultado_busqueda.html', resultados=get_producto(request.form['search']))

'''
Redirecciona a la página para ver el producto seleccionado de la lista de los 
resultados obtenidos. 
'''
@login_required
def ver_articulo_buscado():
    return render_template('producto/ver_articulo_buscado.html', producto=get_producto(request.form['search']))


# Muestra un artículo si es que el usuario es un comprador.
@login_required
def ver_articulo_comprador():
    # obtenemos información del producto
    id_producto = request.form['id_producto']
    # y del comprador que está observando el producto
    try:
        correo_comprador = request.form['correo_comprador']
        # si se mandó una reseña del producto, la intentamos guardar
        guarda_resenia(request.form['resenia'], request.form['numero_estrellas'], correo_comprador, id_producto)
    except Exception as e:
        pass
    #Se hace la busqueda del producto deseado
    producto = db.session.query(Producto).filter(Producto.id_producto == id_producto).one()
    #Una vez cargado el producto, cargamos sus imagenes
    imagen = db.session.query(Imagen).filter(Imagen.id_producto == id_producto).first()
    # y de los compras para obtener las reseñas y calificación
    (compras,promedio_estrellas) = get_compras_con_reseña(id_producto)
    return render_template('producto/ver_articulo_comprador.html', producto = producto, compras = compras, promedio_estrellas=promedio_estrellas, imagen = imagen)

# Muestra un artículo si es que el usuario es un vendedor.
@login_required
def ver_articulo_vendedor():
    # obtenemos información del producto
    id_producto = request.form['id_producto']
    #Se hace la busqueda del producto deseado
    producto = db.session.query(Producto).filter(Producto.id_producto == id_producto).one()
    # y de los compras para obtener las reseñas y calificación
    (compras,promedio_estrellas) = get_compras_con_reseña(id_producto)
    #Una vez cargado el producto cargamos la imagen de este
    imagen = db.session.query(Imagen).filter(Imagen.id_producto == id_producto).first()
    return render_template('producto/ver_articulo_vendedor.html', producto = producto, compras = compras, promedio_estrellas=promedio_estrellas, url_img = imagen)

#Funcion que nos ayuda a cargar todos los productos que pertenezcan a un vendedor
@login_required
def productos_vendedor():
    #Obtenemos el ID del vendedor que haya iniciado sesion
    id_vendedor = current_user.correo
    """
    Realizamos la busqueda en la base de datos, para ello tomaemos la tabla Producto e Imagen
    y haremos una union por la izquierda, esto con el proposito de que si un producto no posee
    una imagen aun asi pueda desplegarlo
    """
    productos = db.engine.execute("""SELECT producto.correo_vendedor as correo_vendedor, producto.id_producto as id_producto,
                                            nombre,precio , cantidad, detalles, descripcion, estado, ruta
                                            FROM producto
                                            Left JOIN imagen 
                                            ON producto.id_producto = imagen.id_producto WHERE producto.correo_vendedor = '"""+str(id_vendedor)+"'")
    
    #Cargamos la pagina con los datos del vendedor
    return render_template('producto/productos_vendedor.html', producto = productos)

###---------------------------------- MÉTODOS AUXILIARES ----------------------------------###

# Método auxiliar que nos devuelve las compras con comentario y el promedio de estrellas de un
# producto en específico.
def get_compras_con_reseña(id_producto):
    compras = db.session.query(Compra, Usuario).join(Usuario, Compra.correo_comprador == Usuario.correo)\
                                                .filter(Compra.id_producto == id_producto).all()
    compras_con_opinion = list(filter(lambda compra: compra.Compra.comentario != None, compras))
    compras_con_calificacion = list(filter(lambda compra: compra.Compra.numero_estrellas != None and compra.Compra.numero_estrellas != 0, compras))
    promedio_estrellas = 0
    if len(compras_con_calificacion) != 0:
        promedio_estrellas = reduce(lambda acc, compra: compra.Compra.numero_estrellas + acc
                                                        if compra.Compra.numero_estrellas != None 
                                                        else acc, compras_con_calificacion, 0)/len(compras_con_calificacion)
    return (compras_con_opinion,promedio_estrellas)

# Método auxiliar para guardar reseñas
def guarda_resenia(comentario, numero_estrellas, correo_comprador, id_producto):
    # buscamos todas las posibles compras que haya hecho el vendedor del producto
    compras = db.session.query(Compra).filter_by(correo_comprador=correo_comprador,id_producto=id_producto).all()
    for compra in compras:
        # las iteramos para buscar alguna que no contenga comentario
        if not compra.comentario:
            # en tal caso, agregamos la reseña y terminamos
            compra.comentario = comentario
            compra.numero_estrellas = numero_estrellas
            db.session.commit()
            return
    flash('Por favor, compre el producto')

'''
Método auxiliar que nos devuelve una lista de todos los productos que 
coincidan con el nombre dado por el usuario.
'''
def get_producto(nombre):
    producto = db.engine.execute("""SELECT producto.correo_vendedor as correo_vendedor, producto.id_producto as id_producto,
                                            nombre,precio , cantidad, detalles, descripcion, estado, ruta
                                            FROM producto
                                            Left JOIN imagen
                                            ON producto.id_producto = imagen.id_producto  WHERE nombre LIKE '%%"""+nombre+"%%'")
    return producto
    