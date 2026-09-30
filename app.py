import os
from decimal import Decimal

import psycopg

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

from flask_wtf.csrf import CSRFProtect

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

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

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError(
        "Debe definir la variable de entorno SECRET_KEY."
    )

if not os.getenv("DATABASE_URL"):
    raise RuntimeError(
        "Debe definir la variable de entorno DATABASE_URL."
    )


# =========================================================
# PROTECCIÓN CSRF
# =========================================================

csrf = CSRFProtect(app)


# =========================================================
# FLASK-LOGIN
# =========================================================

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"

login_manager.login_message = (
    "Debe iniciar sesión para acceder a esta página."
)

login_manager.login_message_category = "warning"


# =========================================================
# COMPROBAR CONEXIÓN POSTGRESQL
# =========================================================

def comprobar_conexion_postgresql():

    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                cursor.execute("SELECT 1")
                cursor.fetchone()

        print("CONEXION POSTGRESQL CORRECTA")

    except psycopg.Error as error:

        print(
            "Error al conectar con PostgreSQL:",
            error
        )


# =========================================================
# CARGAR USUARIO
# =========================================================

@login_manager.user_loader
def cargar_usuario(user_id):

    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        usuario,
                        password
                    FROM usuarios
                    WHERE id = %s
                    """,
                    (int(user_id),)
                )

                registro = cursor.fetchone()

        if registro is None:
            return None

        return Usuario(
            registro["id"],
            registro["usuario"],
            registro["password"]
        )

    except (psycopg.Error, ValueError, TypeError):

        return None


# =========================================================
# INICIO
# =========================================================

@app.route("/")
def inicio():

    return render_template(
        "index.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("panel")
        )

    form = LoginForm()

    if form.validate_on_submit():

        try:

            with obtener_conexion() as conexion:

                with conexion.cursor() as cursor:

                    cursor.execute(
                        """
                        SELECT
                            id,
                            usuario,
                            password
                        FROM usuarios
                        WHERE usuario = %s
                        """,
                        (form.usuario.data,)
                    )

                    registro = cursor.fetchone()

            if (
                registro is not None
                and check_password_hash(
                    registro["password"],
                    form.password.data
                )
            ):

                usuario = Usuario(
                    registro["id"],
                    registro["usuario"],
                    registro["password"]
                )

                login_user(usuario)

                flash(
                    "Inicio de sesión correcto.",
                    "success"
                )

                siguiente = request.args.get("next")

                if siguiente:
                    return redirect(siguiente)

                return redirect(
                    url_for("panel")
                )

            flash(
                "Usuario o contraseña incorrectos.",
                "danger"
            )

        except psycopg.Error as error:

            flash(
                f"Error al iniciar sesión: {error}",
                "danger"
            )

    return render_template(
        "login.html",
        form=form
    )


# =========================================================
# LOGOUT
# =========================================================

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
# REGISTRO DE USUARIO
# =========================================================

@app.route(
    "/registro",
    methods=["GET", "POST"]
)
@app.route(
    "/usuarios/registrar",
    methods=["GET", "POST"]
)
def registrar_usuario():

    form = UsuarioForm()

    if form.validate_on_submit():

        try:

            with obtener_conexion() as conexion:

                with conexion.cursor() as cursor:

                    cursor.execute(
                        """
                        SELECT id
                        FROM usuarios
                        WHERE usuario = %s
                        """,
                        (form.usuario.data,)
                    )

                    existente = cursor.fetchone()

                    if existente is not None:

                        flash(
                            "Ese nombre de usuario ya está registrado.",
                            "warning"
                        )

                        return render_template(
                            "registro.html",
                            form=form
                        )

                    password_hash = generate_password_hash(
                        form.password.data
                    )

                    cursor.execute(
                        """
                        INSERT INTO usuarios (
                            usuario,
                            password
                        )
                        VALUES (%s, %s)
                        """,
                        (
                            form.usuario.data,
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

        except psycopg.Error as error:

            flash(
                f"Error al registrar el usuario: {error}",
                "danger"
            )

    return render_template(
        "registro.html",
        form=form
    )


# =========================================================
# COMPATIBILIDAD CON url_for("registro")
# =========================================================

@app.route(
    "/registro-usuario",
    endpoint="registro"
)
def registro():

    return redirect(
        url_for("registrar_usuario")
    )


# =========================================================
# PANEL
# =========================================================

@app.route("/panel")
@login_required
def panel():

    return render_template(
        "panel.html"
    )


# =========================================================
# PRODUCTOS - SELECT
# =========================================================

@app.route("/productos")
@login_required
def productos():

    lista_productos = []

    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        p.id,
                        p.nombre,
                        p.categoria,
                        p.descripcion,
                        p.stock,
                        p.proveedor_id,
                        pr.nombre AS proveedor_nombre
                    FROM productos AS p
                    LEFT JOIN proveedores AS pr
                        ON p.proveedor_id = pr.id
                    ORDER BY p.id
                    """
                )

                lista_productos = cursor.fetchall()

    except psycopg.Error as error:

        flash(
            f"Error al consultar los productos: {error}",
            "danger"
        )

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
        titulo="Productos",
        productos=lista_productos,
        disponibles=disponibles,
        agotados=agotados
    )

