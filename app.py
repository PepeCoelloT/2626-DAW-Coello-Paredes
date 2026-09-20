import os

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from mysql.connector import Error

from conexion.conexion import obtener_conexion

from models import Usuario

from forms import (
    ProductoForm,
    ClienteForm,
    ProveedorForm,
    FacturacionForm
)

from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm


# =========================================================
# APLICACIÓN FLASK
# =========================================================

app = Flask(__name__)


# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY"
)

if not app.config["SECRET_KEY"]:

    raise RuntimeError(
        "Debe definir la variable de entorno SECRET_KEY."
    )


# =========================================================
# CONFIGURACIÓN MYSQL
# SEMANA 14
# =========================================================

app.config["MYSQL_HOST"] = "localhost"

app.config["MYSQL_PORT"] = 3306

app.config["MYSQL_USER"] = "root"

app.config["MYSQL_PASSWORD"] = os.getenv(
    "MYSQL_PASSWORD"
)

app.config["MYSQL_DATABASE"] = "fitness_zone"


# =========================================================
# CONFIGURACIÓN FLASK-LOGIN
# =========================================================

login_manager = LoginManager()

login_manager.init_app(
    app
)

login_manager.login_view = "login"

login_manager.login_message = (
    "Debe iniciar sesión para acceder a esta página."
)

login_manager.login_message_category = "warning"


# =========================================================
# COMPROBACIÓN DE CONEXIÓN MYSQL
# =========================================================

def comprobar_conexion_mysql():

    conexion = None
    cursor = None

    try:

        conexion = obtener_conexion()

        cursor = conexion.cursor()

        cursor.execute(
            "SELECT 1"
        )

        cursor.fetchone()

        print(
            "Conexión MySQL establecida correctamente."
        )

    except Error as error:

        print(
            "Error al conectar con MySQL:",
            error
        )

    finally:

        if cursor is not None:

            cursor.close()

        if (
            conexion is not None
            and conexion.is_connected()
        ):

            conexion.close()


# =========================================================
# DATOS TEMPORALES DE LOS DEMÁS MÓDULOS
# =========================================================
#
# La actividad exige como mínimo un módulo completamente
# conectado a MySQL.
#
# El módulo PRODUCTOS implementa
# SELECT, INSERT, UPDATE y DELETE sobre MySQL.
#
# Clientes, Proveedores y Facturación mantienen por ahora
# la lógica desarrollada anteriormente.
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


contador_facturas = 3


# =========================================================
# AUTENTICACIÓN DE USUARIOS
# SEMANA 14
# =========================================================


# ---------------------------------------------------------
# CARGAR USUARIO PARA FLASK-LOGIN
# ---------------------------------------------------------

