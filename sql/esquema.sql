-- =========================================================
-- FITZONE STORE
-- SEMANA 13
-- BASE DE DATOS RELACIONAL MYSQL
-- =========================================================


-- =========================================================
-- CREACIÓN DE LA BASE DE DATOS
-- =========================================================

CREATE DATABASE IF NOT EXISTS fitness_zone
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;


USE fitness_zone;


-- =========================================================
-- TABLA: CATEGORIAS
-- =========================================================
--
-- Se utiliza para demostrar una relación mediante
-- PRIMARY KEY y FOREIGN KEY.
--
-- Una categoría puede tener muchos productos.
-- =========================================================

CREATE TABLE IF NOT EXISTS categorias (

    id_categoria INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(50) NOT NULL UNIQUE

);


-- =========================================================
-- TABLA: PRODUCTOS
-- =========================================================

CREATE TABLE IF NOT EXISTS productos (

    id_producto INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(80) NOT NULL,

    id_categoria INT NOT NULL,

    descripcion VARCHAR(250) NOT NULL,

    stock INT NOT NULL DEFAULT 0,

    CONSTRAINT fk_producto_categoria

        FOREIGN KEY (id_categoria)

        REFERENCES categorias(id_categoria)

        ON UPDATE CASCADE

        ON DELETE RESTRICT

);


-- =========================================================
-- TABLA: CLIENTES
-- =========================================================

CREATE TABLE IF NOT EXISTS clientes (

    id_cliente INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    correo VARCHAR(120) NOT NULL,

    telefono VARCHAR(25) NOT NULL,

    ciudad VARCHAR(80) NOT NULL,

    activo BOOLEAN NOT NULL DEFAULT TRUE

);


-- =========================================================
-- TABLA: PROVEEDORES
-- =========================================================

CREATE TABLE IF NOT EXISTS proveedores (

    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    productos VARCHAR(200) NOT NULL,

    contacto VARCHAR(25) NOT NULL,

    ciudad VARCHAR(80) NOT NULL,

    activo BOOLEAN NOT NULL DEFAULT TRUE

);


-- =========================================================
-- TABLA: FACTURAS
-- =========================================================
--
-- Cada factura pertenece a un cliente.
-- =========================================================

CREATE TABLE IF NOT EXISTS facturas (

    id_factura INT AUTO_INCREMENT PRIMARY KEY,

    numero VARCHAR(30) NOT NULL UNIQUE,

    fecha DATE NOT NULL,

    id_cliente INT NOT NULL,

    forma_pago VARCHAR(50) NOT NULL,

    pagada BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_factura_cliente

        FOREIGN KEY (id_cliente)

        REFERENCES clientes(id_cliente)

        ON UPDATE CASCADE

        ON DELETE RESTRICT

);


-- =========================================================
-- TABLA: DETALLE_FACTURA
-- =========================================================
--
-- Relaciona las facturas con los productos vendidos.
-- =========================================================

CREATE TABLE IF NOT EXISTS detalle_factura (

    id_detalle INT AUTO_INCREMENT PRIMARY KEY,

    id_factura INT NOT NULL,

    id_producto INT NOT NULL,

    cantidad INT NOT NULL,

    precio_unitario DECIMAL(10, 2) NOT NULL,

    CONSTRAINT fk_detalle_factura

        FOREIGN KEY (id_factura)

        REFERENCES facturas(id_factura)

        ON UPDATE CASCADE

        ON DELETE CASCADE,

    CONSTRAINT fk_detalle_producto

        FOREIGN KEY (id_producto)

        REFERENCES productos(id_producto)

        ON UPDATE CASCADE

        ON DELETE RESTRICT

);


-- =========================================================
-- CATEGORÍAS INICIALES
-- =========================================================

INSERT IGNORE INTO categorias (nombre)
VALUES
    ('Fuerza'),
    ('Cardio'),
    ('Movilidad'),
    ('Accesorios'),
    ('Ropa deportiva');


-- =========================================================
-- PRODUCTOS INICIALES
-- =========================================================
--
-- Solo se insertan si todavía no existe un producto
-- con el mismo nombre.
-- =========================================================


-- BANDAS ELÁSTICAS

INSERT INTO productos (
    nombre,
    id_categoria,
    descripcion,
    stock
)

SELECT
    'Bandas elásticas',
    id_categoria,
    'Ideales para ejercicios de fuerza, movilidad y entrenamiento funcional.',
    10

FROM categorias

WHERE nombre = 'Fuerza'

AND NOT EXISTS (
    SELECT 1
    FROM productos
    WHERE nombre = 'Bandas elásticas'
);


-- MANCUERNAS

INSERT INTO productos (
    nombre,
    id_categoria,
    descripcion,
    stock
)

SELECT
    'Mancuernas',
    id_categoria,
    'Accesorios para entrenar brazos, hombros, espalda y piernas.',
    8

FROM categorias

WHERE nombre = 'Fuerza'

AND NOT EXISTS (
    SELECT 1
    FROM productos
    WHERE nombre = 'Mancuernas'
);


-- COLCHONETAS

INSERT INTO productos (
    nombre,
    id_categoria,
    descripcion,
    stock
)

SELECT
    'Colchonetas',
    id_categoria,
    'Recomendadas para yoga, abdominales y estiramientos.',
    0

FROM categorias

WHERE nombre = 'Movilidad'

AND NOT EXISTS (
    SELECT 1
    FROM productos
    WHERE nombre = 'Colchonetas'
);


-- BOTELLAS DEPORTIVAS

INSERT INTO productos (
    nombre,
    id_categoria,
    descripcion,
    stock
)

SELECT
    'Botellas deportivas',
    id_categoria,
    'Útiles para mantener una correcta hidratación durante el entrenamiento.',
    15

FROM categorias

WHERE nombre = 'Accesorios'

AND NOT EXISTS (
    SELECT 1
    FROM productos
    WHERE nombre = 'Botellas deportivas'
);


-- GUANTES DE GIMNASIO

INSERT INTO productos (
    nombre,
    id_categoria,
    descripcion,
    stock
)

SELECT
    'Guantes de gimnasio',
    id_categoria,
    'Brindan comodidad y protección durante ejercicios con peso.',
    6

FROM categorias

WHERE nombre = 'Accesorios'

AND NOT EXISTS (
    SELECT 1
    FROM productos
    WHERE nombre = 'Guantes de gimnasio'
);


-- ROPA DEPORTIVA

INSERT INTO productos (
    nombre,
    id_categoria,
    descripcion,
    stock
)

SELECT
    'Ropa deportiva',
    id_categoria,
    'Prendas cómodas para entrenamientos en casa, gimnasio o al aire libre.',
    0

FROM categorias

WHERE nombre = 'Ropa deportiva'

AND NOT EXISTS (
    SELECT 1
    FROM productos
    WHERE nombre = 'Ropa deportiva'
);


-- =========================================================
-- CONSULTAS DE COMPROBACIÓN
-- =========================================================


-- VERIFICAR TABLAS

SHOW TABLES;


-- VERIFICAR CATEGORÍAS

SELECT *
FROM categorias;


-- =========================================================
-- CONSULTA RELACIONADA MEDIANTE JOIN
-- =========================================================
--
-- Esta consulta será utilizada también desde Flask.
-- Demuestra la relación entre productos y categorías.
-- =========================================================

SELECT

    p.id_producto AS id,

    p.nombre,

    c.nombre AS categoria,

    p.descripcion,

    p.stock

FROM productos AS p

INNER JOIN categorias AS c
    ON p.id_categoria = c.id_categoria

ORDER BY p.id_producto ASC;