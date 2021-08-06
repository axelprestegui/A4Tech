from flask import Blueprint
from controllers.ProductoController import * #importamos nuestras funciones necesarios
from controllers.CompraController import comprar_producto # Importamos método de compra

# creamos una nueva blueprint producto_bp, en este caso llamada producto y le asignamos el prefijo /producto
producto_bp = Blueprint('producto', __name__, url_prefix='/producto')

# agregamos una nueva ruta a producto_bp, en este caso, la ruta "/agrega_producto" cuando se entre
# a la dirección ".../producto/agrega_producto" se llamará al método agrega_producto de ProductoController
producto_bp.route('/crear_producto', methods=['POST','GET'])(crear_producto)
# análogo al caso anterior, se agrega la ruta "/actualiza", cuando se entre a la dirección
# ".../producto/actualiza" se llamará al método actualiza de ProductoController
producto_bp.route('/actualizar_producto', methods=['POST', 'GET'])(actualizar_producto)
producto_bp.route('/eliminar_producto', methods=['POST', 'GET'])(eliminar_producto)

# bp que agrega la ruta de compra_producto
producto_bp.route('/comprar_producto', methods=['POST','GET'])(comprar_producto)
producto_bp.route('/buscar_producto', methods=['POST', 'GET'])(buscar_producto)
producto_bp.route('/resultado_busqueda' , methods=['POST', 'GET'])(resultado_busqueda)

producto_bp.route('/mostrar_todos', methods = ['POST','GET'])(mostrar_todos)
producto_bp.route('/productos_vendedor', methods = ['POST','GET'])(productos_vendedor)
producto_bp.route('/ver_articulo', methods = ['POST','GET'])(ver_articulo)
producto_bp.route('/ver_articulo_buscado', methods = ['POST','GET'])(ver_articulo_buscado)