@login_manager.user_loader
def load_user(user_id):

    conexion = None
    cursor = None

    try:

        id_usuario = int(
            user_id
        )

        conexion = obtener_conexion()

        cursor = conexion.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                id,
                usuario,
                password

            FROM usuarios

            WHERE id = %s
            """,
            (
                id_usuario,
            )
        )

        registro = cursor.fetchone()

        if registro is None:

            return None

        return Usuario(
            registro["id"],
            registro["usuario"],
            registro["password"]
        )

    except (
        ValueError,
        TypeError,
        Error
    ):

        return None

    finally:

        if cursor is not None:

            cursor.close()

        if (
            conexion is not None
            and conexion.is_connected()
        ):

            conexion.close()


# ---------------------------------------------------------
# REGISTRAR USUARIO
# ---------------------------------------------------------

@app.route(
    "/registro",
    methods=["GET", "POST"]
)
def registro():

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )

    form = UsuarioForm()

    if form.validate_on_submit():

        conexion = None
        cursor = None

        try:

            nombre_usuario = (
                form.usuario.data.strip()
            )

            conexion = obtener_conexion()

            cursor = conexion.cursor(
                dictionary=True
            )

            # ---------------------------------------------
            # COMPROBAR QUE EL USUARIO NO EXISTA
            # ---------------------------------------------

            cursor.execute(
                """
                SELECT id

                FROM usuarios

                WHERE usuario = %s
                """,
                (
                    nombre_usuario,
                )
            )

            usuario_existente = cursor.fetchone()

            if usuario_existente is not None:

                flash(
                    "El nombre de usuario ya está registrado.",
                    "warning"
                )

                return render_template(
                    "registro.html",
                    form=form
                )

            # ---------------------------------------------
            # GENERAR HASH DE LA CONTRASEÑA
            # ---------------------------------------------

            password_hash = generate_password_hash(
                form.password.data
            )

            # ---------------------------------------------
            # INSERT PARAMETRIZADO
            # ---------------------------------------------

            cursor.execute(
                """
                INSERT INTO usuarios (
                    usuario,
                    password
                )

                VALUES (
                    %s,
                    %s
                )
                """,
                (
                    nombre_usuario,
                    password_hash
                )
            )

            conexion.commit()

            flash(
                "Usuario registrado correctamente. "
                "Ahora puede iniciar sesión.",
                "success"
            )

            return redirect(
                url_for("login")
            )

        except Error as error:

            if conexion is not None:

                conexion.rollback()

            flash(
                f"Error al registrar el usuario: {error}",
                "danger"
            )

        finally:

            if cursor is not None:

                cursor.close()

            if (
                conexion is not None
                and conexion.is_connected()
            ):

                conexion.close()

    return render_template(
        "registro.html",
        form=form
    )


# ---------------------------------------------------------
# INICIAR SESIÓN
# ---------------------------------------------------------

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )

    form = LoginForm()

    if form.validate_on_submit():

        conexion = None
        cursor = None

        try:

            nombre_usuario = (
                form.usuario.data.strip()
            )

            conexion = obtener_conexion()

            cursor = conexion.cursor(
                dictionary=True
            )

            # ---------------------------------------------
            # BUSCAR USUARIO
            # ---------------------------------------------

            cursor.execute(
                """
                SELECT
                    id,
                    usuario,
                    password

                FROM usuarios

                WHERE usuario = %s
                """,
                (
                    nombre_usuario,
                )
            )

            registro = cursor.fetchone()

            # ---------------------------------------------
            # COMPROBAR CONTRASEÑA MEDIANTE HASH
            # ---------------------------------------------

            if (
                registro is None
                or not check_password_hash(
                    registro["password"],
                    form.password.data
                )
            ):

                flash(
                    "Usuario o contraseña incorrectos.",
                    "danger"
                )

                return render_template(
                    "login.html",
                    form=form
                )

            usuario = Usuario(
                registro["id"],
                registro["usuario"],
                registro["password"]
            )

            login_user(
                usuario
            )

            flash(
                f"Bienvenido, {current_user.usuario}.",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        except Error as error:

            flash(
                f"Error al iniciar sesión: {error}",
                "danger"
            )

        finally:

            if cursor is not None:

                cursor.close()

            if (
                conexion is not None
                and conexion.is_connected()
            ):

                conexion.close()

    return render_template(
        "login.html",
        form=form
    )


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        usuario=current_user.usuario
    )


# ---------------------------------------------------------
# CERRAR SESIÓN
# ---------------------------------------------------------

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(
        url_for("login")
    )


# =========================================================
# RUTAS GENERALES
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
# MYSQL - CRUD COMPLETO
# =========================================================


# ---------------------------------------------------------
# LISTAR PRODUCTOS
# SELECT + JOIN + FETCHALL
# ---------------------------------------------------------

@app.route("/productos")
@login_required
def productos():

    titulo = "Gestión de Productos"

    conexion = None
    cursor = None

    lista_productos = []

    try:

        conexion = obtener_conexion()

        cursor = conexion.cursor(
            dictionary=True
        )


        # -------------------------------------------------
        # CONSULTA RELACIONADA
        # PRODUCTOS + CATEGORIAS
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT

                p.id_producto AS id,

                p.nombre,

                c.nombre AS categoria,

                p.descripcion,

                p.stock

            FROM productos AS p

            INNER JOIN categorias AS c
                ON p.id_categoria = c.id_categoria

            ORDER BY p.id_producto ASC
            """
        )


        # Recuperación de varios registros.
        lista_productos = cursor.fetchall()


    except Error as error:

        flash(
            f"Error al consultar los productos: {error}",
            "danger"
        )


    finally:

        if cursor is not None:

            cursor.close()

        if (
            conexion is not None
            and conexion.is_connected()
        ):

            conexion.close()


    # -----------------------------------------------------
    # RESUMEN
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


    return render_template(
        "productos.html",
        titulo=titulo,
        productos=lista_productos,
        disponibles=disponibles,
        agotados=agotados
    )