# =========================================================
# PRODUCTOS - INSERT
# =========================================================

@app.route(
    "/productos/nuevo",
    methods=["GET", "POST"]
)
@login_required
def registrar_producto():

    form = ProductoForm()

    # CARGAR PROVEEDORES ACTIVOS DESDE POSTGRESQL
    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre
                    FROM proveedores
                    WHERE activo = TRUE
                    ORDER BY nombre
                    """
                )

                lista_proveedores = cursor.fetchall()

        form.proveedor_id.choices = [
            (
                proveedor["id"],
                proveedor["nombre"]
            )
            for proveedor in lista_proveedores
        ]

    except psycopg.Error as error:

        form.proveedor_id.choices = []

        flash(
            f"Error al cargar los proveedores: {error}",
            "danger"
        )

    # GUARDAR PRODUCTO
    if form.validate_on_submit():

        try:

            with obtener_conexion() as conexion:

                with conexion.cursor() as cursor:

                    cursor.execute(
                        """
                        INSERT INTO productos (
                            nombre,
                            categoria,
                            descripcion,
                            stock,
                            proveedor_id
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            form.nombre.data,
                            form.categoria.data,
                            form.descripcion.data,
                            form.stock.data,
                            form.proveedor_id.data
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

        except psycopg.Error as error:

            flash(
                f"Error al registrar el producto: {error}",
                "danger"
            )

    return render_template(
        "formulario_producto.html",
        form=form,
        modo="registrar"
    )

# =========================================================
# PRODUCTOS - UPDATE
# =========================================================

@app.route(
    "/productos/editar/<int:id_producto>",
    methods=["GET", "POST"]
)
@login_required
def editar_producto(id_producto):

    # BUSCAR EL PRODUCTO
    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre,
                        categoria,
                        descripcion,
                        stock,
                        proveedor_id
                    FROM productos
                    WHERE id = %s
                    """,
                    (id_producto,)
                )

                producto = cursor.fetchone()

    except psycopg.Error as error:

        flash(
            f"Error al consultar el producto: {error}",
            "danger"
        )

        return redirect(
            url_for("productos")
        )

    if producto is None:

        flash(
            "El producto seleccionado no existe.",
            "warning"
        )

        return redirect(
            url_for("productos")
        )

    form = ProductoForm()

    # CARGAR PROVEEDORES ACTIVOS
    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre
                    FROM proveedores
                    WHERE activo = TRUE
                    ORDER BY nombre
                    """
                )

                lista_proveedores = cursor.fetchall()

        form.proveedor_id.choices = [
            (
                proveedor["id"],
                proveedor["nombre"]
            )
            for proveedor in lista_proveedores
        ]

    except psycopg.Error as error:

        form.proveedor_id.choices = []

        flash(
            f"Error al cargar los proveedores: {error}",
            "danger"
        )

    # MODIFICAR PRODUCTO
    if form.validate_on_submit():

        try:

            with obtener_conexion() as conexion:

                with conexion.cursor() as cursor:

                    cursor.execute(
                        """
                        UPDATE productos
                        SET
                            nombre = %s,
                            categoria = %s,
                            descripcion = %s,
                            stock = %s,
                            proveedor_id = %s
                        WHERE id = %s
                        """,
                        (
                            form.nombre.data,
                            form.categoria.data,
                            form.descripcion.data,
                            form.stock.data,
                            form.proveedor_id.data,
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

        except psycopg.Error as error:

            flash(
                f"Error al modificar el producto: {error}",
                "danger"
            )

    # MOSTRAR LOS DATOS ACTUALES
    if request.method == "GET":

        form.nombre.data = producto["nombre"]
        form.categoria.data = producto["categoria"]
        form.descripcion.data = producto["descripcion"]
        form.stock.data = producto["stock"]
        form.proveedor_id.data = producto["proveedor_id"]

    return render_template(
        "formulario_producto.html",
        form=form,
        modo="editar"
    )


# =========================================================
# PRODUCTOS - DELETE
# =========================================================

@app.route(
    "/productos/eliminar/<int:id_producto>",
    methods=["POST"]
)
@login_required
def eliminar_producto(id_producto):

    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    DELETE FROM productos
                    WHERE id = %s
                    """,
                    (id_producto,)
                )

                eliminado = cursor.rowcount

            conexion.commit()

        if eliminado == 0:

            flash(
                "El producto seleccionado no existe.",
                "warning"
            )

        else:

            flash(
                "Producto eliminado correctamente.",
                "success"
            )

    except psycopg.Error as error:

        flash(
            f"No se pudo eliminar el producto: {error}",
            "danger"
        )

    return redirect(
        url_for("productos")
    )


# =========================================================
# CLIENTES - SELECT
# =========================================================

@app.route("/clientes")
@login_required
def clientes():

    lista_clientes = []

    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre,
                        correo,
                        telefono,
                        ciudad,
                        activo
                    FROM clientes
                    ORDER BY id
                    """
                )

                lista_clientes = cursor.fetchall()

    except psycopg.Error as error:

        flash(
            f"Error al consultar los clientes: {error}",
            "danger"
        )

    activos = sum(
        1
        for cliente in lista_clientes
        if cliente["activo"]
    )

    inactivos = len(lista_clientes) - activos

    return render_template(
        "clientes.html",
        titulo="Clientes",
        clientes=lista_clientes,
        activos=activos,
        inactivos=inactivos
    )


# =========================================================
# CLIENTES - INSERT
# =========================================================

@app.route(
    "/clientes/registrar",
    methods=["GET", "POST"]
)
@login_required
def registrar_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        try:

            with obtener_conexion() as conexion:

                with conexion.cursor() as cursor:

                    cursor.execute(
                        """
                        INSERT INTO clientes (
                            nombre,
                            correo,
                            telefono,
                            ciudad,
                            activo
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            form.nombre.data,
                            form.correo.data,
                            form.telefono.data,
                            form.ciudad.data,
                            form.activo.data
                        )
                    )

                conexion.commit()

            flash(
                "Cliente registrado correctamente.",
                "success"
            )

            return redirect(
                url_for("clientes")
            )

        except psycopg.Error as error:

            flash(
                f"Error al registrar el cliente: {error}",
                "danger"
            )

    return render_template(
        "formulario_cliente.html",
        form=form,
        modo="registrar"
    )


# =========================================================
# CLIENTES - UPDATE
# =========================================================

@app.route(
    "/clientes/editar/<int:id_cliente>",
    methods=["GET", "POST"]
)
@login_required
def editar_cliente(id_cliente):

    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre,
                        correo,
                        telefono,
                        ciudad,
                        activo
                    FROM clientes
                    WHERE id = %s
                    """,
                    (id_cliente,)
                )

                cliente = cursor.fetchone()

    except psycopg.Error as error:

        flash(
            f"Error al consultar el cliente: {error}",
            "danger"
        )

        return redirect(
            url_for("clientes")
        )

    if cliente is None:

        flash(
            "El cliente seleccionado no existe.",
            "warning"
        )

        return redirect(
            url_for("clientes")
        )

    form = ClienteForm()

    if form.validate_on_submit():

        try:

            with obtener_conexion() as conexion:

                with conexion.cursor() as cursor:

                    cursor.execute(
                        """
                        UPDATE clientes
                        SET
                            nombre = %s,
                            correo = %s,
                            telefono = %s,
                            ciudad = %s,
                            activo = %s
                        WHERE id = %s
                        """,
                        (
                            form.nombre.data,
                            form.correo.data,
                            form.telefono.data,
                            form.ciudad.data,
                            form.activo.data,
                            id_cliente
                        )
                    )

                conexion.commit()

            flash(
                "Cliente modificado correctamente.",
                "success"
            )

            return redirect(
                url_for("clientes")
            )

        except psycopg.Error as error:

            flash(
                f"Error al modificar el cliente: {error}",
                "danger"
            )

    if request.method == "GET":

        form.nombre.data = cliente["nombre"]
        form.correo.data = cliente["correo"]
        form.telefono.data = cliente["telefono"]
        form.ciudad.data = cliente["ciudad"]
        form.activo.data = cliente["activo"]

    return render_template(
        "formulario_cliente.html",
        form=form,
        modo="editar"
    )


# =========================================================
# CLIENTES - DELETE
# =========================================================

@app.route(
    "/clientes/eliminar/<int:id_cliente>",
    methods=["POST"]
)
@login_required
def eliminar_cliente(id_cliente):

    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    DELETE FROM clientes
                    WHERE id = %s
                    """,
                    (id_cliente,)
                )

                eliminado = cursor.rowcount

            conexion.commit()

        if eliminado:

            flash(
                "Cliente eliminado correctamente.",
                "success"
            )

        else:

            flash(
                "El cliente seleccionado no existe.",
                "warning"
            )

    except psycopg.Error as error:

        flash(
            f"No se pudo eliminar el cliente: {error}",
            "danger"
        )

    return redirect(
        url_for("clientes")
    )


# =========================================================
# PROVEEDORES - SELECT
# =========================================================

@app.route("/proveedores")
@login_required
def proveedores():

    lista_proveedores = []

    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre,
                        productos,
                        contacto,
                        ciudad,
                        activo
                    FROM proveedores
                    ORDER BY id
                    """
                )

                lista_proveedores = cursor.fetchall()

    except psycopg.Error as error:

        flash(
            f"Error al consultar los proveedores: {error}",
            "danger"
        )

    activos = sum(
        1
        for proveedor in lista_proveedores
        if proveedor["activo"]
    )

    inactivos = len(lista_proveedores) - activos

    return render_template(
        "proveedores.html",
        titulo="Proveedores",
        proveedores=lista_proveedores,
        activos=activos,
        inactivos=inactivos
    )


