/* Unos cuántos usuarios más*/
INSERT INTO usuario VALUES
('axelprestegui@ciencias.unam.mx','Axel','Prestegui','Ramos','cubito53',1000000000,true);

/*Insertamos 10 usuarios nuevos 5 vendedores y 5 compradores*/
INSERT INTO usuario VALUES
('abraham_355@ciencias.unam.mx','Abraham','Lagunas','Trejo','3st4N0es#n4Contraseña',5538051085,true),
('ogfastpw@hotmail.com','Paul','Walker','nAM','2fst2S3c',8444823692,true),
('robscallonof@gmail.com','Rob','Scallon','nAM','gut4rStr1ng',7828188844,true),
('iamgroot@gmail.com','Taika David','Cohen','nAM','G#4rdi4nOTG',5672505734,true),
('mando@gmail.com','Din','Djarin','nAM','Th1sI$th3W4y',1273450350,true),
('keanur@gmail.com','Keanu','Reeves', 'nAM','ne0isN#tW1ck',9837690500,false),
('robpendulum@gmail.com','Rob','Swire','nAM','p3nd#lum',7992645133, false),
('elpapadeloslatinos@hotmail.com','Elmer','Figueroa','Arce','Ch4yan#',1168481207,false),
('dlalex@gmail.com','Diego','Luna','Alexander','4m0r#sP3rros',1397970569,false),
('memototoro@gmail.com','Guillermo','del Toro','Gómez','T1t4nF4#n0',9803040253,false);

