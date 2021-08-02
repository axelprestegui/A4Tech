from flask import request,json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy() # nuestro ORM
ma = Marshmallow() # para nuestros esquemas

"""
Clase modelo Vendedor que modela nuestra tabla Vendedor de nuestra BD con los atributos
correo, nombre, apellido_paterno, apellido_materno, contrasenia y telefono, así como la relación
productos para sus productos publicados. Posiblemente hará falta y será de utilidad agregar
alguna relación venta para cuando se haya implementado el modelo Compra.
"""
class Vendedor(db.Model):
    __tablename__ = 'vendedor'
    correo = db.Column(db.Unicode, primary_key=True, nullable=False, unique=True)
    nombre = db.Column(db.Unicode, nullable=False)
    apellido_paterno = db.Column(db.Unicode, nullable=False)
    apellido_materno = db.Column(db.Unicode, nullable=False)
    contrasenia = db.Column(db.Unicode, nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    productos = db.relationship('Producto', backref='vendedor')
    #ventas = db.relationship('Compra', backref='vendedor') para cuando se implemente compra

    def __init__(self, correo, nombre, apellido_paterno, apellido_materno, contrasenia, telefono):
        self.correo = correo
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_paterno = apellido_materno
        self.contrasenia = contrasenia
        self.telefono = telefono

class VendedorEsquema(ma.Schema):
    class Meta:
        fields = ('correo', 'nombre', 'apellido_paterno', 'apellido_materno', 'contrasenia', 'telefono')

"""
Clase modelo Comprador que modela nuestra tabla Comprador de nuestra BD con los atributos correo,
nombre, apellido_paterno, apellido_materno, contrasenia y telefono. Posiblemente hará falta y
será de utilidad agregar alguna relación compras para cuando se haya implementado el modelo Compra.
"""
class Comprador(db.Model):
    __tablename__ = 'comprador'
    correo = db.Column(db.Unicode, primary_key=True, nullable=False, unique=True)
    nombre = db.Column(db.Unicode, nullable=False)
    apellido_paterno = db.Column(db.Unicode, nullable=False)
    apellido_materno = db.Column(db.Unicode, nullable=False)
    contrasenia = db.Column(db.Unicode, nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    #compras = db.relationship('Compra', backref='comprador') para cuando se implemente compra

    def __init__(self, correo, nombre, apellido_paterno, apellido_materno, contrasenia, telefono):
        self.correo = correo
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_paterno = apellido_materno
        self.contrasenia = contrasenia
        self.telefono = telefono

class CompradorEsquema(ma.Schema):
    class Meta:
        fields = ('correo', 'nombre', 'apellido_paterno', 'apellido_materno', 'contrasenia', 'telefono')

"""
Clase modelo Producto que modela nuestra tabla Producto de nuestra BD con los atributos
correo_vendeor, nombre, precio, cantidad, detalles, descripción, estado, así como sus resenias y promedio_resenias.
Posiblemente hará falta y será de utilidad agregar alguna relación compra_venta para cuando se haya implementado
el modelo Compra.
"""
class Producto(db.Model):
    __tablename__ = 'producto'
    correo_vendedor = db.Column(db.Unicode, db.ForeignKey('vendedor.correo'), primary_key=True, nullable=False)
    id_producto = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    nombre = db.Column(db.Unicode, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    detalles = db.Column(db.Unicode, nullable=False)
    descripcion = db.Column( db.Unicode, nullable=True)
    estado = db.Column(db.Boolean, nullable=False)
    resenias = None
    promedio_resenias = None
    #compra_venta = db.relationschip('Compra', backref='producto') para cuando se implemente Compra

    def __init__(self, correo_vendedor, nombre, precio, cantidad, detalles, descripcion, estado):
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

"""
Clase modelo Compra que modela nuestra tabla Compra de nuestra BD con los atributos.
correo_comprador, correo_vendedor, id_producto, forma_pago, cantidad, costo_total direccion, 
comentario, numero_estrellas.
"""
class Compra(db.Model):
   __tablename__='compra' 
   correo_comprador = db.Column(db.Unicode, db.ForeignKey('comprador.correo'), primary_key=True, nullable=False)
   correo_vendedor = db.Column(db.Unicode, db.ForeignKey('vendedor.correo'), primary_key=True, nullable=False)
   id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), primary_key=True)
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

   def __init__(self, correo_comprador, correo_vendedor, id_producto, forma_pago, cantidad, costo_total, direccion, comentario,numero_estrellas):
       self.correo_comprador = correo_comprador
       self.correo_vendedor = correo_vendedor
       self.id_producto = id_producto
       self.forma_pago = forma_pago
       self.cantidad = cantidad
       self.costo_total = costo_total
       self.estado = direccion.estado
       self.ciudad = direccion.ciudad
       self.alcaldia = direccion.alcaldia
       self.colonia = direccion.colonia
       self.calle = direccion.calle
       self.numero_ext = direccion.numero_ext
       self.numero_int = direccion.numero_int
       self.codigo_postal = codigo_postal
       self.comentario = comentario
       self.numero_estrellas = numero_estrellas

class CompraEsquema(ma.Schema):
    class Meta: 
        fields = ('correo_comprador', 'correo_vendedor', 'id_producto', 'forma_pago', 'cantidad', 'costo_total', 'estado', 'ciudad', 'alcaldia', 'colonia', 'calle', 'numero_ext', 'numero_int', 'codigo_postal', 'comentario', 'numero_estrellas')

"""
Clase contenedora de datos de la direccion para no pasar tantos argumentos en clase Compra.
"""
class Direccion():
    def __init__(self, estado, ciudad, alcaldia, colonia, calle, numero_ext, numero_int, codigo_postal):
        self.estado = estado
        self.ciudad = ciudad
        self.alcaldia = alcaldia
        self.colonia = colonia
        self.calle = calle
        self.numero_ext = numero_ext
        self.numero_int = numero_int
        self.codigo_postal = codigo_postal