# =========================================================
# PROVEEDORES - INSERT
# =========================================================

@app.route(
    "/proveedores/registrar",
    methods=["GET", "POST"]
)
@login_required
def registrar_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        try:

            with obtener_conexion() as conexion:

                with conexion.cursor() as cursor:

                    cursor.execute(
                        """
                        INSERT INTO proveedores (
                            nombre,
                            productos,
                            contacto,
                            ciudad,
                            activo
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            form.nombre.data,
                            form.productos.data,
                            form.contacto.data,
                            form.ciudad.data,
                            form.activo.data
                        )
                    )

                conexion.commit()

            flash(
                "Proveedor registrado correctamente.",
                "success"
            )

            return redirect(
                url_for("proveedores")
            )

        except psycopg.Error as error:

            flash(
                f"Error al registrar el proveedor: {error}",
                "danger"
            )

    return render_template(
        "formulario_proveedor.html",
        form=form,
        modo="registrar"
    )


# =========================================================
# PROVEEDORES - UPDATE
# =========================================================

@app.route(
    "/proveedores/editar/<int:id_proveedor>",
    methods=["GET", "POST"]
)
@login_required
def editar_proveedor(id_proveedor):

    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre,
                        productos,
                        contacto,
                        ciudad,
                        activo
                    FROM proveedores
                    WHERE id = %s
                    """,
                    (id_proveedor,)
                )

                proveedor = cursor.fetchone()

    except psycopg.Error as error:

        flash(
            f"Error al consultar el proveedor: {error}",
            "danger"
        )

        return redirect(
            url_for("proveedores")
        )

    if proveedor is None:

        flash(
            "El proveedor seleccionado no existe.",
            "warning"
        )

        return redirect(
            url_for("proveedores")
        )

    form = ProveedorForm()

    if form.validate_on_submit():

        try:

            with obtener_conexion() as conexion:

                with conexion.cursor() as cursor:

                    cursor.execute(
                        """
                        UPDATE proveedores
                        SET
                            nombre = %s,
                            productos = %s,
                            contacto = %s,
                            ciudad = %s,
                            activo = %s
                        WHERE id = %s
                        """,
                        (
                            form.nombre.data,
                            form.productos.data,
                            form.contacto.data,
                            form.ciudad.data,
                            form.activo.data,
                            id_proveedor
                        )
                    )

                conexion.commit()

            flash(
                "Proveedor modificado correctamente.",
                "success"
            )

            return redirect(
                url_for("proveedores")
            )

        except psycopg.Error as error:

            flash(
                f"Error al modificar el proveedor: {error}",
                "danger"
            )

    if request.method == "GET":

        form.nombre.data = proveedor["nombre"]
        form.productos.data = proveedor["productos"]
        form.contacto.data = proveedor["contacto"]
        form.ciudad.data = proveedor["ciudad"]
        form.activo.data = proveedor["activo"]

    return render_template(
        "formulario_proveedor.html",
        form=form,
        modo="editar"
    )