/*Insertamos 5 productos por cada vendedor registrado*/
INSERT INTO producto (correo_vendedor, nombre, precio, cantidad, detalles, descripcion, estado) VALUES
('axelprestegui@ciencias.unam.mx','LB-Silhouette Works GT Nissan 35GT-RR Ver.2', 99.99, 35,'Serie HW J-Imports, 8/10','Auto de hot wheels de la serie importados de japon',true),
('abraham_355@ciencias.unam.mx', 'Control Xbox One Edicion Le Mans N 2', 2000.00,1, 'Control Xbox One, compatible con PC','Control edicion especial de Le Mans en conmemoración del decimo aniversario de la serie de juegos Forza', false),
('abraham_355@ciencias.unam.mx', 'Sennheiser Audífonos HD 660S', 10500.42,100 ,'Sennheiser Audífonos HD 660S, Alámbrico, 3 Metros, 3.5mm, Negro','Los nuevos HD 660 s de sennheiser son los audífonos ideales para audiófilos apasionados, gracias a su diseño abierto y dinámico',true),
('abraham_355@ciencias.unam.mx', 'Motorola One',4000.55, 10, 'Motorola One 5.8 plg 64 GB Negro Desbloqueado','Saca al fotógrafo que llevas dentro con el Motorola One 64 GB 5.8 plg Negro Desbloqueado que gracias a su cámara doble de 13 MP + 2 MP, tomarás fotos profesionales con su avanzados recursos como el de color destacado, con el que podrás eligir un color para resaltar y dejar lo demás en blanco y negro', true),
('abraham_355@ciencias.unam.mx', 'Need for Speed: Pro Street', 500,1, 'Videojuego xbox 360, Edición Platinum Hits','Lleva a casa el mejor juego de la franquicia de need for speed para 360', false),
('ogfastpw@hotmail.com','Brian´s Nissan Skyline Gtr R34 ', 559, 10, 'Brian´s Nissan Skyline Gtr R34 Rapido Y Furioso 1:24','El vendedor no incluyó una descripción del producto',true),
('ogfastpw@hotmail.com','Juego de rines r34 Nismo', 1559.34, 1,'5 x Rines Nismo, calcomanias blanco y rojo - Skyline GTR R32 R33 R34 R35 Silvia LMGT4','El vendedor no incluyó una descripción del producto',true),
('ogfastpw@hotmail.com','TOUGHBOOK 31',15000,1,'LAPTOP USO RUDO','La Panasonic TOUGHBOOK® 31 es la laptop de uso rudo con el historial más completo del mercado', true),
('ogfastpw@hotmail.com', 'DieCast Hotwheels Mitsubishi Eclipse', 150.99, 400,'DieCast Hotwheels Mitsubishi Eclipse 2021 Fast & Furious Fast Stars 1/5 [Verde] escala 1:64 Premium','El vendedor no incluyó una descripción del producto', true),
('ogfastpw@hotmail.com','Dom Dodge Charger', 2099.00, 10, 'Ninguna','Version en lego del mitico auto de Dom de la saga Rapido y furioso', true),
('robscallonof@gmail.com','Rob Scallon Signature', 2399.99, 15, 'Chapman Guitars ML1 RS Rob Scallon Signature Guitar','One of the first things you ll notice about the ML1 RS is the neck-through design', true),
('robscallonof@gmail.com','Amplificador Marshall Micro Amp',25000.25, 2,'Amplificador Marshall Micro AMP MS-4 Combo Transistor 2W','Perfecto para ti. Con tu amplificador Marshall Micro Amp MS-4, mejorarás todos los sonidos y encontrarás las melodías que estás buscando. Gracias a su potencia de 2 W, disfrutarás de un tono real y una gran apariencia', true),
('robscallonof@gmail.com','Mooer Reecho Digital Delay',2101.79,5,'Mooer Reecho Digital Delay Guitar Effects Pedal','The Mooer Reecho Digital Delay offers 3 awesome modes of delay: Analog, RealEcho, and TapeEcho. The controls are simple and easy-to-use so you can find a sound you like in no time whether you like a spacey echo or a bluesy/country style delay sound. Its full metal casing makes it durable and road ready, and like most great effects pedals it has true bypass.',true),
('robscallonof@gmail.com','KALA Ubass California Exotic Walnut Top Solid Body with a Gigbag Fretted / 4 String',23058.36,3,'Kala Ubass California Exotic Walnut Top Solid Body with a Gigbag Fretted / 4 String', 'El vendedor no incluyó una descripción del producto', true),
('robscallonof@gmail.com','Otamatone "Deluxe"', 3695.61, 5, 'Otamatone "Deluxe" versión en inglés Blanco y negro','La otamatone se pueden reproducir fácilmente y tiene un sonido digital a analógico Movimiento con el sonido de un tambor.', true),
('iamgroot@gmail.com','Ratcatcher II con Sebastian', 289, 3, 'Ratcatcher II con Sebastian','El vendedor no incluyó una descripción del producto', true),
('iamgroot@gmail.com', 'Marvel Legends The Grandmaster + Korg Nuevo Thor Ragnarok', 850, 45, 'Sin detalles', 'Se pone en venta el paquete de Marvel Legends The Grandmaster + Korg Thor Ragnarok. Nuevo, marca hasbro. El paquete está nuevo y sellado Se hacen envíos a cualquier parte de México. Se acepta mercado pago.', true),
('iamgroot@gmail.com','Jojo Rabbit', 171, 300, 'Jojo Rabbit - Blu Ray [Blu-ray]', 'El vendedor no incluyó una descripción del producto', true),
('iamgroot@gmail.com','Camisa Hawaiana', 600, 50, 'Hombres Aloha Camisa Hawaiana en Mapa y Paisajes Amarillo','El vendedor no incluyó una descripción del producto', true),
('iamgroot@gmail.com', 'Marvel Thor Love and Thunder Camiseta', 500, 60, 'Colores lisos: 100% algodón; Gris brezo: 90% algodón, 10% poliéster; Todos los demás: 50% algodón, 50% poliéster', 'El vendedor no incluyó una descripción del producto', true),
('mando@gmail.com', 'Black Series Sable láser de Star Wars Mandalorian Force FX Elite', 8499.99, 1, 'LED avanzados con efectos de sonido: combina LED avanzados y efectos de sonido de sable de luz inspirados en el entretenimiento, el sable de luz Force FX Elite es el sable de luz Force FX más realista hasta la fecha', 'El vendedor no incluyó una descripción del producto', true),
('mando@gmail.com', 'STAR WARS The Black Series - The Mandalorian - Casco electrónico Premium - Artículo de colección para Juego de rol -Edad: 14+', 3495.86, 1, 'CASCO ELECTRÓNICO PREMIUM: Con su decorado altamente detallado, diseño basado en la serie, acolchado interior y tamaño ajustable, este casco es una adición fantástica a toda colección Star Wars', 'El vendedor no incluyó una descripción del producto', true),
('mando@gmail.com', 'Mattel Star Wars The Mandalorian The Child 8" Peluche para niños de 3 años en adelante, 8 Pulgadas, Verde', 329, 1, '¡Este juguete de peluche de 20 cm de "The Child" encantará a los fans de Star Wars en todas partes!','El vendedor no incluyó una descripción del producto', true),
('mando@gmail.com', 'LEGO Kit de construcción Star Wars: The Mandalorian 75292 The Razor Crest™ (1023 Piezas)', 2899, 10, 'The Mandalorian 75292 The Razor Crest, divertido juguete de construcción para niños que fomenta el juego creativo (1023 piezas)','El vendedor no incluyó una descripción del producto', true),
('mando@gmail.com', 'Funko - Pop! Star Wars: The Mandalorian - Ahsoka with Sabers Figura Coleccionable, Keychain, Multicolor', 319, 200, 'From The Mandalorian, Ahsoka with Sabers, as a stylized Pop!','El vendedor no incluyó una descripción del producto', true);

