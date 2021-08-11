from flask import request,json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy() # nuestro ORM
ma = Marshmallow() # para nuestros esquemas

class Usuario(db.Model, UserMixin):
    """
    Clase modelo Vendedor que modela nuestra tabla Vendedor de nuestra BD.

    Atributos:
        correo              El correo que será usado como llave principal para cada usuario.
        nombre              Nombre del usuario.
        apellido_paterno    Apellido paterno del usuario.
        apellido_materno    Apellido materno del usuario.
        contrasenia         Contraseña del usuario.
        telefono            Número telefónico del usuario.
        tipo                Rol con el cual se registró: True para vendedor y False para comprador.
        productos           Relación con Producto, aquellos productos publicados por el usuario si este es vendedor.
    """
    __tablename__ = 'usuario'
    correo = db.Column(db.Unicode, primary_key=True, nullable=False, unique=True)
    nombre = db.Column(db.Unicode, nullable=False)
    apellido_paterno = db.Column(db.Unicode, nullable=False)
    apellido_materno = db.Column(db.Unicode, nullable=False)
    contrasenia = db.Column(db.Unicode, nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.Boolean, nullable=False)
    productos = db.relationship('Producto', backref='usuario')
    
    def __init__(self, correo, nombre, apellido_paterno, apellido_materno, contrasenia, telefono, tipo):
        """
        Constructor de la clase.
        """
        self.correo = correo
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.contrasenia = contrasenia
        self.telefono = telefono
        self.tipo = tipo

    def check_contrasenia(self, constrasenia):
        """
        check_contrasenia se encarga de validar las contraseñas proporcionadas al iniciar sesión.

        :param contrasenia: la contraseña pasada al intentar iniciar sesión
        :return: True syssla contraseña proporcionada es igual a la contraseña almacenada en la BD.
        """
        return self.contrasenia.replace(' ','') == constrasenia.replace(' ','')

    def is_authenticated(self):
        """
        is_authenticates se encarga de decirnos si hay un usuario en sesión en nuestra aplicación

        :return: True si se encuentra un usario en sesión.
        """
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.correo

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class UsuarioEsquema(ma.Schema):
    class Meta:
        fields = ('correo', 'nombre', 'apellido_paterno', 'apellido_materno', 'contrasenia', 'telefono', 'tipo')