# =========================================================
# PROVEEDORES - DELETE
# =========================================================

@app.route(
    "/proveedores/eliminar/<int:id_proveedor>",
    methods=["POST"]
)
@login_required
def eliminar_proveedor(id_proveedor):

    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    DELETE FROM proveedores
                    WHERE id = %s
                    """,
                    (id_proveedor,)
                )

                eliminado = cursor.rowcount

            conexion.commit()

        if eliminado:

            flash(
                "Proveedor eliminado correctamente.",
                "success"
            )

        else:

            flash(
                "El proveedor seleccionado no existe.",
                "warning"
            )

    except psycopg.Error as error:

        flash(
            f"No se pudo eliminar el proveedor: {error}",
            "danger"
        )

    return redirect(
        url_for("proveedores")
    )


# =========================================================
# FACTURACIÓN - SELECT
# =========================================================

@app.route("/facturacion")
@login_required
def facturacion():

    lista_facturas = []

    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        f.id,
                        f.numero,
                        f.fecha,
                        f.forma_pago,
                        f.pagada,

                        c.nombre AS cliente_nombre,
                        c.correo AS cliente_correo,

                        p.nombre AS producto_nombre,

                        d.cantidad,
                        d.precio,

                        (d.cantidad * d.precio) AS subtotal

                    FROM facturas AS f

                    INNER JOIN clientes AS c
                        ON f.cliente_id = c.id

                    INNER JOIN detalle_factura AS d
                        ON d.factura_id = f.id

                    INNER JOIN productos AS p
                        ON d.producto_id = p.id

                    ORDER BY f.id DESC
                    """
                )

                lista_facturas = cursor.fetchall()

    except psycopg.Error as error:

        flash(
            f"Error al consultar la facturación: {error}",
            "danger"
        )

    productos_vendidos = sum(
        factura["cantidad"]
        for factura in lista_facturas
    )

    total_facturado = sum(
        (
            factura["subtotal"]
            for factura in lista_facturas
        ),
        Decimal("0.00")
    )

    return render_template(
        "facturacion.html",
        titulo="Facturación",
        facturas=lista_facturas,
        productos_vendidos=productos_vendidos,
        total_facturado=total_facturado
    )