/*Insertamos las imagenes de los productos listados arriba*/
INSERT INTO imagen VALUES
('abraham_355@ciencias.unam.mx',1,'../../static/images/abraham_355@ciencias.unam.mx/1/LBGTR.jpg'),
('abraham_355@ciencias.unam.mx',2,'../../static/images/abraham_355@ciencias.unam.mx/2/xctrllrLMnsN.png'),
('abraham_355@ciencias.unam.mx',3,'../../static/images/abraham_355@ciencias.unam.mx/3/SenHD660.jpg'),
('abraham_355@ciencias.unam.mx',4,'../../static/images/abraham_355@ciencias.unam.mx/4/MotoOne.jpg'),
('abraham_355@ciencias.unam.mx',5,'../../static/images/abraham_355@ciencias.unam.mx/5/proStrt.jpg'),
('ogfastpw@hotmail.com',6,'../../static/images/ogfastpw@hotmail.com/6/SkyR34.jpg'),
('ogfastpw@hotmail.com',7,'../../static/images/ogfastpw@hotmail.com/7/RinNismo.jpg'),
('ogfastpw@hotmail.com',8,'../../static/images/ogfastpw@hotmail.com/8/TOUGHBOOK.jpg'),
('ogfastpw@hotmail.com',9,'../../static/images/ogfastpw@hotmail.com/9/BriansEcl.jpg'),
('ogfastpw@hotmail.com',10,'../../static/images/ogfastpw@hotmail.com/10/DomChar.jpeg'),
('robscallonof@gmail.com',11,'../../static/images/robscallonof@gmail.com/11/RobSig.jpg'),
('robscallonof@gmail.com',12,'../../static/images/robscallonof@gmail.com/12/RobAmp.jpg'),
('robscallonof@gmail.com',13,'../../static/images/robscallonof@gmail.com/13/RobPedal.jpeg'),
('robscallonof@gmail.com',14,'../../static/images/robscallonof@gmail.com/14/RobBass.jpg'),
('robscallonof@gmail.com',15,'../../static/images/robscallonof@gmail.com/15/otomatone.jpg'),
('iamgroot@gmail.com',16,'../../static/images/iamgroot@gmail.com/16/ratcat.jpg'),
('iamgroot@gmail.com',17,'../../static/images/iamgroot@gmail.com/17/korg.jpg'),
('iamgroot@gmail.com',18,'../../static/images/iamgroot@gmail.com/18/jojo.jpg'),
('iamgroot@gmail.com',19,'../../static/images/iamgroot@gmail.com/19/hawainana.jpg'),
('iamgroot@gmail.com',20,'../../static/images/iamgroot@gmail.com/20/camiseta.jpeg'),
('mando@gmail.com',21,'../../static/images/mando@gmail.com/21/darksaber.jpg'),
('mando@gmail.com',22,'../../static/images/mando@gmail.com/22/helmet.jpg'),
('mando@gmail.com',23,'../../static/images/mando@gmail.com/23/baby.jpg'),
('mando@gmail.com',24,'../../static/images/mando@gmail.com/24/razor.jpg'),
('mando@gmail.com',25,'../../static/images/mando@gmail.com/25/funko.jpg');

