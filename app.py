from flask import Flask, render_template
from config import Config
from models.Modelos import Usuario
from routes.producto_bp import producto_bp
from routes.usuario_bp import usuario_bp
from models.Modelos import db
from flask_login import LoginManager


app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
app.testing = True

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(correo):
    try:
        return Usuario.query.get(correo)
    except:
        return None

db.init_app(app)

app.register_blueprint(producto_bp, url_prefix='/producto')

app.register_blueprint(usuario_bp, url_prefix='/usuario')


app.config.update(
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)

@app.route('/')
def index():
    return render_template('index.html')
if __name__ == '__main__':
    app.debug = True
    app.run()