class Producto(db.Model):
    """
    Clase modelo Producto que modela nuestra tabla Producto de nuestra BD.

    Atributos:
        correo_vendedor     El correo del usuario vendedor que publica este producto.
        id_producto         Id del producto que lo identifica de manera única junto a correo_vendedor.
        nombre              Nombre del producto.
        precio              Costo del artículo por unidad.
        cantidad            Unidades disponibles para la venta.
        detalles            Detalles del producto.
        descripcion         Descripción del producto.
        estado              Estado del producto: True para nuevo, False para usado.
    """
    __tablename__ = 'producto'
    correo_vendedor = db.Column(db.Unicode, db.ForeignKey('usuario.correo'), primary_key=True, nullable=False)
    id_producto = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    nombre = db.Column(db.Unicode, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    detalles = db.Column(db.Unicode, nullable=False)
    descripcion = db.Column( db.Unicode, nullable=True)
    estado = db.Column(db.Boolean, nullable=False)

    def __init__(self, correo_vendedor, nombre, precio, cantidad, detalles, descripcion, estado):
        """
        Constructos de la clase.
        """
        self.correo_vendedor = correo_vendedor
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.detalles = detalles
        self.descripcion = descripcion
        self.estado = estado

class ProductoEsquema(ma.Schema):
    class Meta:
        fields = ('correo_vendedor', 'id_producto', 'nombre', 'precio', 'cantidad', 'detalles', 'descripcion', 'estado')

class Compra(db.Model):
   """
    Clase modelo Compra que modela nuestra tabla Compra de nuestra BD.

    Atributos:
        correo_comprador    Correo del usuario comprador que realiza la compra.
        correo_vendedor     Correo del usuario vendedor del producto.
        id_producto         Id único del producto comprado.
        forma_pago          Forma que comprador usará para pagar la compra.
        cantidad            Cantidad de elementos que se está comprando del producto.
        costo_total         Total del costo de la compra.
        direccion           Atributos que conforman la dirección de la compra.
        comentario          Opinión que el usuario comprador puede dar hacerca del producto y su compra.
        numero_estrellas    Calificación dada por el usuario comprador al producto entre 1 y 5. 0 cuando se decide no calificar.
    """
   __tablename__='compra' 
   correo_comprador = db.Column(db.Unicode, db.ForeignKey('usuario.correo'), primary_key=True, nullable=False)
   correo_vendedor = db.Column(db.Unicode, db.ForeignKey('usuario.correo'), primary_key=True, nullable=False)
   id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), primary_key=True)
   id_compra = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
   forma_pago = db.Column(db.Unicode, nullable=False)
   cantidad = db.Column(db.Integer, nullable=False)
   costo_total = db.Column(db.Integer, nullable=False)
   estado = db.Column(db.Unicode, nullable= False)
   ciudad = db.Column(db.Unicode, nullable= False)
   alcaldia = db.Column(db.Unicode, nullable= False)
   colonia = db.Column(db.Unicode, nullable= False)
   calle = db.Column(db.Unicode, nullable= False)
   numero_ext = db.Column(db.Integer, nullable= False)
   numero_int = db.Column(db.Unicode)
   codigo_postal = db.Column(db.Integer, nullable= False)
   comentario = db.Column(db.Unicode)
   numero_estrellas = db.Column(db.Integer)

   def __init__(self, correo_comprador, correo_vendedor, id_producto, forma_pago, cantidad, costo_total, estado, ciudad, alcaldia, colonia, calle, numero_ext, numero_int, codigo_postal, comentario,numero_estrellas):
       """
       Constructor de la clase
       """
       self.correo_comprador = correo_comprador
       self.correo_vendedor = correo_vendedor
       self.id_producto = id_producto
       self.forma_pago = forma_pago
       self.cantidad = cantidad
       self.costo_total = costo_total
       self.estado = estado
       self.ciudad = ciudad
       self.alcaldia = alcaldia
       self.colonia = colonia
       self.calle = calle
       self.numero_ext = numero_ext
       self.numero_int = numero_int
       self.codigo_postal = codigo_postal
       self.comentario = comentario
       self.numero_estrellas = numero_estrellas

class CompraEsquema(ma.Schema):
    class Meta: 
        fields = ('correo_comprador', 'correo_vendedor', 'id_producto', 'forma_pago', 'cantidad', 'costo_total', 'estado', 'ciudad', 'alcaldia', 'colonia', 'calle', 'numero_ext', 'numero_int', 'codigo_postal', 'comentario', 'numero_estrellas')

class Imagen(db.Model):
    """
    Clase modelo Imagen que modela nuestra tabla Imagen de nuestra BD.

    Atributos:
        correo_vendedor     Correo del usuario vendedor, usado como llave primario, que publica el producto al cual pertenece la imagen.
        id_producto         Id del producto al cual pertenece la imagen.
        ruta                Ruta donde se encuentra almacenada la imagen, usada como llave primaria.
    """
    __tablename__ = 'imagen'
    correo_vendedor = db.Column(db.Unicode, db.ForeignKey('usuario.correo'), primary_key=True, nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'))
    ruta = db.Column(db.Unicode, db.ForeignKey('usuario.correo'),primary_key=True)

    #compra_venta = db.relationschip('Compra', backref='producto') para cuando se implemente Compra

    def __init__(self, correo_vendedor, id_producto, ruta):
        self.correo_vendedor = correo_vendedor
        self.id_producto = id_producto
        self.ruta = ruta

class ProductoEsquema(ma.Schema):
    class Meta:
        fields = ('correo_vendedor', 'ruta')
