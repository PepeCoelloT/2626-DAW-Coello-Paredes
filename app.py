import os
import sqlite3

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash
)

from forms import (
    ProductoForm,
    ClienteForm,
    ProveedorForm,
    FacturacionForm
)


app = Flask(__name__)


# =========================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# =========================================================

# Clave necesaria para la protección CSRF de Flask-WTF.
# Se mantiene la configuración desarrollada en la Semana 11.
app.config["SECRET_KEY"] = "fitzone-store-semana11-2026"


# =========================================================
# BASE DE DATOS SQLITE
# SEMANA 12 - PERSISTENCIA LOCAL
# =========================================================

# Ruta absoluta del directorio principal del proyecto.
BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

# Carpeta destinada al almacenamiento local.
DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

# Se crea la carpeta data si todavía no existe.
os.makedirs(
    DATA_DIR,
    exist_ok=True
)

# Nombre solicitado en la actividad de Semana 12.
DATABASE = os.path.join(
    DATA_DIR,
    "ferreteria.db"
)


# ---------------------------------------------------------
# CONEXIÓN A SQLITE
# ---------------------------------------------------------

def obtener_conexion():

    conn = sqlite3.connect(
        DATABASE
    )

    # Permite acceder a las columnas utilizando su nombre.
    # Ejemplo:
    # producto["nombre"]
    conn.row_factory = sqlite3.Row

    return conn


# ---------------------------------------------------------
# INICIALIZACIÓN DE LA BASE DE DATOS
# ---------------------------------------------------------

def inicializar_base_datos():

    conn = obtener_conexion()

    cursor = conn.cursor()

    # -----------------------------------------------------
    # TABLA PRODUCTOS
    # -----------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            stock INTEGER NOT NULL
        )
        """
    )


    # -----------------------------------------------------
    # PRODUCTOS INICIALES DEL PROYECTO
    # -----------------------------------------------------
    #
    # Estos registros corresponden a los productos que ya
    # existían durante la Semana 11.
    #
    # Solamente se insertan cuando la tabla se encuentra
    # completamente vacía.
    #
    # Después de esta inicialización, SQLite constituye el
    # mecanismo principal de almacenamiento del módulo.
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM productos
        """
    )

    cantidad_productos = cursor.fetchone()[0]

    if cantidad_productos == 0:

        productos_iniciales = [
            (
                "Bandas elásticas",
                "Fuerza",
                "Ideales para ejercicios de fuerza, movilidad y entrenamiento funcional.",
                10
            ),
            (
                "Mancuernas",
                "Fuerza",
                "Accesorios para entrenar brazos, hombros, espalda y piernas.",
                8
            ),
            (
                "Colchonetas",
                "Movilidad",
                "Recomendadas para yoga, abdominales y estiramientos.",
                0
            ),
            (
                "Botellas deportivas",
                "Accesorios",
                "Útiles para mantener una correcta hidratación durante el entrenamiento.",
                15
            ),
            (
                "Guantes de gimnasio",
                "Accesorios",
                "Brindan comodidad y protección durante ejercicios con peso.",
                6
            ),
            (
                "Ropa deportiva",
                "Ropa deportiva",
                "Prendas cómodas para entrenamientos en casa, gimnasio o al aire libre.",
                0
            )
        ]

        cursor.executemany(
            """
            INSERT INTO productos (
                nombre,
                categoria,
                descripcion,
                stock
            )
            VALUES (?, ?, ?, ?)
            """,
            productos_iniciales
        )

    # Guarda definitivamente los cambios realizados.
    conn.commit()

    # Cierra correctamente la conexión.
    conn.close()


# =========================================================
# DATOS TEMPORALES DE LOS DEMÁS MÓDULOS
# =========================================================
#
# Durante la Semana 12 la persistencia obligatoria se
# implementa en el módulo de productos.
#
# Clientes, proveedores y facturación conservan por ahora
# la lógica desarrollada durante la Semana 11.
# =========================================================


# ---------------------------------------------------------
# CLIENTES
# ---------------------------------------------------------

lista_clientes = [
    {
        "nombre": "María López",
        "correo": "maria.lopez@email.com",
        "telefono": "098 456 7821",
        "ciudad": "Puyo",
        "activo": True
    },
    {
        "nombre": "Carlos Pérez",
        "correo": "carlos.perez@email.com",
        "telefono": "099 785 4123",
        "ciudad": "Quito",
        "activo": True
    },
    {
        "nombre": "Andrea Torres",
        "correo": "andrea.torres@email.com",
        "telefono": "097 654 3218",
        "ciudad": "Ambato",
        "activo": True
    },
    {
        "nombre": "Diego Sánchez",
        "correo": "diego.sanchez@email.com",
        "telefono": "096 421 7852",
        "ciudad": "Guayaquil",
        "activo": False
    },
    {
        "nombre": "Sofía Ramírez",
        "correo": "sofia.ramirez@email.com",
        "telefono": "095 874 6321",
        "ciudad": "Cuenca",
        "activo": True
    }
]


