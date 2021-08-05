from flask import Blueprint
from controllers.EvaluaController import evaluar_producto # Importamos la función de evaluar

# creamos una nueva blueprint evaluacion_bp y le asignamos el prefijo /evaluacion
evaluacion_bp = Blueprint('evaluacion', __name__, url_prefix='/evaluacion')

# bp que agrega la ruta de evaluar_producto
evaluacion_bp.route('/evaluacion_producto', methods=['POST','GET'])(evaluar_producto)