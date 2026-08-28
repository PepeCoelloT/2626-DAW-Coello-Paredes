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
# En esta etapa académica se utiliza una clave local.
app.config["SECRET_KEY"] = "fitzone-store-semana11-2026"


# =========================================================
# DATOS TEMPORALES DEL SISTEMA
# SEMANA 11 - FORMULARIOS Y VALIDACIÓN
# =========================================================
#
# En esta etapa todavía no se utiliza una base de datos.
# Los datos permanecen en memoria mientras la aplicación
# se encuentra en ejecución.
# =========================================================


# ---------------------------------------------------------
# PRODUCTOS
# ---------------------------------------------------------

lista_productos = [
    {
        "nombre": "Bandas elásticas",
        "categoria": "Fuerza",
        "descripcion": "Ideales para ejercicios de fuerza, movilidad y entrenamiento funcional.",
        "stock": 10
    },
    {
        "nombre": "Mancuernas",
        "categoria": "Fuerza",
        "descripcion": "Accesorios para entrenar brazos, hombros, espalda y piernas.",
        "stock": 8
    },
    {
        "nombre": "Colchonetas",
        "categoria": "Movilidad",
        "descripcion": "Recomendadas para yoga, abdominales y estiramientos.",
        "stock": 0
    },
    {
        "nombre": "Botellas deportivas",
        "categoria": "Accesorios",
        "descripcion": "Útiles para mantener una correcta hidratación durante el entrenamiento.",
        "stock": 15
    },
    {
        "nombre": "Guantes de gimnasio",
        "categoria": "Accesorios",
        "descripcion": "Brindan comodidad y protección durante ejercicios con peso.",
        "stock": 6
    },
    {
        "nombre": "Ropa deportiva",
        "categoria": "Ropa deportiva",
        "descripcion": "Prendas cómodas para entrenamientos en casa, gimnasio o al aire libre.",
        "stock": 0
    }
]


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
# =========================================================


# ---------------------------------------------------------
# LISTADO DE PRODUCTOS
# ---------------------------------------------------------

@app.route("/productos")
def productos():

    titulo = "Gestión de Productos"

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
# ---------------------------------------------------------

@app.route(
    "/productos/nuevo",
    methods=["GET", "POST"]
)
def registrar_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        nuevo_producto = {
            "nombre": form.nombre.data,
            "categoria": form.categoria.data,
            "descripcion": form.descripcion.data,
            "stock": form.stock.data
        }

        lista_productos.append(
            nuevo_producto
        )

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

    app.run(
        debug=True
    )