# ---------------------------------------------------------
# REGISTRAR PRODUCTO
# INSERT INTO + COMMIT
# ---------------------------------------------------------

@app.route(
    "/productos/nuevo",
    methods=["GET", "POST"]
)
@login_required
def registrar_producto():

    form = ProductoForm()


    if form.validate_on_submit():

        conexion = None
        cursor = None

        try:

            conexion = obtener_conexion()

            cursor = conexion.cursor(
                dictionary=True
            )


            # ---------------------------------------------
            # BUSCAR CATEGORÍA
            # SELECT + WHERE
            # ---------------------------------------------

            cursor.execute(
                """
                SELECT id_categoria

                FROM categorias

                WHERE nombre = %s
                """,
                (
                    form.categoria.data,
                )
            )


            categoria = cursor.fetchone()


            if categoria is None:

                flash(
                    "La categoría seleccionada no existe.",
                    "danger"
                )

                return render_template(
                    "formulario_producto.html",
                    form=form,
                    modo="registrar"
                )


            # ---------------------------------------------
            # INSERT
            # ---------------------------------------------

            cursor.execute(
                """
                INSERT INTO productos (
                    nombre,
                    id_categoria,
                    descripcion,
                    stock
                )

                VALUES (
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    form.nombre.data,
                    categoria["id_categoria"],
                    form.descripcion.data,
                    form.stock.data
                )
            )


            conexion.commit()


            flash(
                "Producto registrado correctamente.",
                "success"
            )


            return redirect(
                url_for("productos")
            )


        except Error as error:

            if conexion is not None:

                conexion.rollback()

            flash(
                f"Error al registrar el producto: {error}",
                "danger"
            )


        finally:

            if cursor is not None:

                cursor.close()

            if (
                conexion is not None
                and conexion.is_connected()
            ):

                conexion.close()


    return render_template(
        "formulario_producto.html",
        form=form,
        modo="registrar"
    )


# ---------------------------------------------------------
# MODIFICAR PRODUCTO
# SELECT WHERE + UPDATE WHERE + COMMIT
# ---------------------------------------------------------

@app.route(
    "/productos/editar/<int:id_producto>",
    methods=["GET", "POST"]
)
@login_required
def editar_producto(id_producto):

    conexion = None
    cursor = None

    producto = None


    # -----------------------------------------------------
    # RECUPERAR REGISTRO ACTUAL
    # -----------------------------------------------------

    try:

        conexion = obtener_conexion()

        cursor = conexion.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT

                p.id_producto AS id,

                p.nombre,

                c.nombre AS categoria,

                p.descripcion,

                p.stock

            FROM productos AS p

            INNER JOIN categorias AS c
                ON p.id_categoria = c.id_categoria

            WHERE p.id_producto = %s
            """,
            (
                id_producto,
            )
        )


        producto = cursor.fetchone()


    except Error as error:

        flash(
            f"Error al consultar el producto: {error}",
            "danger"
        )


    finally:

        if cursor is not None:

            cursor.close()

        if (
            conexion is not None
            and conexion.is_connected()
        ):

            conexion.close()


    if producto is None:

        flash(
            "El producto seleccionado no existe.",
            "warning"
        )

        return redirect(
            url_for("productos")
        )


    form = ProductoForm()


    # -----------------------------------------------------
    # GUARDAR MODIFICACIÓN
    # -----------------------------------------------------

    if form.validate_on_submit():

        conexion = None
        cursor = None

        try:

            conexion = obtener_conexion()

            cursor = conexion.cursor(
                dictionary=True
            )


            # ---------------------------------------------
            # OBTENER ID DE CATEGORÍA
            # ---------------------------------------------

            cursor.execute(
                """
                SELECT id_categoria

                FROM categorias

                WHERE nombre = %s
                """,
                (
                    form.categoria.data,
                )
            )


            categoria = cursor.fetchone()


            if categoria is None:

                flash(
                    "La categoría seleccionada no existe.",
                    "danger"
                )

                return render_template(
                    "formulario_producto.html",
                    form=form,
                    modo="editar"
                )


            # ---------------------------------------------
            # UPDATE
            # ---------------------------------------------

            cursor.execute(
                """
                UPDATE productos

                SET
                    nombre = %s,
                    id_categoria = %s,
                    descripcion = %s,
                    stock = %s

                WHERE id_producto = %s
                """,
                (
                    form.nombre.data,
                    categoria["id_categoria"],
                    form.descripcion.data,
                    form.stock.data,
                    id_producto
                )
            )


            conexion.commit()


            flash(
                "Producto modificado correctamente.",
                "success"
            )


            return redirect(
                url_for("productos")
            )


        except Error as error:

            if conexion is not None:

                conexion.rollback()


            flash(
                f"Error al modificar el producto: {error}",
                "danger"
            )


        finally:

            if cursor is not None:

                cursor.close()

            if (
                conexion is not None
                and conexion.is_connected()
            ):

                conexion.close()


    # -----------------------------------------------------
    # PRECARGAR DATOS DEL PRODUCTO
    # SOLO EN GET
    # -----------------------------------------------------

    if request.method == "GET":

        form.nombre.data = producto["nombre"]

        form.categoria.data = producto["categoria"]

        form.descripcion.data = producto["descripcion"]

        form.stock.data = producto["stock"]


    return render_template(
        "formulario_producto.html",
        form=form,
        modo="editar"
    )


