from decimal import Decimal

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DateField,
    SelectField,
    BooleanField,
    IntegerField,
    DecimalField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    InputRequired,
    NumberRange
)


class FacturacionForm(FlaskForm):

    numero = StringField(
        "Número de factura",
        validators=[
            DataRequired(
                message="El número de factura es obligatorio."
            ),
            Length(
                min=3,
                max=30,
                message="El número de factura debe tener entre 3 y 30 caracteres."
            )
        ]
    )

    fecha = DateField(
        "Fecha",
        format="%Y-%m-%d",
        validators=[
            DataRequired(
                message="La fecha es obligatoria."
            )
        ]
    )

    cliente_nombre = StringField(
        "Nombre del cliente",
        validators=[
            DataRequired(
                message="El nombre del cliente es obligatorio."
            ),
            Length(
                min=3,
                max=80,
                message="El nombre debe tener entre 3 y 80 caracteres."
            )
        ]
    )

    cliente_correo = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(
                message="El correo electrónico es obligatorio."
            ),
            Email(
                message="Ingrese un correo electrónico válido."
            ),
            Length(
                max=120,
                message="El correo no puede superar los 120 caracteres."
            )
        ]
    )

    cliente_telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(
                message="El teléfono del cliente es obligatorio."
            ),
            Length(
                min=7,
                max=15,
                message="El teléfono debe tener entre 7 y 15 caracteres."
            )
        ]
    )

    forma_pago = SelectField(
        "Forma de pago",
        choices=[
            ("", "Seleccione una forma de pago"),
            ("Efectivo", "Efectivo"),
            ("Tarjeta", "Tarjeta"),
            ("Transferencia", "Transferencia")
        ],
        validators=[
            DataRequired(
                message="Debe seleccionar una forma de pago."
            )
        ]
    )

    pagada = BooleanField(
        "Factura pagada",
        default=True
    )

    producto = StringField(
        "Producto",
        validators=[
            DataRequired(
                message="El producto es obligatorio."
            ),
            Length(
                min=2,
                max=80,
                message="El nombre del producto debe tener entre 2 y 80 caracteres."
            )
        ]
    )

    cantidad = IntegerField(
        "Cantidad",
        validators=[
            InputRequired(
                message="La cantidad es obligatoria."
            ),
            NumberRange(
                min=1,
                max=100,
                message="La cantidad debe estar entre 1 y 100."
            )
        ]
    )

    precio = DecimalField(
        "Precio unitario",
        places=2,
        rounding=None,
        validators=[
            InputRequired(
                message="El precio unitario es obligatorio."
            ),
            NumberRange(
                min=Decimal("0.01"),
                max=Decimal("10000.00"),
                message="El precio debe ser mayor a 0 y no superar los $10.000."
            )
        ]
    )

    submit = SubmitField(
        "Guardar factura"
    )