/*SELECT * FROM producto LEFT JOIN imagen ON producto.id_producto = imagen.id_producto;*/
/*Por ultimo añadimos algunas compras simulando que se compran articulos de arriba*/

INSERT INTO compra (Correo_Comprador,Correo_Vendedor,Id_Producto,Forma_Pago,Cantidad,Costo_Total,Estado,Ciudad,Alcaldia,Colonia,Calle,Numero_Ext,Numero_Int,Codigo_Postal,Comentario,Numero_Estrellas) VALUES
('memototoro@gmail.com','mando@gmail.com',1,'efectivo',1,329,'CDMX','CDMX','Cuauhtémoc','Centro','Pino Suarez',35,3,06000,'Un juguete muy bueno para la familia',5),
('memototoro@gmail.com', 'iamgroot@gmail.com',1,'efectivo',1,289,'CDMX','CDMX','Cuauhtémoc','Centro','Pino Suarez',35,3,06000,'Una de mis mejores compras',5),
('dlalex@gmail.com','mando@gmail.com', 1, 'efectivo', 1, 3495.86,'Monterrey','Nuevo Leon','Aldama','Alamos','Paseo Alamos',24,18,07001,'El unico lugar donde se puede encontrar',5),
('dlalex@gmail.com', 'robscallonof@gmail.com',2,'efectivo',1,2399.99,'Monterrey','Nuevo Leon','Aldama','Alamos','Paseo Alamos',24,18,07001,'Podria ser mejor',3),
('elpapadeloslatinos@hotmail.com','robscallonof@gmail.com',2,'efectivo',1,3695.61,'Puerto Rico','Rio Piedras','Costa Grande','Paloloapan','Segunda avenida',42,18,12065,'Excelente precio calidad',5),
('elpapadeloslatinos@hotmail.com','iamgroot@gmail.com', 2,'efectivo',1,600,'Puerto Rico','Rio Piedras','Costa Grande','Paloloapan','Segunda avenida',42,18,12065,'No imagino mi vida sin el',5),
('robpendulum@gmail.com','abraham_355@ciencias.unam.mx', 2,'efectivo', 3,31501.26,'Chicago','Illinois','Downtown','Little Ilinois','2nd Street',7,12,65197,'Pense que era mas grande',3),
('robpendulum@gmail.com', 'robscallonof@gmail.com',2,'efectivo,25000.25',1,25000.25,'Chicago','Illinois','Downtown','Little Ilinois','2nd Street',7,12,65197,'El regalo de cumpleños perfecto',5),
('keanur@gmail.com','mando@gmail.com', 24, 'efectivo', 1,319,'CDMX','CDMX','Venustiano Carranza','Balbuena','Ceciclio Robelo',4,18,05050,'Pronto pedire mas',5),
('keanur@gmail.com','iamgroot@gmail.com',19,'efectivo',1,600,'CDMX','CDMX','Venustiano Carranza','Balbuena','Ceciclio Robelo',4,18,05050,'Sin palabras',5);


/*Derek*/

