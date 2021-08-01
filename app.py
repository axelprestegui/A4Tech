from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config
from flask import jsonify
from routes.producto_bp import producto_bp
from routes.usuario_bp import usuario_bp
from models.Modelos import db


app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(producto_bp, url_prefix='/producto')

app.register_blueprint(usuario_bp, url_prefix='/usuario')

@app.route('/')
def index():
    return render_template('index.html')
if __name__ == '__main__':
    app.debug = True
    app.run()