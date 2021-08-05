from flask import Blueprint
from controllers.UsuarioController import iniciar_sesion, cerrar_sesion
from controllers.RegistroController import registrar_usuario

# Create a blueprint that will link the general routes file to the app
usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')

# Add login and logout routes to the blueprint
usuario_bp.route('/iniciar_sesion', methods=['POST', 'GET'])(iniciar_sesion)
usuario_bp.route('/cerrar_sesion', methods=['POST', 'GET'])(cerrar_sesion)
usuario_bp.route('/registrar_usuario',methods = ['POST','GET'])(registrar_usuario)