INSERT INTO usuario VALUES
-- Vendedor
('derek.almanza.infante@gmail.com', 'Derek','Almanza', 'Infante','12345', 53422233, true), 
-- Compradores
('juan.perez@gmail.com', 'Juan', 'Perez', 'Gonzalez', '12345', 53425667, false),
('yololoi.@gmail.com', 'Cristian', 'Ferras', 'Perez', '12345', 367587442, false),
('el.Dicter@gmail.com', 'Dicter', 'De los Cabos', 'Cañaveral', '12345', 54927992, false),
('lenon@gmail.com', 'Lenon', 'Pieldelobo', 'Rajado', '12345', 6597983, false),
('pancal@gmail.com', 'Pancracio', 'Calva', 'Morena', '12345', 457492223, false);

-- Productos piublicados por vendedor
INSERT INTO producto (Correo_Vendedor, Nombre, Precio, Cantidad, Detalles, Descripcion, Estado) VALUES
('derek.almanza.infante@gmail.com', 'Servilleta usada', 3.00, 1, 'Servilleta con las babas del vendedor', 'Blanca (casi)', false),
('derek.almanza.infante@gmail.com', 'Silla gamer', 1000.00, 5, 'Sin detalles', 'Sin descripcion', true),
('derek.almanza.infante@gmail.com', 'Botella de awa con awa', 15.00, 100, 'Botella de awa bonita', 'Puede contener awa de la llave', true),
('derek.almanza.infante@gmail.com', 'Pata de conejo', 60.00, 4, 'LLeve su pata de conejo para sacar 10 en IS', 'Pata de conejo negro, producto usado ya que el conejo vivo las usaba para caminar', false),
('derek.almanza.infante@gmail.com', 'Galleta Oreo mordida con forma de moneda de $5', 10008000.00, 1, 'Galleta extraordinaria con forma de moneda de $5', 'Sin descripcion', false);

-- Compras con comentarios
INSERT INTO compra (Correo_Comprador,Correo_Vendedor,Id_Producto,Forma_Pago,Cantidad,Costo_Total,Estado,Ciudad,Alcaldia,Colonia,Calle,Numero_Ext,Numero_Int,Codigo_Postal,Comentario,Numero_Estrellas) VALUES
('juan.perez@gmail.com', 'derek.almanza.infante@gmail.com', 26, 'efectivo',1, 3.00, 'CDMX', 'CDMX', 'Tlalpan', 'Arboledas', 'Laureles', 231, 11, 08070, 'excelente producto, efectivamente venían las babas de mi crush',5),
('el.Dicter@gmail.com', 'derek.almanza.infante@gmail.com', 28, 'debito',2, 30.00, 'CDMX', 'CDMX', 'Tlalpan', 'Arboledas', 'Laureles', 233, 14, 08070, 'Compré dos botellasw y ninguna traía awa, pero las botellas estaban bonitas.',4),
('lenon@gmail.com', 'derek.almanza.infante@gmail.com', 29, 'efectivo',3, 180.00, 'CDMX', 'CDMX', 'Tlalpan', 'Arboledas', 'Laureles', 234, 13, 08070, 'Disgustado, compré 3 patas de conejo para sacar 30 en IS y solo saqué 10, no confíen en el vendedor.',3),
('pancal@gmail.com', 'derek.almanza.infante@gmail.com', 30, 'debito', 1, 10008000.00, 'CDMX', 'CDMX', 'Tlalpan', 'Arboledas', 'Laureles', 235, 19, 08070, 'Réplica exacta de una moneda de $5 en la galleta, valió cada peso invertido.',5);

-- Compras sin comentarios
INSERT INTO compra (Correo_Comprador,Correo_Vendedor,Id_Producto,Forma_Pago,Cantidad,Costo_Total,Estado,Ciudad,Alcaldia,Colonia,Calle,Numero_Ext,Numero_Int,Codigo_Postal) VALUES
('yololoi.@gmail.com', 'derek.almanza.infante@gmail.com', 26, 'efectivo',1, 1000.00, 'CDMX', 'CDMX', 'Tlalpan', 'Arboledas', 'Laureles', 232, 12, 08070);

