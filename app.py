from flask import Flask, render_template
from config import Config
from routes.producto_bp import producto_bp
from routes.usuario_bp import usuario_bp
from routes.evaluacion_bp import evaluacion_bp
from models.Modelos import db


app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
app.testing = True

db.init_app(app)

app.register_blueprint(producto_bp, url_prefix='/producto')

app.register_blueprint(usuario_bp, url_prefix='/usuario')

app.register_blueprint(evaluacion_bp, url_prefix='/evaluacion')

app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)

@app.route('/')
def index():
    return render_template('index.html')
if __name__ == '__main__':
    app.debug = True
    app.run()