# ---------------------------------------------------------
# PROVEEDORES
# ---------------------------------------------------------

lista_proveedores = [
    {
        "nombre": "SportFit Ecuador",
        "productos": "Mancuernas y accesorios de fuerza",
        "contacto": "098 234 5678",
        "ciudad": "Quito",
        "activo": True
    },
    {
        "nombre": "ActiveGear",
        "productos": "Ropa deportiva y guantes",
        "contacto": "099 876 5432",
        "ciudad": "Guayaquil",
        "activo": True
    },
    {
        "nombre": "Fitness Supply",
        "productos": "Bandas elásticas y colchonetas",
        "contacto": "097 345 6789",
        "ciudad": "Cuenca",
        "activo": True
    },
    {
        "nombre": "Hydration Sport",
        "productos": "Botellas deportivas",
        "contacto": "096 567 4321",
        "ciudad": "Ambato",
        "activo": False
    }
]


# ---------------------------------------------------------
# FACTURACIÓN
# ---------------------------------------------------------

factura_actual = {
    "numero": "FZ-001-0003",
    "fecha": "13/08/2026",

    "cliente": {
        "nombre": "María López",
        "correo": "maria.lopez@email.com",
        "telefono": "098 456 7821"
    },

    "forma_pago": "Tarjeta",
    "pagada": True,

    "detalle": [
        {
            "producto": "Mancuernas",
            "cantidad": 1,
            "precio": 35.00
        },
        {
            "producto": "Bandas elásticas",
            "cantidad": 2,
            "precio": 20.00
        },
        {
            "producto": "Botella deportiva",
            "cantidad": 1,
            "precio": 12.00
        }
    ]
}


# Cantidad demostrativa inicial de facturas registradas.
contador_facturas = 3


# =========================================================
# RUTAS
# =========================================================


# ---------------------------------------------------------
# INICIO
# ---------------------------------------------------------

@app.route("/")
def inicio():

    return render_template(
        "index.html"
    )


# =========================================================
# PRODUCTOS
# SEMANA 12 - SQLITE
# =========================================================


# ---------------------------------------------------------
# LISTADO DE PRODUCTOS
# SELECT + FETCHALL
# ---------------------------------------------------------

@app.route("/productos")
def productos():

    titulo = "Gestión de Productos"

    # Se establece una conexión con SQLite.
    conn = obtener_conexion()

    cursor = conn.cursor()

    # Se recuperan todos los productos almacenados
    # persistentemente en la base de datos.
    cursor.execute(
        """
        SELECT
            id,
            nombre,
            categoria,
            descripcion,
            stock
        FROM productos
        ORDER BY id ASC
        """
    )

    # La actividad solicita utilizar fetchall().
    lista_productos = cursor.fetchall()

    # Se cierra la conexión después de recuperar los datos.
    conn.close()


    # -----------------------------------------------------
    # RESUMEN DE PRODUCTOS
    # -----------------------------------------------------

    disponibles = sum(
        1
        for producto in lista_productos
        if producto["stock"] > 0
    )

    agotados = sum(
        1
        for producto in lista_productos
        if producto["stock"] == 0
    )


    # Los registros recuperados desde SQLite se envían
    # hacia la plantilla productos.html.
    return render_template(
        "productos.html",
        titulo=titulo,
        productos=lista_productos,
        disponibles=disponibles,
        agotados=agotados
    )


# ---------------------------------------------------------
# REGISTRAR PRODUCTO
# VALIDACIÓN + INSERT
# ---------------------------------------------------------

