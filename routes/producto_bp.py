from flask import Blueprint
from controllers.ProductoController import crear_producto, actualizar_producto, eliminar_producto #importamos nuestras funciones necesarios

# creamos una nueva blueprint producto_bp, en este caso llamada producto y le asignamos el prefijo /producto
producto_bp = Blueprint('producto', __name__, url_prefix='/producto')

# agregamos una nueva ruta a producto_bp, en este caso, la ruta "/agrega_producto" cuando se entre
# a la dirección ".../producto/agrega_producto" se llamará al método agrega_producto de ProductoController
producto_bp.route('/crear_producto', methods=['POST','GET'])(crear_producto)
# análogo al caso anterior, se agrega la ruta "/actualiza", cuando se entre a la dirección
# ".../producto/actualiza" se llamará al método actualiza de ProductoController
producto_bp.route('/actualiza', methods=['POST'])(actualizar_producto)