# ---------------------------------------------------------
# ELIMINAR PRODUCTO
# DELETE WHERE + COMMIT
# ---------------------------------------------------------

@app.route(
    "/productos/eliminar/<int:id_producto>",
    methods=["POST"]
)
@login_required
def eliminar_producto(id_producto):

    conexion = None
    cursor = None

    try:

        conexion = obtener_conexion()

        cursor = conexion.cursor()


        cursor.execute(
            """
            DELETE FROM productos

            WHERE id_producto = %s
            """,
            (
                id_producto,
            )
        )


        conexion.commit()


        if cursor.rowcount > 0:

            flash(
                "Producto eliminado correctamente.",
                "success"
            )

        else:

            flash(
                "El producto seleccionado no existe.",
                "warning"
            )


    except Error as error:

        if conexion is not None:

            conexion.rollback()


        flash(
            f"No fue posible eliminar el producto: {error}",
            "danger"
        )


    finally:

        if cursor is not None:

            cursor.close()

        if (
            conexion is not None
            and conexion.is_connected()
        ):

            conexion.close()


    return redirect(
        url_for("productos")
    )


# =========================================================
# CLIENTES
# =========================================================


@app.route("/clientes")
@login_required
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
@login_required
def registrar_cliente():

    form = ClienteForm()


    if form.validate_on_submit():

        nuevo_cliente = {

            "nombre":
                form.nombre.data,

            "correo":
                form.correo.data,

            "telefono":
                form.telefono.data,

            "ciudad":
                form.ciudad.data,

            "activo":
                form.activo.data
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


@app.route("/proveedores")
@login_required
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
@login_required
def registrar_proveedor():

    form = ProveedorForm()


    if form.validate_on_submit():

        nuevo_proveedor = {

            "nombre":
                form.nombre.data,

            "productos":
                form.productos.data,

            "contacto":
                form.contacto.data,

            "ciudad":
                form.ciudad.data,

            "activo":
                form.activo.data
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


@app.route("/facturacion")
@login_required
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
@login_required
def registrar_facturacion():

    global factura_actual
    global contador_facturas


    form = FacturacionForm()


    if form.validate_on_submit():

        factura_actual = {

            "numero":
                form.numero.data,

            "fecha":
                form.fecha.data.strftime(
                    "%d/%m/%Y"
                ),

            "cliente": {

                "nombre":
                    form.cliente_nombre.data,

                "correo":
                    form.cliente_correo.data,

                "telefono":
                    form.cliente_telefono.data
            },

            "forma_pago":
                form.forma_pago.data,

            "pagada":
                form.pagada.data,

            "detalle": [
                {
                    "producto":
                        form.producto.data,

                    "cantidad":
                        form.cantidad.data,

                    "precio":
                        float(
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

    with app.app_context():

        comprobar_conexion_mysql()


    app.run(
        debug=True
    )