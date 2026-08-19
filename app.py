from flask import Flask, render_template

app = Flask(__name__)


# =========================================================
# DATOS TEMPORALES DEL SISTEMA
# SEMANA 10 - CONTENIDO DINÁMICO CON JINJA2
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


# =========================================================
# RUTAS
# =========================================================


# ---------------------------------------------------------
# INICIO
# ---------------------------------------------------------

@app.route("/")
def inicio():
    return render_template("index.html")


# ---------------------------------------------------------
# PRODUCTOS
# ---------------------------------------------------------

@app.route("/productos")
def productos():

    titulo = "Gestión de Productos"

    disponibles = sum(
        1 for producto in lista_productos
        if producto["stock"] > 0
    )

    agotados = sum(
        1 for producto in lista_productos
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
# CLIENTES
# ---------------------------------------------------------

@app.route("/clientes")
def clientes():

    titulo = "Gestión de Clientes"

    activos = sum(
        1 for cliente in lista_clientes
        if cliente["activo"]
    )

    inactivos = sum(
        1 for cliente in lista_clientes
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
# PROVEEDORES
# ---------------------------------------------------------

@app.route("/proveedores")
def proveedores():

    titulo = "Gestión de Proveedores"

    activos = sum(
        1 for proveedor in lista_proveedores
        if proveedor["activo"]
    )

    inactivos = sum(
        1 for proveedor in lista_proveedores
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
# FACTURACIÓN
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

    facturas_registradas = 3

    return render_template(
        "facturacion.html",
        titulo=titulo,
        factura=factura_actual,
        subtotal=subtotal,
        iva=iva,
        total=total,
        productos_vendidos=productos_vendidos,
        facturas_registradas=facturas_registradas
    )


# =========================================================
# EJECUCIÓN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)