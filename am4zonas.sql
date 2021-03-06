/* CREACION DE LA BASE DE DATOS 'am4zonas'*/

/* Si la base de datos 'am4zonas' existe, la borramos. */
drop database if exists am4zonas;

/* Creamos la base de datos 'am4zonas'. */
create database am4zonas;

/* Nos conectamos a la base de datos 'am4zonas'*/
\c am4zonas

/*  Creamos la tabla Comprador cuya llave primaria será Correo.
    Acepta tuplas de la forma: ('axelprestegui@ciencias.unam.mx','Axel','Prestegui','Ramos','cubito53',5576679861)
*/
CREATE TABLE Usuario (
    Correo varchar(320) NOT NULL,
    Nombre varchar(55) NOT NULL,
    Apellido_paterno varchar(70) NOT NULL,
    Apellido_materno varchar(70) NOT NULL,
    Contrasenia char(255) NOT NULL,
    Telefono bigint NOT NULL,
    Tipo boolean NOT NULL,
    CONSTRAINT PK_CorreoUsuario PRIMARY KEY (Correo)
);

/*  Creamos la tabla Producto cuya llave primaria compuesta será Correo_Vendedor y Id_Producto. 
                        'CHECK' Garantizamos que hay piezas en reserva.
                        'CHECK' Garantizamos que no hay precios negativos.
    Notemos que 'ON DELETE CASCADE' Una llave foránea con eliminación en cascada significa que si se elimina un 
                                    registro en la tabla principal, los registros correspondientes en la tabla 
                                    secundaria se eliminarán automáticamente.
                'ON UPDATE CASCADE' Una llave foránea con actualización en cascada significa que si se actualiza un 
                                    registro en la tabla principal, los registros correspondientes en la tabla 
                                    secundaria se actualizarán automáticamente.
    Acepta tuplas de la forma: ('dererex@ciencias.unam.mx', 'Lápices de Colores Marca Steadler 24 piezas', 500.00, 50, 'Excelentes lápices de colores de buena 
                                        calidad', True)
*/
CREATE TABLE Producto (
    Correo_Vendedor varchar(320) NOT NULL,
    Id_Producto SERIAL UNIQUE,
    Nombre varchar(500) NOT NULL,
    Precio float NOT NULL,
    Cantidad int NOT NULL,
    Detalles text NOT NULL,
    Descripcion text,
    Estado boolean NOT NULL,
    CONSTRAINT PK_Producto PRIMARY KEY (Id_Producto, Correo_Vendedor),
    CONSTRAINT FK_CorreoVendedor FOREIGN KEY (Correo_Vendedor) references Usuario (Correo) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT verificaCantidad CHECK (-1 < Cantidad),
    CONSTRAINT verificaPrecio CHECK (0 = Precio or 0 < Precio)
);

/*  Creamos la tabla Compra cuya llave primaria compuesta será Correo_Comprador, Correo_Vendedor y Id_Producto.
    Notemos que 'ON DELETE CASCADE' Una llave foránea con eliminación en cascada significa que si se elimina un 
                                    registro en la tabla principal, los registros correspondientes en la tabla 
                                    secundaria se eliminarán automáticamente.
                'ON UPDATE CASCADE' Una llave foránea con actualización en cascada significa que si se actualiza un 
                                    registro en la tabla principal, los registros correspondientes en la tabla 
                                    secundaria se actualizarán automáticamente.
    Acepta tuplas de la forma: ()
*/
CREATE TABLE Compra (
    Correo_Comprador varchar(320) NOT NULL,
    Correo_Vendedor varchar(320) NOT NULL,
    Id_Producto int NOT NULL,
    Id_Compra SERIAL UNIQUE,
    Forma_Pago varchar(320) NOT NULL,
    Cantidad int NOT NULL,
    Costo_Total int NOT NULL, 
    Estado varchar(50) NOT NULL,
    Ciudad varchar(50) NOT NULL,
    Alcaldia varchar(55) NOT NULL,
    Colonia varchar(55) NOT NULL,
    Calle varchar(75) NOT NULL,
    Numero_Ext int NOT NULL,
    Numero_Int varchar(15),
    Codigo_Postal int NOT NULL,
    Comentario text,
    Numero_Estrellas int,
    CONSTRAINT PK_Compra PRIMARY KEY (Correo_Comprador, Correo_Vendedor, Id_Producto, Id_Compra),
    CONSTRAINT FK_CorreoVendedor FOREIGN KEY (Correo_Vendedor) references Usuario (Correo) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_CorreoComprador FOREIGN KEY (Correo_Comprador) references Usuario (Correo) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Id FOREIGN KEY (Id_Producto) references Producto (Id_Producto) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Imagen (
    Correo_Vendedor varchar(320) NOT NULL,
    Id_producto int NOT NULL,
    Ruta varchar(320),
    CONSTRAINT PK_Imagen PRIMARY KEY (Correo_Vendedor, Ruta),
    CONSTRAINT FK_CorreoVendedor FOREIGN KEY (Correo_Vendedor) references Usuario (Correo) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Id_producto FOREIGN KEY (Id_producto) references Producto (Id_producto) ON DELETE CASCADE ON UPDATE CASCADE
);

/* Algunas tuplas a insertar en la base*/
/**
INSERT INTO usuario VALUES
('axelprestegui@ciencias.unam.mx','Axel','Prestegui','Ramos','cubito53',1000000000,true),
('derekalmanzacancer@gmail.com','Derek','AP','AM','hola1234',5545648748,true),
('presteguiaxel@gmail.com','Axel','Prestegui','Ramos','qwerty',1000000000,false),
('dererex@ciencias.unam.mx','Derek','AP','AM','hola1234',5545648748,true),
('tania@gmail.com','Tania','AP','AM','qwerty',1000000000,false);

INSERT INTO producto (Correo_Vendedor, Nombre, Precio, Cantidad, Detalles, Descripcion, Estado) VALUES
('axelprestegui@ciencias.unam.mx', 'Zapatos adidas número 26 edición limitada', 1500.00, 10, 'Sin detalles', 'Sin descripción', true),
('dererex@ciencias.unam.mx', 'Lápices de Colores Marca Steadler 24 piezas', 500.00, 50, 'Excelentes lápices de colores de buena calidad','Sin descripción',true);

INSERT INTO compra (Correo_Comprador,Correo_Vendedor,Id_Producto,Forma_Pago,Cantidad,Costo_Total,Estado,Ciudad,Alcaldia,Colonia,Calle,Numero_Ext,Numero_Int,Codigo_Postal,Comentario) VALUES
('tania@gmail.com','axelprestegui@ciencias.unam.mx',1,'efectivo',2,3000.0,'CDMX','CDMX','Coyoacan','asdas','calle 10',1010,401,04420,'Excelente producto! 100% recomendado'),
('derekalmanzacancer@gmail.com','presteguiaxel@gmail.com',1,'efectivo',2,3000.0,'CDMX','CDMX','Coyoacan','asds','calle 10',1010,401,04420,'Me gustaron mucho, muy buena edición');

INSERT INTO compra (Correo_Comprador,Correo_Vendedor,Id_Producto,Forma_Pago,Cantidad,Costo_Total,Estado,Ciudad,Alcaldia,Colonia,Calle,Numero_Ext,Numero_Int,Codigo_Postal) VALUES
('presteguiaxel@gmail.com','axelprestegui@ciencias.unam.mx',1,'efectivo',2,3000.0,'CDMX','CDMX','Coyoacan','asdas','calle 10',1010,401,04420);
**/