# =========================================================
# FACTURACIÓN - INSERT
# =========================================================

@app.route(
    "/facturacion/registrar",
    methods=["GET", "POST"]
)
@login_required
def registrar_facturacion():

    form = FacturacionForm()

    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                # CARGAR CLIENTES
                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre,
                        correo
                    FROM clientes
                    WHERE activo = TRUE
                    ORDER BY nombre
                    """
                )

                clientes = cursor.fetchall()

                form.cliente_id.choices = [
                    (
                        cliente["id"],
                        f'{cliente["nombre"]} - {cliente["correo"]}'
                    )
                    for cliente in clientes
                ]

                # CARGAR PRODUCTOS
                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre,
                        stock
                    FROM productos
                    ORDER BY nombre
                    """
                )

                productos = cursor.fetchall()

                form.producto_id.choices = [
                    (
                        producto["id"],
                        f'{producto["nombre"]} - Stock: {producto["stock"]}'
                    )
                    for producto in productos
                ]

    except psycopg.Error as error:

        flash(
            f"Error al cargar clientes o productos: {error}",
            "danger"
        )

    if form.validate_on_submit():

        try:

            with obtener_conexion() as conexion:

                with conexion.cursor() as cursor:

                    # COMPROBAR PRODUCTO Y STOCK
                    cursor.execute(
                        """
                        SELECT
                            id,
                            stock
                        FROM productos
                        WHERE id = %s
                        """,
                        (
                            form.producto_id.data,
                        )
                    )

                    producto = cursor.fetchone()

                    if producto is None:

                        flash(
                            "El producto seleccionado no existe.",
                            "warning"
                        )

                        return render_template(
                            "formulario_facturacion.html",
                            form=form,
                            modo="registrar"
                        )

                    if producto["stock"] < form.cantidad.data:

                        flash(
                            "No existe stock suficiente para registrar la factura.",
                            "warning"
                        )

                        return render_template(
                            "formulario_facturacion.html",
                            form=form,
                            modo="registrar"
                        )

                    # CREAR FACTURA
                    cursor.execute(
                        """
                        INSERT INTO facturas (
                            numero,
                            fecha,
                            cliente_id,
                            forma_pago,
                            pagada
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (
                            form.numero.data,
                            form.fecha.data,
                            form.cliente_id.data,
                            form.forma_pago.data,
                            form.pagada.data
                        )
                    )

                    factura = cursor.fetchone()

                    # CREAR DETALLE
                    cursor.execute(
                        """
                        INSERT INTO detalle_factura (
                            factura_id,
                            producto_id,
                            cantidad,
                            precio
                        )
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            factura["id"],
                            form.producto_id.data,
                            form.cantidad.data,
                            form.precio.data
                        )
                    )

                    # ACTUALIZAR STOCK
                    cursor.execute(
                        """
                        UPDATE productos
                        SET stock = stock - %s
                        WHERE id = %s
                        """,
                        (
                            form.cantidad.data,
                            form.producto_id.data
                        )
                    )

                conexion.commit()

            flash(
                "Factura registrada correctamente.",
                "success"
            )

            return redirect(
                url_for("facturacion")
            )

        except psycopg.Error as error:

            flash(
                f"Error al registrar la factura: {error}",
                "danger"
            )

    return render_template(
        "formulario_facturacion.html",
        form=form,
        modo="registrar"
    )