@app.route(
    "/productos/nuevo",
    methods=["GET", "POST"]
)
def registrar_producto():

    form = ProductoForm()

    # Solamente se almacena información cuando todas
    # las reglas de validación de WTForms se cumplen.
    if form.validate_on_submit():

        conn = obtener_conexion()

        cursor = conn.cursor()

        # Consulta SQL parametrizada.
        #
        # Se utilizan signos ? para evitar concatenar
        # directamente los datos recibidos del usuario.
        cursor.execute(
            """
            INSERT INTO productos (
                nombre,
                categoria,
                descripcion,
                stock
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                form.nombre.data,
                form.categoria.data,
                form.descripcion.data,
                form.stock.data
            )
        )

        # Confirma el INSERT y almacena el registro
        # permanentemente en ferreteria.db.
        conn.commit()

        # Cierra correctamente la conexión.
        conn.close()

        flash(
            "Producto registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("productos")
        )

    return render_template(
        "formulario_producto.html",
        form=form
    )


# =========================================================
# CLIENTES
# =========================================================


# ---------------------------------------------------------
# LISTADO DE CLIENTES
# ---------------------------------------------------------

@app.route("/clientes")
def clientes():

    titulo = "Gestión de Clientes"

    activos = sum(
        1
        for cliente in lista_clientes
        if cliente["activo"]
    )

    inactivos = sum(
        1
        for cliente in lista_clientes
        if not cliente["activo"]
    )

    return render_template(
        "clientes.html",
        titulo=titulo,
        clientes=lista_clientes,
        activos=activos,
        inactivos=inactivos
    )


# ---------------------------------------------------------
# REGISTRAR CLIENTE
# ---------------------------------------------------------

@app.route(
    "/clientes/nuevo",
    methods=["GET", "POST"]
)
def registrar_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        nuevo_cliente = {
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data,
            "ciudad": form.ciudad.data,
            "activo": form.activo.data
        }

        lista_clientes.append(
            nuevo_cliente
        )

        flash(
            "Cliente registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("clientes")
        )

    return render_template(
        "formulario_cliente.html",
        form=form
    )


# =========================================================
# PROVEEDORES
# =========================================================


# ---------------------------------------------------------
# LISTADO DE PROVEEDORES
# ---------------------------------------------------------

@app.route("/proveedores")
def proveedores():

    titulo = "Gestión de Proveedores"

    activos = sum(
        1
        for proveedor in lista_proveedores
        if proveedor["activo"]
    )

    inactivos = sum(
        1
        for proveedor in lista_proveedores
        if not proveedor["activo"]
    )

    return render_template(
        "proveedores.html",
        titulo=titulo,
        proveedores=lista_proveedores,
        activos=activos,
        inactivos=inactivos
    )


# ---------------------------------------------------------
# REGISTRAR PROVEEDOR
# ---------------------------------------------------------

@app.route(
    "/proveedores/nuevo",
    methods=["GET", "POST"]
)
def registrar_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        nuevo_proveedor = {
            "nombre": form.nombre.data,
            "productos": form.productos.data,
            "contacto": form.contacto.data,
            "ciudad": form.ciudad.data,
            "activo": form.activo.data
        }

        lista_proveedores.append(
            nuevo_proveedor
        )

        flash(
            "Proveedor registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("proveedores")
        )

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# =========================================================
# FACTURACIÓN
# =========================================================


# ---------------------------------------------------------
# VISUALIZAR FACTURA ACTUAL
# ---------------------------------------------------------

@app.route("/facturacion")
def facturacion():

    titulo = "Gestión de Facturación"

    subtotal = sum(
        item["cantidad"] * item["precio"]
        for item in factura_actual["detalle"]
    )

    iva = subtotal * 0.15

    total = subtotal + iva

    productos_vendidos = sum(
        item["cantidad"]
        for item in factura_actual["detalle"]
    )

    return render_template(
        "facturacion.html",
        titulo=titulo,
        factura=factura_actual,
        subtotal=subtotal,
        iva=iva,
        total=total,
        productos_vendidos=productos_vendidos,
        facturas_registradas=contador_facturas
    )


# ---------------------------------------------------------
# REGISTRAR FACTURA
# ---------------------------------------------------------

@app.route(
    "/facturacion/nueva",
    methods=["GET", "POST"]
)
def registrar_facturacion():

    global factura_actual
    global contador_facturas

    form = FacturacionForm()

    if form.validate_on_submit():

        factura_actual = {

            "numero": form.numero.data,

            "fecha": form.fecha.data.strftime(
                "%d/%m/%Y"
            ),

            "cliente": {
                "nombre": form.cliente_nombre.data,
                "correo": form.cliente_correo.data,
                "telefono": form.cliente_telefono.data
            },

            "forma_pago": form.forma_pago.data,

            "pagada": form.pagada.data,

            "detalle": [
                {
                    "producto": form.producto.data,
                    "cantidad": form.cantidad.data,
                    "precio": float(
                        form.precio.data
                    )
                }
            ]
        }

        contador_facturas += 1

        flash(
            "Factura registrada correctamente.",
            "success"
        )

        return redirect(
            url_for("facturacion")
        )

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# =========================================================
# EJECUCIÓN
# =========================================================

if __name__ == "__main__":

    # Antes de iniciar Flask se comprueba la existencia
    # de la base de datos y de la tabla productos.
    inicializar_base_datos()

    app.run(
        debug=True
    )