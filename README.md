# FitZone Store

Proyecto final de la asignatura Desarrollo de Aplicaciones Web.

## Descripción

FitZone Store es una aplicación web desarrollada con Flask para la gestión de productos, clientes, proveedores y facturación.

El sistema permite administrar información mediante operaciones CRUD y cuenta con autenticación de usuarios y rutas protegidas.

## Funcionalidades

- Inicio de sesión y autenticación de usuarios.
- Rutas protegidas mediante Flask-Login.
- Gestión de productos.
- Gestión de clientes.
- Gestión de proveedores.
- Gestión de facturación.
- Operaciones CRUD: Crear, Leer, Actualizar y Eliminar.
- Relación entre clientes, productos, facturas y detalle de factura.
- Actualización automática del stock al registrar, modificar o eliminar una factura.
- Conexión a base de datos PostgreSQL.

## Tecnologías utilizadas

- Python
- Flask
- Flask-WTF
- Flask-Login
- PostgreSQL
- HTML
- CSS
- Bootstrap
- JavaScript

## Estructura principal

- `app.py`: aplicación principal y rutas.
- `forms/`: formularios del sistema.
- `templates/`: plantillas HTML.
- `static/`: archivos CSS, JavaScript e imágenes.
- `conexion/`: configuración de conexión a la base de datos.
- `sql/`: script de creación de la base de datos.
- `requirements.txt`: dependencias del proyecto.

## Ejecución local

1. Crear y activar un entorno virtual.
2. Instalar las dependencias:

```bash
pip install -r requirements.txt