# =========================================================
# FACTURACIÓN - UPDATE
# =========================================================

@app.route(
    "/facturacion/editar/<int:id_factura>",
    methods=["GET", "POST"]
)
@login_required
def editar_facturacion(id_factura):

    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                # BUSCAR FACTURA ACTUAL
                cursor.execute(
                    """
                    SELECT
                        f.id,
                        f.numero,
                        f.fecha,
                        f.cliente_id,
                        f.forma_pago,
                        f.pagada,

                        d.id AS detalle_id,
                        d.producto_id,
                        d.cantidad,
                        d.precio

                    FROM facturas AS f

                    INNER JOIN detalle_factura AS d
                        ON d.factura_id = f.id

                    WHERE f.id = %s
                    """,
                    (
                        id_factura,
                    )
                )

                factura = cursor.fetchone()

                # CARGAR CLIENTES
                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre,
                        correo
                    FROM clientes
                    WHERE activo = TRUE
                    ORDER BY nombre
                    """
                )

                clientes = cursor.fetchall()

                # CARGAR PRODUCTOS
                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre,
                        stock
                    FROM productos
                    ORDER BY nombre
                    """
                )

                productos = cursor.fetchall()

    except psycopg.Error as error:

        flash(
            f"Error al consultar la factura: {error}",
            "danger"
        )

        return redirect(
            url_for("facturacion")
        )

    if factura is None:

        flash(
            "La factura seleccionada no existe.",
            "warning"
        )

        return redirect(
            url_for("facturacion")
        )

    form = FacturacionForm()

    form.cliente_id.choices = [
        (
            cliente["id"],
            f'{cliente["nombre"]} - {cliente["correo"]}'
        )
        for cliente in clientes
    ]

    form.producto_id.choices = [
        (
            producto["id"],
            f'{producto["nombre"]} - Stock: {producto["stock"]}'
        )
        for producto in productos
    ]

    if form.validate_on_submit():

        try:

            with obtener_conexion() as conexion:

                with conexion.cursor() as cursor:

                    # DEVOLVER STOCK ANTERIOR
                    cursor.execute(
                        """
                        UPDATE productos
                        SET stock = stock + %s
                        WHERE id = %s
                        """,
                        (
                            factura["cantidad"],
                            factura["producto_id"]
                        )
                    )

                    # BUSCAR PRODUCTO SELECCIONADO
                    cursor.execute(
                        """
                        SELECT
                            id,
                            stock
                        FROM productos
                        WHERE id = %s
                        """,
                        (
                            form.producto_id.data,
                        )
                    )

                    producto = cursor.fetchone()

                    if producto is None:

                        conexion.rollback()

                        flash(
                            "El producto seleccionado no existe.",
                            "warning"
                        )

                        return render_template(
                            "formulario_facturacion.html",
                            form=form,
                            modo="editar"
                        )

                    # COMPROBAR STOCK
                    if producto["stock"] < form.cantidad.data:

                        conexion.rollback()

                        flash(
                            "No existe stock suficiente.",
                            "warning"
                        )

                        return render_template(
                            "formulario_facturacion.html",
                            form=form,
                            modo="editar"
                        )

                    # ACTUALIZAR FACTURA
                    cursor.execute(
                        """
                        UPDATE facturas
                        SET
                            numero = %s,
                            fecha = %s,
                            cliente_id = %s,
                            forma_pago = %s,
                            pagada = %s
                        WHERE id = %s
                        """,
                        (
                            form.numero.data,
                            form.fecha.data,
                            form.cliente_id.data,
                            form.forma_pago.data,
                            form.pagada.data,
                            id_factura
                        )
                    )

                    # ACTUALIZAR DETALLE
                    cursor.execute(
                        """
                        UPDATE detalle_factura
                        SET
                            producto_id = %s,
                            cantidad = %s,
                            precio = %s
                        WHERE id = %s
                        """,
                        (
                            form.producto_id.data,
                            form.cantidad.data,
                            form.precio.data,
                            factura["detalle_id"]
                        )
                    )

                    # DESCONTAR STOCK NUEVO
                    cursor.execute(
                        """
                        UPDATE productos
                        SET stock = stock - %s
                        WHERE id = %s
                        """,
                        (
                            form.cantidad.data,
                            form.producto_id.data
                        )
                    )

                conexion.commit()

            flash(
                "Factura modificada correctamente.",
                "success"
            )

            return redirect(
                url_for("facturacion")
            )

        except psycopg.Error as error:

            flash(
                f"Error al modificar la factura: {error}",
                "danger"
            )

    if request.method == "GET":

        form.numero.data = factura["numero"]
        form.fecha.data = factura["fecha"]
        form.cliente_id.data = factura["cliente_id"]
        form.forma_pago.data = factura["forma_pago"]
        form.pagada.data = factura["pagada"]
        form.producto_id.data = factura["producto_id"]
        form.cantidad.data = factura["cantidad"]
        form.precio.data = factura["precio"]

    return render_template(
        "formulario_facturacion.html",
        form=form,
        modo="editar"
    )

# =========================================================
# FACTURACIÓN - DELETE
# =========================================================

@app.route(
    "/facturacion/eliminar/<int:id_factura>",
    methods=["POST"]
)
@login_required
def eliminar_facturacion(id_factura):

    try:

        with obtener_conexion() as conexion:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        producto_id,
                        cantidad
                    FROM detalle_factura
                    WHERE factura_id = %s
                    """,
                    (id_factura,)
                )

                detalle = cursor.fetchone()

                if detalle is None:

                    flash(
                        "La factura seleccionada no existe.",
                        "warning"
                    )

                    return redirect(
                        url_for("facturacion")
                    )

                # RESTAURAR STOCK
                cursor.execute(
                    """
                    UPDATE productos
                    SET stock = stock + %s
                    WHERE id = %s
                    """,
                    (
                        detalle["cantidad"],
                        detalle["producto_id"]
                    )
                )

                # ELIMINAR DETALLE
                cursor.execute(
                    """
                    DELETE FROM detalle_factura
                    WHERE factura_id = %s
                    """,
                    (id_factura,)
                )

                # ELIMINAR FACTURA
                cursor.execute(
                    """
                    DELETE FROM facturas
                    WHERE id = %s
                    """,
                    (id_factura,)
                )

            conexion.commit()

        flash(
            "Factura eliminada correctamente.",
            "success"
        )

    except psycopg.Error as error:

        flash(
            f"No se pudo eliminar la factura: {error}",
            "danger"
        )

    return redirect(
        url_for("facturacion")
    )


# =========================================================
# EJECUCIÓN
# =========================================================

if __name__ == "__main__":

    comprobar_conexion_postgresql()

    app.run(
        debug=True
    )